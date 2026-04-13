import re
import sys
from pathlib import Path
from md_handler.formatter_abstract import FormatterAbstract
from md_handler.template_compiler import TemplateCompiler
#from template_compiler import TemplateCompiler
from data_models.template_compiler_model import TemplateCompilerTask, TemplateCompilerFunction

class TemplateFormatter(FormatterAbstract):

    def __init__(self, content):
        super().__init__()
        self.raw_text = content
        self.pattern_list = []
        self.question_regex = None

    # Conectores a las posibles entradas
    def build_single_line_pattern_list(self):
        for regex_id, pattern_value in self.single_line_pattern.items():
            self.pattern_list.append(self.build_group_simple_regex(regex_id, pattern_value))

    def build_multiline_pattern_list(self):
        for regex_id, pattern_value in self.multiline_pattern.items():
            self.pattern_list.append(self.build_group_atomic_regex(regex_id, pattern_value))

    def build_singleline_option_pattern_list(self):
        for regex_id, pattern_value in self.singleline_option_pattern.items():
            self.pattern_list.append(self.build_group_atomic_regex(regex_id, pattern_value))

    def build_regex(self):
        question_search_pattern = self.build_search_pattern(*self.pattern_list)
        self.question_regex = self.build_group_atomic_regex(
            "question",
            rf'{question_search_pattern}',
        )

    '''
    Auxiliary Functions
    '''
    def fix_single_aspect(self, input_pattern, ouput_pattern, content):

        fixed_content = ""
        input_pattern_regex = re.compile(input_pattern)
        
        fixed_content = input_pattern_regex.sub(ouput_pattern, content)

        return fixed_content
    
    '''
    Main Functions
    '''
    def reorder_singleline_quiz(self):
        self.build_single_line_pattern_list()
        self.build_regex()
        
        question_pattern = re.compile(self.question_regex, re.MULTILINE)
        quiz = question_pattern.sub(self.ouput_single_line_order, self.raw_text)
        
        return quiz

    def format_multiline_quiz(self):
        self.build_multiline_pattern_list()
        self.build_regex()
        
        question_pattern = re.compile(self.question_regex, flags=re.DOTALL)
        
        upper_literals =  TemplateCompilerFunction(
            function_name = "upper_literals",
            args = [
                self.literal_A_key,
                self.literal_B_key,
                self.literal_C_key,
                self.literal_D_key
            ]
        )

        delete_comment_marks = TemplateCompilerFunction(
            function_name = "delete_comment_marks",
            args = [
                self.added_prompt_text_key,
                self.added_option_A_key,
                self.added_option_B_key,
                self.added_option_C_key,
                self.added_option_D_key
            ]
        )

        delete_code_blocks = TemplateCompilerFunction(
            function_name = "delete_code_blocks",
            args = [
                self.added_prompt_text_key,
                self.added_option_A_key,
                self.added_option_B_key,
                self.added_option_C_key,
                self.added_option_D_key
            ]
        )

        convert_marks_to_bold = TemplateCompilerFunction(
            function_name = "convert_marks_to_bold",
            args = [
                self.option_A_key,
                self.option_B_key,
                self.option_C_key,
                self.option_D_key
            ]
        )
        
        tabulate_paragraphs = TemplateCompilerFunction(
            function_name = "tabulate_paragraph",
            args = [
                self.added_prompt_text_key,
                self.literal_A_key,
                self.added_option_A_key,
                self.literal_B_key,
                self.added_option_B_key,
                self.literal_C_key,
                self.added_option_C_key,
                self.literal_D_key,
                self.added_option_D_key
            ]
        )
        
        format_quiz = TemplateCompilerTask(
            task_id = "format_quiz",
            functions = [
                upper_literals,
                delete_comment_marks,
                delete_code_blocks,
                convert_marks_to_bold,
                tabulate_paragraphs
            ]
        )
        
        template_compiler = TemplateCompiler(
            output_order = self.output_multiline_list,
            transformations = format_quiz,
        )
        
        quiz_formatted = question_pattern.sub(template_compiler, self.raw_text)

        # This is an odd edge case
        # quiz_fixed_italic_marks = self.fix_single_aspect(
        #     self.worng_italic_mark,
        #     self.italic_mark,
        #     quiz_formatted)

        # quiz_fixed_bold_marks = self.fix_single_aspect(
        #     self.worng_bold_mark,
        #     self.bold_mark,
        #     quiz_fixed_italic_marks)

        quiz_fixed_soft_new_lines = self.fix_single_aspect(
            self.soft_new_line,
            self.simple_new_line,
            quiz_formatted)

        quiz_fixed_new_lines = self.fix_single_aspect(
            self.new_line,
            self.md_newline,
            quiz_fixed_soft_new_lines)


        quiz = quiz_fixed_new_lines

        return quiz
    
    def format_singleline_option_quiz(self):
        self.build_singleline_option_pattern_list()
        self.build_regex()
        question_pattern = re.compile(self.question_regex, flags=re.DOTALL)

        upper_literals =  TemplateCompilerFunction(
            function_name = "upper_literals",
            args = [
                self.literal_A_key,
                self.literal_B_key,
                self.literal_C_key,
                self.literal_D_key
            ]
        )

        delete_comment_marks = TemplateCompilerFunction(
            function_name = "delete_comment_marks",
            args = [
                self.added_prompt_text_key
            ]
        )

        delete_code_blocks = TemplateCompilerFunction(
            function_name = "delete_code_blocks",
            args = [
                self.added_prompt_text_key
            ]
        )

        convert_marks_to_bold = TemplateCompilerFunction(
            function_name = "convert_marks_to_bold",
            args = [
                self.option_A_key,
                self.option_B_key,
                self.option_C_key,
                self.option_D_key
            ]
        )
        
        tabulate_paragraphs = TemplateCompilerFunction(
            function_name = "tabulate_paragraph",
            args = [
                self.added_prompt_text_key,
                self.literal_A_key,
                self.literal_B_key,
                self.literal_C_key,
                self.literal_D_key,
            ]
        )
        
        format_quiz = TemplateCompilerTask(
            task_id = "format_quiz",
            functions = [
                upper_literals,
                delete_comment_marks,
                delete_code_blocks,
                convert_marks_to_bold,
                tabulate_paragraphs
            ]
        )
        
        template_compiler = TemplateCompiler(
            output_order = self.output_singleline_option_list,
            transformations = format_quiz,
        )
        
        quiz_formatted = question_pattern.sub(template_compiler, self.raw_text)

        quiz_fixed_soft_new_lines = self.fix_single_aspect(
            self.soft_new_line,
            self.simple_new_line,
            quiz_formatted)

        quiz_fixed_new_lines = self.fix_single_aspect(
            self.new_line,
            self.md_newline,
            quiz_fixed_soft_new_lines)


        quiz = quiz_fixed_new_lines

        return quiz

    '''
    Test functions
    '''
    def test_multiple_line_numerals(self):
        self.build_multiline_pattern_list()
        self.build_regex()
        
        question_pattern = re.compile(self.question_regex, re.DOTALL)
        quiz = question_pattern.sub(self.ouput_multiline_order, self.raw_text)
        
        return quiz

    def get_self_path(self):

        if getattr(sys, 'frozen', False):
            self_path = Path(sys.executable).resolve().parent.absolute()
        else:
            self_path = Path(__file__).resolve().parent.absolute()
            
        return self_path

if __name__ == "__main__":

    self_path = Path(__file__).resolve().parent.parent.absolute()
    tests_path = self_path / "Temporales"
    #print(tests_path)
    
    file_path = tests_path / "EF. TECNOLOGIA E INFORMÁTICA GRADO 7 2P 2025.md"

    content=""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    html_code = '<!-- -->'
    if html_code in content:
        content.replace(html_code,"empty_html_comment")

    regex_builder = TemplateFormatter(content)
    
    quiz = regex_builder.test_multiple_line_numerals()
    output_file_path = tests_path / "EvaluacionTransformada.md"
    with open(output_file_path, 'w', encoding='utf-8') as f2:
        f2.write(quiz)
    

    
