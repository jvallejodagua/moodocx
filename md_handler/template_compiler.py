import re
from typing import TypeAlias
RegexStr: TypeAlias = str
#from data_models.template_compiler_model import TemplateCompilerTask
FunctionDict: TypeAlias = dict

class TemplateCompiler:
    
    '''
    Sección para inicializar variables y ejecutar de modo automático
    '''
    def __init__(self, output_regex: RegexStr, transformations: TemplateCompilerTask):
        self.output_regex = RegexStr
        self.transformations = transformations
        self.groups = {}

    def execute_pipeline(self):
        
        for config in self.transformations.functions:
            call_function(config)

    def call_function(self, config):

        function_name = config.function_name
        args = config.args
        kwargs = config.kwargs

        if hasattr(self, function_name):
            execute_function(self.task_id, function_name, args, kwargs)
        else:
            resultados[self.task_id] = f"Error: Función '{function_name}' no encontrada."

    def execute_function(self, function_name, *args, **kwargs):
        function = getattr(self, function_name)
        
        if callable(function):
            try:
                print(f"[Ejecutando] Tarea: {self.transformations.task_id} -> Método: {function_name}()")
                function(*args, **kwargs)
            except Exception as e:
                print(f"Error en ejecución: {str(e)}")
        else:
            print(f"Error: '{function_name}' no es llamable.")

    def tabulate_paragraph(self, group_name):
        paragraph = self.groups[group_name]
        line_pattern = r'(?P<line>^.+$)'
        line_regex = re.compile(line_pattern, re.MULTILINE)
        tabbed_line_pattern = r'\t\g<line>'
        self.groups[group_name] = line_regex.sub(tabbed_line_pattern, paragraph)
    
    def get_groups(self, match):
        self.groups = match.groupdict()
    '''
    Función que se espera sea llamada por re.sub
    '''
    def __call__(self, match):
        self.get_groups(match)
        self.execute_pipeline()

        formatted_string = match.expand(self.output_regex)
        return formatted_string
