# -*- coding: utf-8 -*-
# md_quiz_to_docx_converter.py

"""
Script para reestructurar archivos Markdown de cuestionarios.

Dependencias:
- panflute: Una biblioteca para crear filtros de Pandoc en Python.
  Para instalarla, ejecuta: pip install panflute

Descripción:
Este script procesa archivos Markdown (.md) ubicados en una carpeta 'Temporales'.
La lógica de transformación es la siguiente:
1. Lee un archivo Markdown que contiene bloques de texto seguidos de preguntas
   de opción múltiple basadas en ese texto.
2. Identifica estos bloques de texto (contexto) y los bloques de preguntas
   (listas ordenadas).
3. Para cada pregunta en una lista, mueve el bloque de texto de contexto
   correspondiente al interior de la pregunta.
4. Antecede al texto movido la frase "De acuerdo al texto responde:" seguida
   de dos saltos de línea.
5. Conserva todo el formato de texto enriquecido (negritas, cursivas,
   resaltados, imágenes, etc.) gracias al uso de un AST (Abstract Syntax Tree)
   manejado por panflute/pandoc.
"""

import os
import sys
import subprocess
from contextlib import contextmanager

if sys.platform == "win32":
    _original_popen = subprocess.Popen

    class NoWindowPopen(_original_popen):
        def __init__(self, *args, **kwargs):
            # Forzamos la bandera para evitar la consola negra
            flags = kwargs.get('creationflags', 0)
            kwargs['creationflags'] = flags | subprocess.CREATE_NO_WINDOW
            
            # Seguridad adicional para PyInstaller sin consola
            if 'stdin' not in kwargs:
                kwargs['stdin'] = subprocess.DEVNULL
                
            super().__init__(*args, **kwargs)

    # Reemplazamos la clase en el módulo estándar
    subprocess.Popen = NoWindowPopen

import panflute as pf
from typing import List
from filesystem.files_finder import FilesInSubfolder
from pathlib import Path
from pandoc_handler.docx_post_processor import DocxPostProcessor

