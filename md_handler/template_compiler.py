# -*- coding: utf-8 -*-
# template_compiler.py

import re
from typing import TypeAlias
import time
OrderList: TypeAlias = list[str]
from data_models.template_compiler_model import TemplateCompilerTask
from md_handler.formatter_abstract import FormatterAbstract
FunctionDict: TypeAlias = dict

class TemplateCompiler(FormatterAbstract):
    
    '''
    Sección para inicializar variables y ejecutar de modo automático
    '''
    def __init__(
        self,
        output_order: OrderList,
        transformations: TemplateCompilerTask | None = None
    ):
        super().__init__()
        self.output_order = output_order
        self.transformations = transformations
        self.groups = {}

    def execute_pipeline(self):
        if self.transformations:
            for config in self.transformations.functions:
                self.call_function(config)

    def call_function(self, config):
        
        function_name = config.function_name
        args = config.args
        kwargs = config.kwargs

        if hasattr(self, function_name):
            self.execute_function(function_name, *args, **kwargs)
        else:
            resultados[self.transformations.task_id] = f"Error: Función '{function_name}' no encontrada."

    def execute_function(self, function_name, *args, **kwargs):
        function = getattr(self, function_name)
        
        if callable(function):
            try:
                function(*args, **kwargs)
            except Exception as e:
                print(f"Error en ejecución: {str(e)}")
        else:
            print(f"Error: '{function_name}' no es llamable.")

    '''
    Funciones de proceso de grupos
    '''
    def upper_literals(self, *group_names):
        for group_name in group_names:
            literal = self.groups[group_name]
            
            self.groups[group_name] = literal.upper()

    def convert_marks_to_bold(self, *group_names):
        for group_name in group_names:
            paragraph = self.groups[group_name]
            marks_pattern = (
                rf'{self.bracket_mark}'
            )
            marks_regex = re.compile(marks_pattern)

            mark_to_bold_pattern = r'**\1**'
            self.groups[group_name] = marks_regex.sub(mark_to_bold_pattern, paragraph)

    def tabulate_paragraph(self, *group_names):
        for group_name in group_names:
            paragraph = self.groups[group_name]
            line_pattern = r'(?P<line>^.+$)'
            line_regex = re.compile(line_pattern, re.MULTILINE)
            tabbed_line_pattern = r'\t\g<line>'
            self.groups[group_name] = line_regex.sub(tabbed_line_pattern, paragraph)

    '''
    Funciones auxiliares de la clase
    '''
    def get_groups(self, match):
        self.groups = match.groupdict()
    
    def get_output(self, order_list: OrderList) -> str:
        output_text=""
        for item in order_list:
            if item in self.groups.keys():
                output_text += self.groups[item]
            else:
                output_text += item
        
        return output_text
    '''
    Función que se espera sea llamada por re.sub
    '''
    def __call__(self, match):
        self.get_groups(match)
        self.execute_pipeline()
        
        formatted_string = self.get_output(self.output_order)
        return formatted_string
