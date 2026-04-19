# -*- coding: utf-8 -*-
# docx_to_md_converter.py

"""
Script para convertir archivos .docx a Markdown (.md) utilizando Pandoc.

Este módulo define una clase reutilizable que localiza todos los archivos .docx
en un directorio específico y ejecuta el comando de conversión de Pandoc para cada uno.

Requisitos:
- Python 3.6+
- Pandoc debe estar instalado y accesible en el PATH del sistema.
  (Puedes verificarlo ejecutando 'pandoc --version' en tu terminal).
"""

import subprocess
import os
import sys
from pathlib import Path
from typing import List
from filesystem.files_finder import FilesInSubfolder
import time

# Clase principal
class DocxToMdConverter:
    """
    Una clase para convertir todos los archivos .docx de un directorio a Markdown.

    Encapsula la lógica para encontrar archivos, construir y ejecutar los comandos
    de Pandoc, y manejar los posibles errores durante el proceso.
    """

    def __init__(self, inputs_path: Path):
        
        self.files_finder = FilesInSubfolder(
            files_path = inputs_path,
            suffix_extension = ".docx",
        )
        
    def create_media_directory(self, media_folder: str) -> None:
        media_folder_path = self.files_finder.files_path / media_folder
        media_folder_path.mkdir(exist_ok=True)

    def build_pandoc_command(self, input_file: str, output_file: str, media_folder: str) -> list[str]:
        return[
            "pandoc",
            input_file,
            "-o",
            output_file,
            f"--extract-media={media_folder}",
            "--wrap=none"
        ]

    def execute_pandoc_process(self, command: list[str]) -> None:
        flags_creation = 0
        if sys.platform == "win32":
            flags_creation = subprocess.CREATE_NO_WINDOW
        
        subprocess.run(
            command,
            cwd = str(self.files_finder.files_path.absolute()),
            env = os.environ.copy(),
            check = True,
            capture_output = True,
            text = True,
            creationflags = flags_creation,
            encoding = 'utf-8'
        )

    def run(self) -> None:
        """
        Orquesta el proceso de conversión para todos los archivos .docx encontrados.
        """
        tag_text = "Conversión de Docx a Markdown"
        tag = self.files_finder.get_process_tag(tag_text)
        print(tag)
        print(f"Directorio de trabajo: {self.files_finder.files_path}")

        docx_files_to_convert = self.files_finder.get_files()
        
        if not docx_files_to_convert:
            return

        success_count = 0
        error_count = 0

        for docx_file in docx_files_to_convert:

            md_file = docx_file.with_suffix(".md")
            
            print(f"\nProcesando: '{docx_file.name}' -> '{md_file.name}'")

            stem_no_space = self.files_finder.make_no_space_stem(docx_file)
            media_dir_path = f"Imagenes-{stem_no_space}"
            
            self.create_media_directory(media_dir_path)
            
            command = self.build_pandoc_command(
                docx_file,
                md_file,
                media_dir_path)

            try:
                result = self.execute_pandoc_process(command)
                if self.files_finder.file_exists(md_file):
                    print(f"  -> ÉXITO: Archivo '{md_file.name}' creado correctamente.")
                    success_count += 1
                

            except FileNotFoundError:
                print("\nERROR CRÍTICO: El comando 'pandoc' no se encontró.")
                print("Por favor, asegúrate de que Pandoc esté instalado y en el PATH de tu sistema.")
                return
            
            except subprocess.CalledProcessError as e:
                print(f"  -> ERROR: Falló la conversión de '{docx_file.name}'.")
                print(f"     Salida de error de Pandoc: {e.stderr.strip()}")
                error_count += 1
        
        print("\n--- Resumen de la conversión ---")
        print(f"Archivos convertidos con éxito: {success_count}")
        print(f"Archivos con errores: {error_count}")


# --- Punto de entrada del Script ---
if __name__ == "__main__":
    SOURCE_FOLDER = "Temporales"
    
    try:
        converter = DocxToMdConverter(SOURCE_FOLDER)
        converter.run()
        
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"Ha ocurrido un error inesperado: {e}")

    print("\nProceso finalizado.")