class MdQuizToDocxConverter:
    """
    Clase que encapsula la lógica para reestructurar archivos Markdown
    de cuestionarios.
    """

    def __init__(self,
        inputs_path: Path = Path("Temporales"),
        outputs_path: Path = Path("TemporalesTextoAVoz"),
        reuse_stimulus_input: bool = False,
        target_font: str = "Liberation Serif",
        target_font_size: int = 18,
        max_img_size: float = 17.5):
        """
        Inicializa el restructurador.

        Args:
            inputs_path (str): El nombre de la carpeta que contiene los
                                 archivos .md a procesar. Se espera que
                                 esté al mismo nivel que el script.
        """
        self.inputs_path = inputs_path
        self.destination_path = outputs_path
        self.reuse_stimulus = reuse_stimulus_input
        self.target_font = target_font
        self.target_font_size = target_font_size
        self.max_img_size = max_img_size
        
        self.files_finder = FilesInSubfolder(
            files_path = self.inputs_path,
            suffix_extension = ".md"
        )

    def reorder_doc(self, doc: pf.Doc) -> pf.Doc:
        '''
        Reorganiza las secciones no numeradas en lista numerada
        '''
        
        new_content: List[pf.Block]=[]
        current_context_blocks: List[pf.Block] = []
        prefix_text = "De acuerdo al texto responde:"
        each_list_item_content: List[pf.ListItem]=[]
                
        for elem in doc._content:
            if isinstance(elem, pf.OrderedList):
                prefix_para = pf.Para(pf.Str(prefix_text))

                cloned_context = [b for b in current_context_blocks]
                each_item_content: List[pf.Block]=[]
                
                #print(cloned_context)

                for each_list_item in elem._content:
                    for each_item in each_list_item._content:
                        each_item_content.append(each_item)
                    each_list_item_content.append(
                        pf.ListItem(
                            prefix_para,
                            *cloned_context,
                            *each_item_content
                        )
                    )
                    each_item_content=[]

                #new_content.append(pf.Para())
                current_context_blocks = []
            else:
                current_context_blocks.append(elem)
        
        ordered_list_content=pf.OrderedList(*each_list_item_content)
        new_content.append(ordered_list_content)
        #doc=pf.Doc(*new_content)
        doc.content=new_content
        return doc


    def _process_file(self, file_path: str, output_file_path: str):
        """
        Procesa un único archivo Markdown, aplicando la transformación.
        """
        print(f"Procesando archivo: {os.path.basename(file_path)}...")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
            #original_content.encode('utf-8-sig').strip()

            # 1. Convertir el texto de entrada a un objeto Doc (AST)
            doc = pf.convert_text(
                original_content,
                input_format='markdown+mark',
                output_format='panflute',
                standalone=True,
                extra_args=['--wrap=none']
            )
            
            # 2. Ordenar el Doc en memoria
            doc=self.reorder_doc(doc)

            # 3. Convertir el objeto Doc modificado de vuelta a texto Markdown
            final_markdown_text = pf.convert_text(
                doc,
                input_format='panflute',
                output_format='markdown+mark',
                standalone=True,
                extra_args=['--wrap=none']
            )

            # 4. Escribir la cadena de texto resultante en el archivo
            with open(output_file_path, 'w', encoding='utf-8') as f:
                f.write(final_markdown_text)
            print(f" -> Archivo transformado exitosamente.")

        except Exception as e:
            print(f" -> ERROR procesando el archivo {os.path.basename(file_path)}: {e}")

    def run(self):
        tag_text = f"Convirtiendo md en {self.inputs_path.stem} a docx con pngs"
        tag = self.files_finder.get_process_tag(tag_text)
        print(tag)
        """
        Ejecuta el proceso de reestructuración para todos los archivos .md
        en la carpeta de origen.
        """
        if not self.inputs_path.is_dir():
            print(f"El directorio de origen '{self.inputs_path}' no fue encontrado.")
            print("El script no procesará ningún archivo.")
            return

        print(f"Iniciando proceso en la carpeta: '{self.inputs_path}'")
        markdown_files_found = False

        md_files = self.files_finder.get_files()

        for md_file in md_files:
            if md_file.stem.endswith("-modificado"):
                continue
            md_modified_file = md_file.parent / f'{md_file.stem}-modificado.md'
            docx_file = md_file.parent / f'{md_file.stem}.docx'
            docx_modified_file = md_file.parent / f'{md_modified_file.stem}.docx'

            markdown_files_found = True
            
            command = [
                "pandoc",
                str(md_file),
                "-o", str(docx_file),
                "--wrap=none",
                #f"--resource-path=.{os.pathsep}{self.inputs_path}"]
                f"--resource-path={self.inputs_path}"]

            flags_creation = 0
            if sys.platform == "win32":
                flags_creation = subprocess.CREATE_NO_WINDOW
            
            subprocess.run(
                command,
                cwd=str(self.files_finder.files_path.absolute()),
                env=os.environ.copy(),
                check=True,
                capture_output=True,
                text=True,
                creationflags = flags_creation,
                encoding='utf-8'
            )
            
            self.files_finder.file_exists(docx_file)
            
            docx_cleaner = DocxPostProcessor(
                target_font=self.target_font,
                target_font_size=self.target_font_size)
            docx_cleaner.apply_global_font(str(docx_file))

            docx_cleaner.apply_margins(str(docx_file), margin_cm=1.0)
            docx_cleaner.restore_original_image_sizes(
                str(docx_file),
                max_width_cm=self.max_img_size
            )
            # Aplicamos la limpieza al archivo docx recién creado
            docx_cleaner.remove_bullets_keep_indent(str(docx_file))
            #Convertir opciones A. B. C. a lista real
            docx_cleaner.convert_text_options_to_list(str(docx_file))

            # Se aplica los aumentos de tamaño de letra a los títulos.
            docx_cleaner.adjust_heading_sizes(str(docx_file))

            if self.reuse_stimulus:

                self._process_file(str(md_file),str(md_modified_file))

                command = [
                    "pandoc",
                    str(md_modified_file),
                    "-o",
                    str(docx_modified_file),
                    "--wrap=none",
                    #f"--resource-path=:{self.inputs_path}"]
                    f"--resource-path={self.inputs_path}"]
                
                subprocess.run(
                    command,
                    cwd=str(self.files_finder.files_path.absolute()),
                    env=os.environ.copy(),
                    check=True,
                    capture_output=True,
                    text=True,
                    creationflags = flags_creation,
                    encoding='utf-8'
                )
                
                self.files_finder.file_exists(docx_modified_file)
                docx_cleaner.apply_global_font(str(docx_modified_file))
                
                docx_cleaner.apply_margins(
                    str(docx_modified_file),
                    margin_cm=1.0
                )
                docx_cleaner.restore_original_image_sizes(
                    str(docx_modified_file),
                    max_width_cm=19.0
                )
                # Aplicamos la limpieza al archivo docx recién creado
                docx_cleaner.remove_bullets_keep_indent(str(docx_modified_file))
                #Convertir opciones A. B. C. a lista real
                docx_cleaner.convert_text_options_to_list(str(docx_modified_file))

                # Se aplica los aumentos de tamaño de letra a los títulos.
                docx_cleaner.adjust_heading_sizes(str(docx_file))
        
        if not markdown_files_found:
            print("No se encontraron archivos .md en la carpeta.")
            
        print("Proceso completado.")


if __name__ == '__main__':
    FOLDER = "Temporales"
    
    try:
        
        restructurer = MdQuizToDocxConverter(inputs_path=FOLDER,outputs_path=FOLDER)
        restructurer.run()
        
    except ImportError:
        print("\nERROR: La biblioteca 'panflute' no está instalada.")
        print("Por favor, ejecute: pip install panflute")
    except Exception as e:
        print(f"Ha ocurrido un error inesperado durante la ejecución: {e}")