# -*- coding: utf-8 -*-
# pydantic_to_moodle_xml_converter.py

"""
Módulo para convertir los modelos Pydantic de cuestionarios, generados por
DocxToPydanticParser, al formato XML de Moodle.

Este script toma una lista de objetos DocumentModel y genera un archivo XML
independiente para cada uno, listo para ser importado en Moodle.
"""

import os
from typing import List
import xml.etree.ElementTree as ET
from xml.dom import minidom

# --- Dependencias del proyecto ---
from json_handler.docx_to_pydantic import DocxToPydantic, DocumentModel, QuestionModel

class PydanticToMoodleXmlConverter:
    """
    Convierte una lista de modelos Pydantic (DocumentModel) a archivos XML
    en formato Moodle Quiz.
    """

    def __init__(self, input_dir: str, output_dir: str):
        self.input_directory = input_dir
        self.output_directory = output_dir

    def _pretty_print_xml(self, root_element: ET.Element) -> str:
        """
        Formatea un elemento XML de ElementTree para que sea legible por humanos
        con indentación.

        Args:
            root_element: El elemento raíz del árbol XML.

        Returns:
            Una cadena de texto con el XML formateado.
        """
        # Convierte el árbol de ElementTree a una cadena de bytes
        rough_string = ET.tostring(root_element, 'utf-8')
        # Parsea la cadena con minidom para formatearla
        reparsed = minidom.parseString(rough_string)
        # Retorna el XML con indentación y declaración XML
        return reparsed.toprettyxml(indent="  ")

    def _create_question_element(self, question_model: QuestionModel) -> ET.Element:
        """
        Crea un único elemento <question> en formato Moodle XML a partir de
        un QuestionModel de Pydantic.

        Args:
            question_model: El modelo de datos de la pregunta.

        Returns:
            Un objeto ET.Element que representa la pregunta en XML.
        """
        # Elemento raíz de la pregunta
        question_element = ET.Element("question", type="multichoice")

        # --- Nombre de la pregunta (identificador único) ---
        name = ET.SubElement(question_element, "name")
        # Formateamos el identificador para que tenga ceros a la izquierda (ej. Q001)
        name_text = ET.SubElement(name, "text")
        name_text.text = f"Q{int(question_model.identifier):03d}"

        # --- Texto de la pregunta (enunciado) ---
        questiontext = ET.SubElement(question_element, "questiontext", format="html")
        questiontext_text = ET.SubElement(questiontext, "text")
        # Usamos CDATA para encapsular el contenido HTML de forma segura
        #questiontext_text.text = f"<![CDATA[{question_model.prompt_html}]]>"
        questiontext_text.text = question_model.prompt_html
        
        # --- Elementos boilerplate (valores fijos según el ejemplo) ---
        ET.SubElement(question_element, "tags")
        defaultgrade = ET.SubElement(question_element, "defaultgrade")
        defaultgrade.text = "1.0"
        hidden = ET.SubElement(question_element, "hidden")
        hidden.text = "0"
        penalty = ET.SubElement(question_element, "penalty")
        penalty.text = "0.0"
        generalfeedback = ET.SubElement(question_element, "generalfeedback")
        ET.SubElement(generalfeedback, "text")
        partiallycorrectfeedback = ET.SubElement(question_element, "partiallycorrectfeedback")
        ET.SubElement(partiallycorrectfeedback, "text")
        shuffleanswers = ET.SubElement(question_element, "shuffleanswers")
        shuffleanswers.text = "1"
        single = ET.SubElement(question_element, "single")
        single.text = "true"
        answernumbering = ET.SubElement(question_element, "answernumbering")
        answernumbering.text = "none"

        # --- Opciones de respuesta ---
        for option in question_model.options:
            fraction = "100" if option.is_correct else "0"
            answer = ET.SubElement(question_element, "answer", fraction=fraction)
            answer_text = ET.SubElement(answer, "text")
            # Usamos CDATA también para las opciones
            # answer_text.text = f"<![CDATA[{option.content_html}]]>"
            answer_text.text = option.content_html

        return question_element

    def process_and_save(self, document_models: List[DocumentModel], output_folder: str):
        """
        Método principal que procesa una lista de DocumentModel y guarda
        cada uno como un archivo XML de Moodle en la carpeta de salida.

        Args:
            document_models: Lista de objetos DocumentModel a convertir.
            output_folder: Ruta de la carpeta donde se guardarán los XML.
        """
        output_messages=[]

        if not document_models:
            output_messages.append("No se recibieron modelos de documento para procesar.")
            print(output_messages[-1])
            return

        os.makedirs(output_folder, exist_ok=True)
        print(f"\n--- Iniciando conversión a Moodle XML. Salida en '{output_folder}' ---")
        
        for doc_model in document_models:
            # --- Construcción del XML ---
            # 1. Crear el elemento raíz <quiz>
            quiz_root = ET.Element("quiz")

            # 2. Iterar sobre cada pregunta en el modelo y crear su elemento XML
            for question in doc_model.questions:
                question_xml_element = self._create_question_element(question)
                quiz_root.append(question_xml_element)

            # 3. Formatear el XML para que sea legible
            xml_content_str = self._pretty_print_xml(quiz_root)

            # --- Guardado del archivo ---
            output_filename = doc_model.file_path.stem + ".xml"
            output_path = doc_model.file_path.parent / output_filename

            try:
                with open(output_path, "w", encoding="utf-8") as f:
                    # Escribimos el contenido, omitiendo la declaración XML de minidom
                    # si se desea la que provee el ejemplo.
                    # La declaración <?xml version="1.0" encoding="UTF-8"?> es estándar.
                    f.write(xml_content_str)
                output_messages.append(f"  - Archivo '{doc_model.file_path.name}' convertido a '{output_path.name}' exitosamente.")
                print(output_messages[-1])
            except IOError as e:
                output_messages.append(f"  - Error al guardar el archivo '{output_path}': {e}")
                print(output_messages[-1])

    def run(self):
        
        # --- Paso 1: Usar el parser existente para obtener los modelos Pydantic ---
        print("--- Paso 1: Parseando documentos DOCX a modelos Pydantic ---")
        parser = DocxToPydantic()
        document_models = parser.parse_all(self.input_directory)

        if not document_models:
            output_message="No se encontraron o no se pudieron procesar archivos DOCX.\n\nAsegúrese de que haya archivos .docx en la carpeta 'Temporales'."
            print("\nNo se encontraron o no se pudieron procesar archivos DOCX.")
            print("Asegúrese de que haya archivos .docx en la carpeta 'Temporales'.")
        else:
            print(f"Se han parseado {len(document_models)} documentos.")
            
            # --- Paso 2: Usar el nuevo conversor para generar el XML de Moodle ---
            print("\n--- Paso 2: Convirtiendo modelos Pydantic a Moodle XML ---")
            self.process_and_save(document_models, self.output_directory)

            print("\n--- Proceso de conversión completado. ---")
            print(f"Puede encontrar los archivos XML en la carpeta '{self.output_directory}'.")

# --- Bloque de Ejecución Principal para Demostración ---
if __name__ == "__main__":
    # Definir carpetas de trabajo
    INPUT_FOLDER = "Temporales"
    OUTPUT_FOLDER = "Temporales" # Carpeta de salida para los XML

    converter = PydanticToMoodleXmlConverter(input_dir=INPUT_FOLDER, output_dir=OUTPUT_FOLDER)
    converter.run()