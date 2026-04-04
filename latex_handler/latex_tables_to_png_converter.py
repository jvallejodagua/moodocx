# -*- coding: utf-8 -*-
# latex_tables_to_png_converter.py

import os
import re
import subprocess
import tempfile
import shutil
from pathlib import Path
import time
import platform
import hashlib
from pypdfium2 import PdfDocument, PdfPage
import PIL
from filesystem.files_finder import FilesInSubfolder
from filesystem.path_latex_windows import resolve_pdflatex_path

class Compilador_Tablas:
        # 1. Al instanciar la clase, le pasas tus argumentos extra
    def __init__(self, nombre_archivo_md, base_dir, eliminar_texto_ayuda):

        self.nombre_archivo = nombre_archivo_md.replace(" ", "")
        self.base_dir=base_dir
        self.contador_tablas = 1  # Llevamos la cuenta de cuántas tablas van
        self.eliminar_texto_ayuda=eliminar_texto_ayuda

    def parse_markdown_table_to_latex(self, md_table_str):
        """Traduce una tabla Markdown a código LaTeX standalone usando tabularx."""
        lines = md_table_str.strip().split('\n')
        if len(lines) < 2:
            return None

        # Extraer y limpiar celdas
        def clean_cells(line):
            import re
            line = line.strip()
            if line.startswith('|'): line = line[1:]
            if line.endswith('|'): line = line[:-1]
            
            cleaned_cells = []
            for cell in line.split('|'):
                cell = cell.strip()
                
                # 1. Separar bloques matemáticos, priorizando $$...$$ sobre $...$
                parts = re.split(r'(\$\$.*?\$\$|\$.*?\$)', cell)
                
                processed_parts = []
                for part in parts:
                    if part.startswith('$$') and part.endswith('$$'):
                        # Convertir $$...$$ a $\displaystyle ...$ para evitar desbordamientos en tabularx
                        inner_math = part[2:-2].strip()
                        processed_parts.append(f"$\\displaystyle {inner_math}$")
                    elif part.startswith('$') and part.endswith('$'):
                        # Es una ecuación en línea normal
                        processed_parts.append(part)
                    else:
                        # Es texto normal: aplicamos formato Markdown y escapes de LaTeX
                        txt = part.replace('%', '\\%')
                        
                        # Convertir Negrita
                        txt = re.sub(r'\*\*(.*?)\*\*', r'\\textbf{\1}', txt)
                        txt = re.sub(r'__(.*?)__', r'\\textbf{\1}', txt)
                        
                        # Convertir Cursiva
                        txt = re.sub(r'\*(.*?)\*', r'\\textit{\1}', txt)
                        txt = re.sub(r'_(?=\S)(.*?)(?<=\S)_', r'\\textit{\1}', txt)
                        
                        # Escapar símbolos de dólar sueltos y guiones bajos que no sean formato
                        txt = txt.replace('$', '\\$')
                        txt = re.sub(r'(?<!\\)_', r'\\_', txt)
                        
                        processed_parts.append(txt)
                        
                cleaned_cells.append("".join(processed_parts))
                
            return cleaned_cells

        headers = clean_cells(lines[0])
        alignments_raw = clean_cells(lines[1])
        
        # Mapear alineaciones para usar columnas tipo 'X' de tabularx
        latex_aligns = []
        for align in alignments_raw:
            is_center = align.startswith(':') and align.endswith(':')
            is_right = align.endswith(':') and not is_center
            
            # El tipo de columna 'X' de tabularx ajusta automáticamente el ancho.
            # Le añadimos modificadores para mantener la alineación deseada.
            if is_center:
                col_fmt = r">{\centering\arraybackslash}X"
            elif is_right:
                col_fmt = r">{\raggedleft\arraybackslash}X"
            else:
                # Por defecto alineado a la izquierda
                col_fmt = r">{\raggedright\arraybackslash}X"
                
            latex_aligns.append(col_fmt)
        
        col_format = "|" + "|".join(latex_aligns) + "|"

        # Generación de la plantilla base LaTeX con "tabularx"
        latex_code = [
            r"\documentclass[border=2pt]{standalone}",
            r"\usepackage[utf8]{inputenc}",
            r"\usepackage[version=4]{mhchem}",
            r"\usepackage{array}",
            r"\usepackage{tabularx}",
            r"\usepackage{amsmath}",
            r"\begin{document}",
            r"{\Huge",
            # Iniciamos tabularx forzando el ancho objetivo de 30cm
            r"\begin{tabularx}{30cm}{" + col_format + "}",
            "\t" + r"\hline"
        ]
        
        bolded_headers = ["\\textbf{" + head + "}" for head in headers]

        # Encabezados
        latex_code.append("\t" + " & ".join(bolded_headers) + r" \\ \hline")
        
        # Datos
        for line in lines[2:]:
            if not line.strip(): continue
            cells = clean_cells(line)
            latex_code.append("\t" + " & ".join(cells) + r" \\ \hline")
            
        latex_code.append(r"\end{tabularx}")
        latex_code.append("}")
        latex_code.append(r"\end{document}")
        
        return "\n".join(latex_code)

    # 2. El método __call__ es lo que ejecutará re.sub
    def __call__(self, coincidencia):
        # 1. Recuperamos los grupos capturados
        texto_adjunto = coincidencia.group("texto_adjunto")
        tabla_markdown = coincidencia.group("tabla")
        texto_sufijo=coincidencia.group("texto_sufijo")

        # Crear subcarpeta de imágenes para este archivo
        img_dir_name = f"Imagenes-{self.nombre_archivo}"
        img_dir_path = self.base_dir / img_dir_name
        img_dir_path.mkdir(exist_ok=True)

        latex_code = self.parse_markdown_table_to_latex(tabla_markdown)
        if not latex_code:
            reemplazo = tabla_markdown
            return reemplazo
            
        img_filename = f"tabla_{self.contador_tablas}.png"
        final_img_path = img_dir_path / img_filename
        
        temp_path = self.base_dir / "compilados"
        temp_path.mkdir(exist_ok=True)

        tex_file = temp_path / "temp.tex"
        
        # 1. Escribir archivo .tex
        with open(tex_file, 'w', encoding='utf-8') as f:
            f.write(latex_code)
        
        time.sleep(3)
        # 2. Compilar con pdflatex
        print(f"  Compilando tabla {self.contador_tablas}...")
        try:
            if platform.system() == 'Windows':
                pdflatex_path = resolve_pdflatex_path()
            else:
                pdflatex_path = "/usr/local/texlive/2025/bin/x86_64-linux/pdflatex"
            
            subprocess.run(
                [pdflatex_path, '-interaction=nonstopmode', '-halt-on-error', '-file-line-error', 'temp.tex'],
                cwd=f"{temp_path}",
                env=os.environ.copy(),
                capture_output=True,
                text=True,
                encoding='utf-8',
                check=True
            )
            # subprocess.run(
            #     ['latexmk', '-xelatex', '-interaction=nonstopmode', 'temp.tex'],
            #     cwd=f"{temp_path}",
            #     capture_output=True, text=True, check=True
            # )
        except subprocess.CalledProcessError as e:
            print(f"  Error de LaTeX en la tabla {tabla_markdown}:")
            print(e.stdout) # Esto imprimirá el log de LaTeX
            print(e.stderr)
            reemplazo = tabla_markdown
            return reemplazo
        
        time.sleep(3)
        
        # 3. Convertir a PNG
        pdf_file = temp_path / "temp.pdf"
        
        if pdf_file.exists():
            print(f"  Convirtiendo PDF a PNG...")
            pdf_converter = PdfDocument(pdf_file)
            page_counter = len(pdf_converter)
            pdf_dpi = 72
            objective_dpi = 300
            resolution_scale_factor = objective_dpi/pdf_dpi
            base_name = "temp"

            generated_png = temp_path / f"{base_name}.png"

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
            
            # 4. Mover imagen a la carpeta destino
            if generated_png.exists():
                shutil.copy(generated_png, final_img_path)
                
                # 5. Sustituir en el texto Markdown
                if self.eliminar_texto_ayuda:
                    md_image_ref = f"![]({img_dir_name}/{img_filename})"
                else:
                    md_image_ref = f"![Tabla {self.contador_tablas}]({img_dir_name}/{img_filename})"
            else:
                print(f"  Error: No se pudo generar la imagen para la tabla {self.contador_tablas}.")
        else:
            print(f"  Error: La compilación de LaTeX falló para la tabla {self.contador_tablas}.")


        reemplazo = f"{texto_adjunto}{md_image_ref}{texto_sufijo}\n"
        self.contador_tablas += 1

        return reemplazo

