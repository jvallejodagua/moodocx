# -*- coding: utf-8 -*-
# docx_to_pydantic.py

"""
Módulo para la conversión de documentos Word (.docx) de cuestionarios
a un modelo de datos estructurado utilizando Pydantic.

Versión 0.0.8: Refactorizado para una detección robusta de la numeración.
- Lee directamente 'word/numbering.xml' para interpretar los estilos de lista.
- Identifica preguntas y opciones basándose en el formato de numeración 
  (ej. 'decimal' para preguntas, 'upperLetter' para opciones) en lugar de 
  depender del frágil 'ilvl'.
- Es inmune a los cambios en los valores de 'numId' internos de Word.
"""

import os
import base64
import io
from typing import List, Optional, Dict, Any

# --- Dependencias ---
# pip install python-docx lxml pydantic
import docx
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from docx.parts.document import DocumentPart
# <<< CORRECCIÓN 1: Añadir la importación correcta para la clase 'Part'
from docx.opc.part import Part
from lxml import etree
from pydantic import BaseModel, Field
from pathlib import Path

from filesystem.files_finder import FilesInSubfolder
from html_css_encoder.image_word_to_image_tag import generate_html_image_output

# --- Modelos Pydantic para la Estructura de Datos ---
# (Sin cambios en los modelos)

class OptionModel(BaseModel):
    """Representa una única opción de respuesta."""
    identifier: str
    content_html: str
    is_correct: bool = False

class QuestionModel(BaseModel):
    """Representa una pregunta completa con su enunciado y opciones."""
    identifier: str
    prompt_html: str
    options: List[OptionModel] = Field(default_factory=list)

class DocumentModel(BaseModel):
    """Representa el contenido completo de un archivo .docx."""
    file_path: Path
    questions: List[QuestionModel] = Field(default_factory=list)


