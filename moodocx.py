# -*- coding: utf-8 -*-
# moodocx.py

import flet as ft
import time
import threading
import asyncio
import sys
import json
from pathlib import Path
import traceback
from pandoc_handler.docx_to_md_converter import DocxToMdConverter
from pandoc_handler.md_quiz_to_docx_converter import MdQuizToDocxConverter
from latex_handler.latex_formulas_to_png_converter import LaTeXFormulasToPngConverter
from latex_handler.latex_tables_to_png_converter import LaTeXTablesToPngConverter
from xml_handler.pydantic_to_moodle_xml_converter import PydanticToMoodleXmlConverter
from md_handler.md_formatter_processor import MdFormatterProcessor
from filesystem.files_finder import FilesManager, SimpleLogger, FolderCleaner

class Moodocx:
    """
    Clase que gestiona la interfaz de usuario para la conversión de documentos.
    Diseñada para ser instanciada y agregada a cualquier página de Flet, 
    haciéndola reutilizable en proyectos más grandes.
    """
    def __init__(self, page: ft.Page, width):
        self.page = page
        self.page.title = "Moodocx V1.1.5"
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

        self.max_ancho_imagen = ft.TextField(
            label="Máximo ancho de las imágenes [cm]", 
            multiline=True, 
            min_lines=1, 
            max_lines=8,
            expand=False,
            text_style=self.estilo_texto,
            border_radius=10,
            label_style=self.estilo_texto,
            value="17.5",
        )

        self.chk_reutilizar_estimulo = ft.Checkbox(
            label = "Generar reutlización de estímulo",
            value = False,
            label_style = self.estilo_texto,
        )
        
        self.fuente_selector = ft.Dropdown(
            label = "Seleccione la fuente",
            label_style = self.estilo_texto,
            text_style = self.estilo_texto,
            expand=True)
        
        self.fuente_selector.options = [
            ft.DropdownOption(
				text = "Liberation Serif",
				style = ft.ButtonStyle(text_style=self.estilo_texto)),
            ft.DropdownOption(
				text = "Liberation Sans",
				style = ft.ButtonStyle(text_style=self.estilo_texto)),
            ft.DropdownOption(
				text = "Liberation Mono",
				style = ft.ButtonStyle(text_style=self.estilo_texto)),
            ft.DropdownOption(
				text = "Carlito",
				style = ft.ButtonStyle(text_style=self.estilo_texto)),
            ft.DropdownOption(
				text = "Caladea",
				style = ft.ButtonStyle(text_style=self.estilo_texto)),
        ]

        self.fuente_selector.value="Liberation Serif"

        self.altura_letra_selector = ft.Dropdown(
            label = "Seleccione el tamaño de la fuente",
            label_style = self.estilo_texto,
            text_style = self.estilo_texto,
            expand=True)
        
        self.altura_letra_selector.options = [
            ft.DropdownOption(
				text = "8",
				style = ft.ButtonStyle(text_style=self.estilo_texto)),
            ft.DropdownOption(
				text = "10",
				style = ft.ButtonStyle(text_style=self.estilo_texto)),
            ft.DropdownOption(
				text = "12",
				style = ft.ButtonStyle(text_style=self.estilo_texto)),
            ft.DropdownOption(
				text = "14",
				style = ft.ButtonStyle(text_style=self.estilo_texto)),
            ft.DropdownOption(
				text = "16",
				style = ft.ButtonStyle(text_style=self.estilo_texto)),
            ft.DropdownOption(
				text = "18",
				style = ft.ButtonStyle(text_style=self.estilo_texto)),
            ft.DropdownOption(
				text = "20",
				style = ft.ButtonStyle(text_style=self.estilo_texto)),
            ft.DropdownOption(
				text = "22",
				style = ft.ButtonStyle(text_style=self.estilo_texto)),
        ]

        self.altura_letra_selector.value="18"

        self.selector_proceso = ft.SegmentedButton(
            on_change=self.handle_selection_change,
            selected_icon=ft.Icon(ft.Icons.ADD_BOX_SHARP),
            selected=["formatear_word"],
            allow_empty_selection=True,
            allow_multiple_selection=True,
            style = ft.ButtonStyle(text_style=self.estilo_texto),
            segments=[
                ft.Segment(
                    value="formatear_word",
                    label=ft.Text("Formatear Word"),
                ),
                ft.Segment(
                    value="producir_moodle",
                    label=ft.Text("Producir Moodle"),
                ),
            ],
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
        
        self.files_checker = SimpleLogger()
        self.inputs_path = self.files_checker.resolve_user_folder_path("_Entradas")
        self.inputs_path.mkdir(exist_ok=True)
        self.outputs_path = self.files_checker.resolve_user_folder_path("_Salidas")
        self.outputs_path.mkdir(exist_ok=True)
        self.files_manager = FilesManager(self.inputs_path, self.outputs_path)
        self.files_manager.create_compile_dir()
        self.folder_cleaner = FolderCleaner()
        
        self.actualizar_clases()

    def handle_selection_change(self, evento_proceso: ft.Event[ft.SegmentedButton]):
        # 1. Obtenemos el texto crudo del evento tal y como lo envía Flet
        datos_crudos = str(evento_proceso.data)
        
        # 2. Búsqueda directa de subcadenas (Infalible sin importar si es Set, List o JSON)
        es_word = "formatear_word" in datos_crudos
        es_moodle = "producir_moodle" in datos_crudos
        
        # 3. Asignamos los valores booleanos al backend de cada componente
        self.chk_word.value = es_word
        self.chk_formato_markdown.value = es_word
        self.chk_ecuaciones.value = es_word
        self.chk_tablas.value = es_word
        self.chk_texto_ayuda.value = es_word
        self.chk_markdown.value = es_word
        
        self.chk_moodle.value = es_moodle
        
        # 4. Forzamos el renderizado directo de los componentes
        self.chk_word.update()
        self.chk_formato_markdown.update()
        self.chk_ecuaciones.update()
        self.chk_tablas.update()
        self.chk_texto_ayuda.update()
        self.chk_markdown.update()
        self.chk_moodle.update()
        
        evento_proceso.control.update()
        
        # Monitor de depuración corregido
        # print(f"Datos crudos recibidos: {datos_crudos}")
        # print(f"Estado real interpretado: Word={es_word}, Moodle={es_moodle}")

    def actualizar_clases(self):
        
        self.procesador_word = DocxToMdConverter(
            inputs_path = self.inputs_path
        )

        self.formateador_markdown = MdFormatterProcessor(
            inputs_path = self.inputs_path,
            outputs_path = self.outputs_path,
        )

        self.procesador_tablas = LaTeXTablesToPngConverter(
            inputs_path = self.outputs_path,
            delete_hint_flag = self.chk_texto_ayuda.value,
            font_size = int(self.altura_letra_selector.value),
            max_img_size = float(self.max_ancho_imagen.value),
        )
        
        self.procesador_ecuaciones = LaTeXFormulasToPngConverter(
            inputs_path = self.outputs_path,
            font_size = int(self.altura_letra_selector.value),
        )
        
        self.generador_word = MdQuizToDocxConverter(
            inputs_path = self.outputs_path,
            outputs_path = self.outputs_path,
            reuse_stimulus_input = self.chk_reutilizar_estimulo.value,
            target_font = self.fuente_selector.value,
            target_font_size = int(self.altura_letra_selector.value),
            max_img_size = float(self.max_ancho_imagen.value),
        )

        self.generador_moodle = PydanticToMoodleXmlConverter(
            inputs_path = self.outputs_path,
            outputs_path = self.outputs_path,
            font_size = int(self.altura_letra_selector.value))

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
        
        contenedor_max_ancho_imagen = ft.Container(
            content = self.max_ancho_imagen,
            padding = 10,
        )

        lista_ui_opciones_adicionales = [
            ft.Text(
                "Opciones adicionales",
                size = self.subtitle_font,
                weight = ft.FontWeight.BOLD
            ),
            self.chk_formato_markdown,
            self.chk_texto_ayuda,
            contenedor_max_ancho_imagen,
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

        area_segura = ft.SafeArea(self.selector_proceso)

        area_basica=ft.Column(
            [self.fuente_selector,
            self.altura_letra_selector,
            self.chk_reutilizar_estimulo,
            area_segura],
            scroll=ft.ScrollMode.AUTO,
            spacing=20,
            margin=10,
        )

        area_avanzada=ft.Column(
            [fila_central],
            scroll=ft.ScrollMode.AUTO, spacing=0,
        )

        tab_label_basica= ft.Tab(
            label="Básico",
        )

        tab_label_avanzada= ft.Tab(
            label="Avanzado"
        )

        ui_tabbar = ft.TabBar(
            tabs=[
                tab_label_basica,
                tab_label_avanzada,
            ],
            label_text_style= self.estilo_texto,
        )

        ui_tabview = ft.TabBarView(
            expand=True,
            controls=[
                ft.Container(content=area_basica),
                ft.Container(content=area_avanzada),
            ],
        )

        ui_column = ft.Column(
            expand=True,
            controls=[
                ui_tabbar,
                ui_tabview,
            ],
        )

        ui_tabs=ft.Tabs(
            selected_index=0,
            length=2,
            expand=True,
            content=ui_column
        )

        ui_area= ft.Container(
            content=ui_tabs,
            margin=0,
            padding=2,
            alignment=ft.Alignment.TOP_LEFT,
            bgcolor=ft.Colors.WHITE,
            #width=600,
            expand=True,
            #height=400,
            border_radius=10,
            border=ft.Border.all(3, ft.Colors.BLACK),
            ink=True,
        )

        columna_general = ft.Column(
            controls = [
                columna_titulo,
                ui_area,
                columna_inferior,
            ],
            spacing = 15,
            alignment = ft.MainAxisAlignment.CENTER,
            horizontal_alignment = ft.CrossAxisAlignment.CENTER,
            expand = True,
        )

        return columna_general

    def actualizar_scripts_ejecutar(self):
        scripts_para_proceso = []

        self.actualizar_clases()

        if self.chk_word.value:
            scripts_para_proceso.append(("Convirtiendo a markdown...", self.procesador_word))

        scripts_para_proceso.append(("Copiando los markdown...", self.files_manager))

        if self.chk_formato_markdown.value:
            scripts_para_proceso.append(("Formateando los markdown...", self.formateador_markdown))

        if self.chk_tablas.value:
            self.procesador_tablas.set_delete_hint_flag(self.chk_texto_ayuda.value)
            scripts_para_proceso.append(("Transformando tablas...", self.procesador_tablas))

        if self.chk_ecuaciones.value:
            scripts_para_proceso.append(("Transformando ecuaciones...", self.procesador_ecuaciones))
            
        if self.chk_markdown.value:
            scripts_para_proceso.append(("Convirtiendo a docx...", self.generador_word))

        if self.chk_moodle.value:
            scripts_para_proceso.append(("Convirtiendo a xml moodle...", self.generador_moodle))
        
        scripts_para_proceso.append(("Limpiando folder vacíos...", self.folder_cleaner))
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
    page.window.height = page_width*0.8
    
    page.add(app.obtener_vista())


if __name__ == "__main__":
    # Inicia la aplicación en modo ventana de escritorio
    ft.run(main=main)