# -*- coding: utf-8 -*-
# latex_formulas_to_png_converter.py

import os
import re
import subprocess
import tempfile
import shutil
import hashlib
import platform
from pathlib import Path
import time
from filesystem.files_finder import FilesInSubfolder
from filesystem.path_latex_windows import resolve_pdflatex_path

class LaTeXFormulasToPngConverter:
    """
    Clase para procesar archivos Markdown, detectando fórmulas LaTeX (inline y bloque)
    y convirtiéndolas en imágenes PNG mediante el compilador nativo de LaTeX (latexmk)
    y pdftocairo, reemplazando el texto original por referencias a las imágenes.
    """

    def __init__(self, target_directory: str, image_subfolder: str = "Imagenes"):
        """
        Inicializa el procesador de ecuaciones.

        Args:
            target_directory (str): Ruta del directorio que contiene los archivos .md.
            image_subfolder (str): Nombre de la subcarpeta donde se guardarán las imágenes generadas.
        """
        self.target_dir = Path(target_directory)
        self.target_dir = self.target_dir.absolute()
        self.files_finder = FilesInSubfolder(self.target_dir,".md")
        self.img_folder_name = image_subfolder
        
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
            r"\begin{document}",
            r"\normalsize",
            f"{delimiter}{latex_code}{delimiter}",
            r"\end{document}"
        ]
        return "\n".join(latex_template)

    def _compile_to_png(self, latex_document: str, output_image_path: Path):
        """
        Escribe el código en un archivo temporal, lo compila con latexmk 
        y lo convierte a PNG usando pdftocairo.
        """
        temp_dir = self.target_dir / "compilados"
        temp_dir.mkdir(exist_ok=True)
        
        tex_file = temp_dir / "temp.tex"
        pdf_file = temp_dir / "temp.pdf"
        base_name = "temp"

        # 1. Escribir archivo .tex temporal
        with open(tex_file, 'w', encoding='utf-8') as f:
            f.write(latex_document)
        
        time.sleep(2)
        #print(temp_dir)
        # 2. Compilar con latexmk (Genera PDF)
        try:
            #print(self.pdflatex_path, '-pdf', '-interaction=nonstopmode', f'{base_name}.tex')
            subprocess.run(
                [self.pdflatex_path, '-interaction=nonstopmode', '-halt-on-error', '-file-line-error', f'{base_name}.tex'],
                cwd=str(temp_dir),
                env=os.environ.copy(),
                capture_output=True,
                text=True,
                check=True
            )
        except subprocess.CalledProcessError as e:
            print(f"  [!] Error de compilación LaTeX:\n{e.stderr}")
            return False
        time.sleep(2)
        #print(pdf_file.exists)
        # 3. Convertir PDF a PNG con pdftocairo
        if pdf_file.exists():
            subprocess.run(
                ['pdftocairo', '-png', '-singlefile', '-r', '300', f'{base_name}.pdf', base_name],
                cwd=str(temp_dir),
                check=False
            )
            
            generated_png = temp_dir / f"{base_name}.png"
            
            # 4. Mover la imagen generada a la ruta final
            if generated_png.exists():
                shutil.copy(generated_png, output_image_path)
                return True
            else:
                print("  [!] Error: pdftocairo no generó la imagen PNG.")
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
        
        # Crear subcarpeta de imágenes para este archivo
        img_dir_name = f"{self.img_folder_name}-{file_path.stem}"
        img_dir_name=img_dir_name.replace(" ","")
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
        
        md_files = self.files_finder.get_files()
        
        if not md_files:
            print("No se encontraron archivos .md en el directorio objetivo.")
            return

        for md_file in md_files:
            self.process_file(md_file)
        
        print("Procesamiento de ecuaciones finalizado con éxito.")


# --- Bloque de Ejecución Principal ---
if __name__ == "__main__":
    procesador = LaTeXFormulasToPngConverter(target_directory="Temporales")
    procesador.run()