class DocxToPydantic:
    """
    Clase principal que orquesta la conversión de archivos .docx
    a una lista de modelos Pydantic (DocumentModel).
    """
    NAMESPACES = {
        'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
        'pic': 'http://schemas.openxmlformats.org/drawingml/2006/picture',
        'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
    }

    def __init__(self):
        ### REFAC: Inicializar diccionarios para almacenar las definiciones de numeración.
        # Esto se llenará una vez por documento.
        self.numbering_definitions: Dict[str, Dict[str, Dict[str, str]]] = {}
        self.num_to_abstract_map: Dict[str, str] = {}

    def parse_all(self, folder_path: str) -> List[DocumentModel]:
        """
        Punto de entrada principal. Procesa todos los archivos .docx en la
        carpeta especificada.
        """

        files_finder = FilesInSubfolder(folder_path, ".docx")
        
        files = files_finder.get_files()

        all_documents = []
        
        for file in files:

            if "~" not in file.name:
                
                print(f"Procesando archivo: {file.name}...")
                try:
                    # ### REFAC: Reiniciar definiciones para cada archivo
                    self.numbering_definitions = {}
                    self.num_to_abstract_map = {}
                    document_model = self._parse_document(file)
                    if document_model:
                        all_documents.append(document_model)
                except Exception as e:
                    print(f"Error al procesar el archivo {file.name}: {e}")
        
        return all_documents

    ### REFAC: Nuevo método para parsear numbering.xml
    # <<< CORRECCIÓN 2: Usar el tipo 'Part' importado correctamente
    def _parse_numbering_definitions(self, numbering_part: Part):
        """
        Lee el archivo numbering.xml y crea mapas en memoria para una
        búsqueda rápida de los estilos de numeración.
        """
        if numbering_part is None:
            return

        numbering_xml = etree.fromstring(numbering_part.blob)

        # Paso 1: Mapear numId a abstractNumId
        for num_element in numbering_xml.findall('w:num', self.NAMESPACES):
            num_id = num_element.get(f'{{{self.NAMESPACES["w"]}}}numId')
            abstract_num_id_element = num_element.find('w:abstractNumId', self.NAMESPACES)
            if num_id is not None and abstract_num_id_element is not None:
                abstract_num_id = abstract_num_id_element.get(f'{{{self.NAMESPACES["w"]}}}val')
                self.num_to_abstract_map[num_id] = abstract_num_id

        # Paso 2: Mapear cada abstractNumId y nivel (ilvl) a su formato (numFmt)
        for abstract_num_element in numbering_xml.findall('w:abstractNum', self.NAMESPACES):
            abstract_id = abstract_num_element.get(f'{{{self.NAMESPACES["w"]}}}abstractNumId')
            if abstract_id not in self.numbering_definitions:
                self.numbering_definitions[abstract_id] = {}
            
            for lvl_element in abstract_num_element.findall('w:lvl', self.NAMESPACES):
                ilvl = lvl_element.get(f'{{{self.NAMESPACES["w"]}}}ilvl')
                num_fmt_element = lvl_element.find('w:numFmt', self.NAMESPACES)
                if ilvl is not None and num_fmt_element is not None:
                    num_fmt = num_fmt_element.get(f'{{{self.NAMESPACES["w"]}}}val')
                    self.numbering_definitions[abstract_id][ilvl] = {'format': num_fmt}

    def _parse_document(self, docx_path: Path) -> Optional[DocumentModel]:
        """
        Procesa un único archivo .docx y lo convierte en un DocumentModel.
        """
        try:
            document = docx.Document(docx_path)
            doc_part = document.part
            
            ### REFAC: Obtener y parsear el 'numbering.xml' ANTES de procesar los párrafos.
            numbering_part = doc_part.part_related_by(RT.NUMBERING)
            self._parse_numbering_definitions(numbering_part)

            xml_content = doc_part.blob
            root = etree.fromstring(xml_content)
            body = root.find('w:body', self.NAMESPACES)
        except Exception as e:
            print(f"No se pudo abrir o parsear el XML de {docx_path}: {e}")
            return None

        intermediate_blocks = []
        for p_element in body.findall('w:p', self.NAMESPACES):
            num_pr = p_element.find('.//w:numPr', self.NAMESPACES)
            
            ### REFAC: Lógica de clasificación robusta
            list_type = 'continuation' # Por defecto, es continuación de lo anterior
            if num_pr is not None:
                ilvl_element = num_pr.find('w:ilvl', self.NAMESPACES)
                num_id_element = num_pr.find('w:numId', self.NAMESPACES)
                
                if ilvl_element is not None and num_id_element is not None:
                    ilvl = ilvl_element.get(f'{{{self.NAMESPACES["w"]}}}val')
                    num_id = num_id_element.get(f'{{{self.NAMESPACES["w"]}}}val')
                    
                    abstract_id = self.num_to_abstract_map.get(num_id)
                    if abstract_id:
                        style = self.numbering_definitions.get(abstract_id, {}).get(ilvl)
                        if style:
                            num_format = style.get('format')
                            if num_format == 'decimal':
                                list_type = 'question'
                            elif num_format in ['upperLetter', 'lowerLetter', 'upperRoman', 'lowerRoman']:
                                list_type = 'option'
            
            html_content = self._paragraph_to_html(p_element, doc_part)
            is_highlighted = self._is_paragraph_highlighted(p_element)
            
            intermediate_blocks.append({
                'type': list_type, # Usamos 'type' en lugar de 'level'
                'html': html_content,
                'is_correct': is_highlighted
            })

        return self._build_model_from_blocks(intermediate_blocks, docx_path)

    def _paragraph_to_html(self, p_element: etree._Element, doc_part: DocumentPart) -> str:
        # (Sin cambios en este método)
        html_parts = []
        if not p_element.xpath(".//*[self::w:t or self::w:drawing]", namespaces=self.NAMESPACES):
            return "<div><br></div>"
        for run_element in p_element.findall('w:r', self.NAMESPACES):
            drawing = run_element.find('w:drawing', self.NAMESPACES)
            if drawing is not None:
                blip = drawing.find('.//a:blip', self.NAMESPACES)
                if blip is not None:
                    embed_id = blip.get(f'{{{self.NAMESPACES["r"]}}}embed')
                    if embed_id:
                        try:
                            img_tag = generate_html_image_output(doc_part, embed_id, drawing)
                            html_parts.append(img_tag)
                        except KeyError:
                            html_parts.append(f"[IMAGEN NO ENCONTRADA: {embed_id}]")
            else:
                text = "".join(run_element.xpath('.//w:t/text()', namespaces=self.NAMESPACES))
                rpr = run_element.find('w:rPr', self.NAMESPACES)
                if rpr is not None:
                    if rpr.find('w:b', self.NAMESPACES) is not None: text = f"<b>{text}</b>"
                    if rpr.find('w:i', self.NAMESPACES) is not None: text = f"<i>{text}</i>"
                    vert_align = rpr.find('w:vertAlign', self.NAMESPACES)
                    if vert_align is not None:
                        val = vert_align.get(f'{{{self.NAMESPACES["w"]}}}val')
                        if val == 'subscript': text = f"<sub>{text}</sub>"
                        elif val == 'superscript': text = f"<sup>{text}</sup>"
                html_parts.append(text)
        return f"<div style='font-size: 21px;'>{''.join(html_parts)}</div>"

    def _is_paragraph_highlighted(self, p_element: etree._Element) -> bool:
        # (Sin cambios en este método)
        return p_element.find('.//w:highlight', self.NAMESPACES) is not None

    ### REFAC: Lógica de construcción basada en 'type' en lugar de 'level'
    def _build_model_from_blocks(self, blocks: list, file_path: Path) -> DocumentModel:
        """
        Construye el DocumentModel final a partir de la lista de bloques intermedios.
        Ahora utiliza el 'type' semántico ('question', 'option') para la lógica.
        """
        doc_model = DocumentModel(file_path=file_path)
        current_question: Optional[QuestionModel] = None
        question_counter = 0

        for block in blocks:
            block_type = block['type']
            html = block['html']
            is_correct = block['is_correct']

            if block_type == 'question':
                if current_question:
                    doc_model.questions.append(current_question)
                
                question_counter += 1
                prompt_final_html = f"<div style='font-size: 21px;'><prompt>{html}</prompt></div>"
                current_question = QuestionModel(
                    identifier=str(question_counter), # El número real secuencial
                    prompt_html=prompt_final_html
                )

            elif block_type == 'option':
                if current_question:
                    # El identificador se basa en el conteo de opciones para esta pregunta
                    option_identifier = chr(65 + len(current_question.options)) # A, B, C...
                    content_final_html = f'<div style="font-size: 21px;"><simpleChoice identifier="{option_identifier}">{html}</simpleChoice></div>'
                    option = OptionModel(
                        identifier=option_identifier,
                        content_html=content_final_html,
                        is_correct=is_correct
                    )
                    current_question.options.append(option)

            elif block_type == 'continuation':
                if current_question:
                    if current_question.options:
                        last_option = current_question.options[-1]
                        inner_html = last_option.content_html.split('>', 2)[2].rsplit('<', 2)[0]
                        new_inner_html = inner_html + html
                        last_option.content_html = f'<div style="font-size: 21px;"><simpleChoice identifier="{last_option.identifier}">{new_inner_html}</simpleChoice></div>'
                        if is_correct:
                            last_option.is_correct = True
                    else:
                        inner_html = current_question.prompt_html.split('>', 2)[2].rsplit('<', 2)[0]
                        new_inner_html = inner_html + html
                        current_question.prompt_html = f"<div style='font-size: 21px;'><prompt>{new_inner_html}</prompt></div>"

        if current_question:
            doc_model.questions.append(current_question)

        return doc_model


