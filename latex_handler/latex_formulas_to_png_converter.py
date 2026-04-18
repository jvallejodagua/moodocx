# -*- coding: utf-8 -*-
# latex_formulas_to_png_converter.py

import os
import sys
import re
import subprocess
import tempfile
import shutil
import hashlib
import platform
from pathlib import Path
import time
from pypdfium2 import PdfDocument, PdfPage
import PIL
from filesystem.files_finder import FilesInSubfolder
from filesystem.path_latex_windows import resolve_pdflatex_path

class LaTeXFormulasToPngConverter:
    """
    Clase para procesar archivos Markdown, detectando fórmulas LaTeX (inline y bloque)
    y convirtiéndolas en imágenes PNG mediante el compilador nativo de LaTeX (latexmk)
    y pypdfium2, reemplazando el texto original por referencias a las imágenes.
    """

    def __init__(self, inputs_path: Path):
        """
        Inicializa el procesador de ecuaciones.

        Args:
            inputs_path (str): Ruta del directorio que contiene los archivos .md.
            image_subfolder (str): Nombre de la subcarpeta donde se guardarán las imágenes generadas.
        """
        self.inputs_path = inputs_path
        self.files_finder = FilesInSubfolder(
            files_path = self.inputs_path,
            suffix_extension = ".md"
        )
        self.images_prefix = self.files_finder.images_prefix
        
        # Configurar rutas de binarios según el sistema operativo
        if platform.system() == 'Windows':
            self.pdflatex_path = resolve_pdflatex_path()
        else:
            self.pdflatex_path = "/usr/local/texlive/2025/bin/x86_64-linux/pdflatex"
        #print(self.pdflatex_path)

    def _generate_filename(self, latex_str: str) -> str:
        """Genera un nombre de archivo único basado en el hash del contenido LaTeX."""
        return hashlib.md5(latex_str.encode('utf-8')).hexdigest() + ".png"

    def _create_latex_document(self, latex_code: str, delimiter: str) -> str:
        """
        Crea el documento LaTeX standalone para renderizar la ecuación de manera aislada.
        Maneja tanto ecuaciones en línea ($) como en bloque ($$).
        """
        # Se utiliza varwidth para ajustar el ancho automáticamente sin desbordar
        latex_template = [
            r"\documentclass[border=2pt]{standalone}",
            r"\usepackage[utf8]{inputenc}",
            r"\usepackage[version=4]{mhchem}",
            r"\usepackage{amsmath}",
            r"\usepackage{amssymb}",
            r"\usepackage{amsfonts}",
            r"\usepackage{physics}",
            r"\usepackage{siunitx}",
            r"\usepackage{xcolor}",
            r"\pagecolor{white}",
            r"\begin{document}",            r"\normalsize",
            f"{delimiter}{latex_code}{delimiter}",
            r"\end{document}"
        ]
        return "\n".join(latex_template)

    def _compile_to_png(self, latex_document: str, output_image_path: Path):
        """
        Escribe el código en un archivo temporal, lo compila con latexmk 
        y lo convierte a PNG usando pypdfium2.
        """
        temp_dir = self.files_finder.compile_path
        
        tex_file = temp_dir / "temp.tex"
        pdf_file = temp_dir / "temp.pdf"
        base_name = "temp"

        # 1. Escribir archivo .tex temporal
        with open(tex_file, 'w', encoding='utf-8') as f:
            f.write(latex_document)
        
        # 2. Compilar con latexmk (Genera PDF)
        try:
            #print(self.pdflatex_path, '-pdf', '-interaction=nonstopmode', f'{base_name}.tex')

            flags_creation = 0
            if sys.platform == "win32":
                flags_creation = subprocess.CREATE_NO_WINDOW

            subprocess.run(
                [self.pdflatex_path, '-interaction=nonstopmode', '-halt-on-error', '-file-line-error', f'{base_name}.tex'],
                cwd=str(temp_dir),
                env=os.environ.copy(),
                check=True,
                capture_output=True,
                text=True,
                creationflags = flags_creation,
                encoding = 'utf-8'
            )
        except subprocess.CalledProcessError as e:
            print(f"  [!] Error de compilación LaTeX:\n{e.stderr}")
            return False
        
        #print(pdf_file.exists)
        # 3. Convertir PDF a PNG con pypdfium2
        if self.files_finder.file_exists(pdf_file):
            
            pdf_converter = PdfDocument(pdf_file)
            page_counter = len(pdf_converter)
            pdf_dpi = 72
            objective_dpi = 300
            resolution_scale_factor = objective_dpi/pdf_dpi

            generated_png = temp_dir / f"{base_name}.png"

            for page_index in range(page_counter):
                page_instance = pdf_converter.get_page(page_index)
                
                bitmap_rasterized = page_instance.render(
                    scale=resolution_scale_factor,
                    rotation=0,
                    crop=(0, 0, 0, 0),
                    fill_color=[255, 255, 255, 255],
                    draw_annots=True,
                    grayscale=False,
                    optimize_mode=None,
                )
                
                pil_bitmap = bitmap_rasterized.to_pil()

                pil_bitmap.save(
                    generated_png,
                    format="PNG",
                    dpi=(objective_dpi,objective_dpi),
                )

            # 4. Mover la imagen generada a la ruta final
            if generated_png.exists():
                shutil.copy(generated_png, output_image_path)
                return True
            else:
                print("  [!] Error: pypdfium2 no generó la imagen PNG.")
                return False
        else:
            print("  [!] Error: No se generó el archivo PDF.")
            return False

    def process_file(self, file_path: Path):
        """
        Lee un archivo Markdown, detecta las ecuaciones, invoca la compilación
        y actualiza el archivo con los enlaces a las imágenes generadas.
        """
        print(f"Procesando archivo: {file_path.name}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Regex para capturar tanto ecuaciones inline ($...$) como en bloque ($$...$$)
        latex_pattern = re.compile(r'(\$\$?)(.+?)\1', re.DOTALL)
        
        no_space_stem = self.files_finder.make_no_space_stem(file_path)
        img_dir_name = f"{self.images_prefix}-{no_space_stem}"
        img_dir = file_path.parent / img_dir_name
        img_dir.mkdir(exist_ok=True)

        def replacement_func(match):
            #Se cambia el delimitador porque standalone no soporta los dobles
            delimiter = match.group(1)
            if delimiter=="$$":
                delimiter="$"
            latex_code = match.group(2).strip()
            
            if not latex_code:
                return match.group(0)

            img_filename = self._generate_filename(latex_code)
            img_full_path = img_dir / img_filename
            
            # Generar la imagen si no existe previamente en caché
            if not img_full_path.exists():
                print(f"  -> Compilando ecuación: {latex_code[:30]}...")
                latex_doc = self._create_latex_document(latex_code, delimiter)
                success = self._compile_to_png(latex_doc, img_full_path)
                
                if not success:
                    print("  -> Omitiendo reemplazo por fallo en compilación.")
                    return match.group(0) # Retorna el texto original si falla
            
            # Formatear ruta relativa para el Markdown
            relative_path = f"{img_dir_name}/{img_filename}"
            return f"![Ecuación]({relative_path})"

        # Sustituir todas las coincidencias
        new_content = latex_pattern.sub(replacement_func, content)

        # Sobrescribir archivo solo si hubo modificaciones
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"  [OK] Archivo actualizado: {file_path.name}\n")
        else:
            print("  [-] Sin cambios detectados.\n")

    def run(self):
        input_name = self.files_finder.files_path.stem
        tag_text = f"Convirtiendo fórmulas latex a png en {input_name}"
        tag = self.files_finder.get_process_tag(tag_text)
        print(tag)

        inputs_path = self.files_finder.files_path
      
        md_files = self.files_finder.get_files()
        
        if not md_files:
            print("No se encontraron archivos .md en el directorio objetivo.")
            return

        for md_file in md_files:
            self.process_file(md_file)
        
        print("Procesamiento de ecuaciones finalizado con éxito.")

# --- Bloque de Ejecución Principal ---
if __name__ == "__main__":
    procesador = LaTeXFormulasToPngConverter(inputs_path="_Entradas")
    procesador.run()