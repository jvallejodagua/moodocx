# -*- coding: utf-8 -*-
# moodocx.py

import flet as ft
import time
import threading
import asyncio
import sys
from pathlib import Path
import traceback
from pandoc_handler.docx_to_md_converter import DocxToMdConverter
from pandoc_handler.md_quiz_to_docx_converter import MdQuizToDocxConverter
from latex_handler.latex_formulas_to_png_converter import LaTeXFormulasToPngConverter
from latex_handler.latex_tables_to_png_converter import LaTeXTablesToPngConverter
from xml_handler.pydantic_to_moodle_xml_converter import PydanticToMoodleXmlConverter
from md_handler.md_formatter_processor import SequenceFormatterProcessor

class Moodocx:
    """
    Clase que gestiona la interfaz de usuario para la conversión de documentos.
    Diseñada para ser instanciada y agregada a cualquier página de Flet, 
    haciéndola reutilizable en proyectos más grandes.
    """
    def __init__(self, page: ft.Page, width):
        self.page = page
        self.page.title = "Moodocx V1.0.0"
        self.title_1 = "Moodocx"
        self.title_2 = "Transforma tus documentos"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 10
        self.page_width = width
        
        # Se define un estilo de letra grande para cumplir con el diseño minimalista
        self.estilo_texto = ft.TextStyle(size = 22)
        
        # Operaciones de archivos
        self.chk_word = ft.Checkbox(
            label = "Docx (ecuaciones) a markdown",
            value = True,
            label_style = self.estilo_texto,
        )

        self.chk_tablas = ft.Checkbox(
            label = "Transformar tablas",
            value = True,
            label_style = self.estilo_texto,
        )

        self.chk_ecuaciones = ft.Checkbox(
            label = "Transformar ecuaciones",
            value = True,
            label_style = self.estilo_texto,
        )
        
        self.chk_markdown = ft.Checkbox(
            label = "Markdown a Docx (png)",
            value = True,
            label_style = self.estilo_texto,
        )

        self.chk_moodle = ft.Checkbox(
            label = "Docx a Moodle (xml)",
            value = False,
            label_style = self.estilo_texto,
        )

        self.chk_formato_markdown = ft.Checkbox(
            label = "Formatear markdown de Docx",
            value = True,
            label_style = self.estilo_texto,
        )

        self.chk_texto_ayuda = ft.Checkbox(
            label = "Quitar etiqueta de tablas",
            value = True,
            label_style = self.estilo_texto,
        )

        self.chk_reutilizar_estimulo = ft.Checkbox(
            label = "Generar reutlización de estímulo",
            value = False,
            label_style = self.estilo_texto,
        )

        # 2. Barra de progreso y texto informativo (ocultos hasta que inicie la ejecución)
        self.progreso = ft.ProgressBar(
            width = self.page_width - 10*self.page.padding,
            value = 0,
            visible = True,
            color = ft.Colors.BLUE,
            bar_height = 10,
        )

        self.texto_estado = ft.Text(
            "             ",
            size = 20,
            visible = True,
        )
        
        # 3. Botón de ejecución
        self.btn_ejecutar = ft.FilledButton(
            content = "Ejecutar conversión", 
            on_click = self.procesar_scripts,
            style = ft.ButtonStyle(
                text_style = ft.TextStyle(size = 24, weight = ft.FontWeight.BOLD), 
                padding = 30
            )
        )


        self.temporals_path = self.get_self_path() / "Temporales"

        self.actualizar_clases()

    def actualizar_clases(self):
        
        self.procesador_word = DocxToMdConverter(source_directory = self.temporals_path)

        self.formateador_markdown = SequenceFormatterProcessor(source_directory = self.temporals_path)

        self.procesador_tablas = LaTeXTablesToPngConverter(
            self.chk_texto_ayuda.value,
            self.temporals_path)
        
        self.procesador_ecuaciones = LaTeXFormulasToPngConverter(target_directory = self.temporals_path)
        
        self.generador_word = MdQuizToDocxConverter(
            source_folder = self.temporals_path,
            destination_folder = self.temporals_path,
            reuse_stimulus_input = self.chk_reutilizar_estimulo.value,
        )

        self.generador_moodle = PydanticToMoodleXmlConverter(
            input_dir = self.temporals_path,
            output_dir = self.temporals_path)

    def get_self_path(self):

        if getattr(sys, 'frozen', False):
            self_path = Path(sys.executable).resolve().parent.absolute()
        else:
            self_path = Path(__file__).resolve().parent.absolute()
            
        return self_path

    def obtener_vista(self):
        """
        Retorna el contenedor principal con todos los elementos de la UI.
        Útil para inyectar este componente en otras vistas.
        """

        self.title_font = 32
        self.subtitle_font = 20

        lista_ui_operaciones_archivos=[
            ft.Text(
                "Operaciones de archivos",
                size = self.subtitle_font,
                weight = ft.FontWeight.BOLD
            ),
            self.chk_word,
            self.chk_tablas,
            self.chk_ecuaciones,
            self.chk_markdown,
            self.chk_moodle,
        ]

        columna_operaciones_archivos = ft.Column(
            controls = lista_ui_operaciones_archivos,
        )

        lista_ui_opciones_adicionales = [
            ft.Text(
                "Opciones adicionales",
                size = self.subtitle_font,
                weight = ft.FontWeight.BOLD
            ),
            self.chk_formato_markdown,
            self.chk_texto_ayuda,
            self.chk_reutilizar_estimulo,
        ]

        columna_opciones_adicionales = ft.Column(
            controls = lista_ui_opciones_adicionales,
            alignment = ft.MainAxisAlignment.START,
        )

        etiqueta_principal1 = ft.Text(
            self.title_1,
            size = self.title_font,
            weight = ft.FontWeight.BOLD,
            text_align = ft.TextAlign.CENTER,
        )

        etiqueta_principal2 = ft.Text(
            self.title_2,
            size = self.title_font,
            weight = ft.FontWeight.BOLD,
            text_align = ft.TextAlign.CENTER,
        )

        columna_titulo = ft.Column(
            controls = [
                ft.Divider(height = 5, color = "transparent"),
                etiqueta_principal1,
                etiqueta_principal2,
                ft.Divider(height = 5, color = "transparent"),
            ],
            alignment = ft.MainAxisAlignment.CENTER,
            horizontal_alignment = ft.CrossAxisAlignment.CENTER,
            spacing = 1,
        )

        fila_central = ft.Row(
            controls = [
                columna_operaciones_archivos,
                columna_opciones_adicionales,
            ],
            alignment = ft.MainAxisAlignment.CENTER,
            vertical_alignment = ft.CrossAxisAlignment.START,
            spacing = 50,
            #expand=True,
        )

        columna_inferior = ft.Column(
            controls = [
                ft.Divider(height = 5, color = "transparent"),
                self.progreso,                
                self.texto_estado,
                self.btn_ejecutar,
            ],
            alignment = ft.MainAxisAlignment.CENTER,
            horizontal_alignment = ft.CrossAxisAlignment.CENTER,
        )

        columna_general = ft.Column(
            controls = [
                columna_titulo,
                fila_central,
                columna_inferior,
            ],
            spacing = 15,
            alignment = ft.MainAxisAlignment.CENTER,
            horizontal_alignment = ft.CrossAxisAlignment.CENTER,
            #expand = True,
        )

        return columna_general

    def actualizar_scripts_ejecutar(self):
        scripts_para_proceso = []

        self.actualizar_clases()

        if self.chk_word.value:
            scripts_para_proceso.append(("Convirtiendo a markdown...", self.procesador_word))

        if self.chk_formato_markdown.value:
            scripts_para_proceso.append(("Formateando los markdown...", self.formateador_markdown))

        if self.chk_tablas.value:
            self.procesador_tablas.set_eliminar_texto_ayuda(self.chk_texto_ayuda.value)
            scripts_para_proceso.append(("Transformando tablas...", self.procesador_tablas))

        if self.chk_ecuaciones.value:
            scripts_para_proceso.append(("Transformando ecuaciones...", self.procesador_ecuaciones))
            
        if self.chk_markdown.value:
            scripts_para_proceso.append(("Convirtiendo a docx...", self.generador_word))

        if self.chk_moodle.value:
            scripts_para_proceso.append(("Convirtiendo a xml moodle...", self.generador_moodle))
        
        return scripts_para_proceso

    # Función para procesar los markdown
    async def procesar_scripts(self, e):
        """
        Evalúa las casillas seleccionadas, ejecuta las clases correspondientes 
        y actualiza la barra de progreso en función de la cantidad de scripts.
        """

        # Deshabilitamos el botón y mostramos la UI
        self.btn_ejecutar.disabled = True
        self.progreso.visible = True
        self.texto_estado.visible = True
        self.progreso.value = 0 
        self.page.update()

        scripts_a_ejecutar = self.actualizar_scripts_ejecutar()

        total_scripts = len(scripts_a_ejecutar)

        if total_scripts == 0:
            self.texto_estado.value = "Ninguna opción seleccionada."
            self.progreso.visible = False
            self.btn_ejecutar.disabled = False
            self.page.update()
            return

        for indice, (mensaje, clase_instanciada) in enumerate(scripts_a_ejecutar):
            self.texto_estado.value = f"Paso {indice + 1} de {total_scripts}: {mensaje}"
            self.page.update()
            
            # Instante para mejorar la ux
            await asyncio.sleep(0.1)
            
            try:
                # Delegación asíncrona:
                await asyncio.to_thread(clase_instanciada.run) 
            except Exception as error:
                self.texto_estado.value = f"Error en la ejecución: {error}"
                traceback.print_exc() 
                self.texto_estado.color = ft.Colors.RED
                self.btn_ejecutar.disabled = False
                self.page.update()
                return 
            
            porcentaje_completado = (indice + 1) / total_scripts
            self.progreso.value = porcentaje_completado
            self.page.update()
            
            await asyncio.sleep(0.1)

        self.texto_estado.value = "¡Todas las conversiones finalizaron con éxito!"
        self.texto_estado.color = ft.Colors.GREEN
        self.btn_ejecutar.disabled = False
        self.page.update()


# Función de entrada principal para Flet
def main(page: ft.Page):

    page.window.resizable = True
    page_width = 900
    app = Moodocx(page, page_width)
    page.window.width = page_width
    page.window.height = page_width*0.7
    
    page.add(app.obtener_vista())


if __name__ == "__main__":
    # Inicia la aplicación en modo ventana de escritorio
    ft.run(main=main)