# --- Bloque de Ejecución Principal ---
if __name__ == "__main__":
    print("--- INICIO DE LA DEMOSTRACIÓN COMPLETA (V0.1.0 - ROBUSTA) ---")
    
    INPUT_FOLDER = "Temporales"
    OUTPUT_FOLDER = "Temporales"
    
    os.makedirs(INPUT_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    print(f"Carpetas de trabajo '{INPUT_FOLDER}' y '{OUTPUT_FOLDER}' aseguradas.")

    parser = DocxToPydantic()

    print("\n--- Iniciando el proceso de parsing con lógica mejorada ---")
    document_models = parser.parse_all(INPUT_FOLDER)

    if document_models:
        print(f"\n--- Proceso completado. Se han parseado {len(document_models)} documentos. ---")
        print(f"--- Exportando resultados a la carpeta '{OUTPUT_FOLDER}' ---")
        
        for doc_model in document_models:
            output_filename = doc_model.file_path.stem + ".json"
            output_path = doc_model.file_path.parent / output_filename
            json_output = doc_model.model_dump_json(indent=2)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(json_output)
            print(f"  - Resultados de '{doc_model.file_path.name}' exportados a '{output_path}'")
            
    else:
        print("\nNo se procesaron documentos. Verifique la carpeta de entrada o los logs de errores.")

    print("\n--- FIN DE LA DEMOSTRACIÓN ---")