class LaTeXTablesToPngConverter:

    def __init__(self,  eliminar_texto_ayuda, target_dir):
        self.eliminar_texto_ayuda=eliminar_texto_ayuda
        self.files_finder = FilesInSubfolder(
            route_to_subfolder = target_dir,
            suffix_extension = ".md")

    def set_eliminar_texto_ayuda(self, nuevo_estado):
        self.eliminar_texto_ayuda=nuevo_estado

    def run(self):
        base_dir = self.files_finder.files_path
        
        table_pattern = re.compile(
            r'^(?P<texto_adjunto>.*?)'                     # 1. Atrapa prefijos (como > o espacios)
            r'(?P<tabla>\|.*\|(?:[ \t]*\n^[ \t]*\|.*\|)*)' # 2. Atrapa TODAS las filas (de | a |)
            r'(?P<texto_sufijo>.*?)'                       # 3. Atrapa lo que haya después del último |
            r'[ \t]*(?:\n|$)',                             # 4. Consume espacios finales y el salto de línea
            re.MULTILINE
        )

        md_files = self.files_finder.get_files()

        for md_file in md_files:
            print(f"Procesando: {md_file.name}")
            
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            compilador = Compilador_Tablas(
                nombre_archivo_md = md_file.stem,
                base_dir = base_dir,
                eliminar_texto_ayuda = self.eliminar_texto_ayuda)

            nuevo_contenido = re.sub(table_pattern, compilador, content)

            # 6. Guardar cambios en el archivo MD
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(nuevo_contenido)
                
            print(f"Actualización completada para {md_file.name}\n")

if __name__ == "__main__":
    eliminar_texto_ayuda=True
    processor = LaTeXTablesToPngConverter(eliminar_texto_ayuda)
    processor.run()