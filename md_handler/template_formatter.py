import re
import sys
from pathlib import Path
from md_handler.template_compiler import TemplateCompiler
#from template_compiler import TemplateCompiler
from data_models.template_compiler_model import TemplateCompilerTask, TemplateCompilerFunction

class TemplateFormatter:

    def __init__(self, content):
        self.raw_text = content
        self.pattern_list = []
        self.question_regex = None

        '''
        General regex
        '''
        self.numeral_character = r'\d+'
        self.space_character_but_new_line = r'[ \t\r\f\v]+'
        self.new_line = r'[\r?\n]+'
        self.punctuation_separator = r'[\.\)]'
        self.accent_mark = r'[*]*'
        self.literal_A_character = r'[aA]'
        self.literal_B_character = r'[bB]'
        self.literal_C_character = r'[cC]'
        self.literal_D_character = r'[dD]'
        self.one_line = r'[^\n]+'
        self.last_added_text = r'(.+?)?(?:<!-- -->)?'
        self.pandoc_comment = r'(?:\n<!-- -->)?|\z'
        
        self.output_punctuation = r'. '
        
        self.numeral_search_key = "numeral_search"
        self.punctuation_numeral_key = "punctuation_numeral"
        self.empty_space_numeral_key = "empty_space_numeral"
        self.accent_prompt_key = "accent_prompt"
        self.prompt_key = "prompt"
        self.added_prompt_text_key = "added_prompt_text"
        self.new_line_A_key = "literal_A_new_line"
        self.accent_mark_A_key = "accent_mark_A"
        self.literal_A_key = "literal_A"
        self.punctuation_separator_A_key = "punctuation_separator_A"
        self.empty_space_A_key = "empty_space_A"
        self.option_A_key = "option_A"
        self.added_option_A_key = "added_option_A"
        self.new_line_B_key = "literal_B_new_line"
        self.accent_mark_B_key = "accent_mark_B"
        self.literal_B_key = "literal_B"
        self.punctuation_separator_B_key = "punctuation_separator_B"
        self.empty_space_B_key = "empty_space_B"
        self.option_B_key = "option_B"
        self.added_option_B_key = "added_option_B"
        self.new_line_C_key = "literal_C_new_line"
        self.accent_mark_C_key = "accent_mark_C"
        self.literal_C_key = "literal_C"
        self.punctuation_separator_C_key = "punctuation_separator_C"
        self.empty_space_C_key = "empty_space_C"
        self.option_C_key = "option_C"
        self.added_option_C_key = "added_option_C"
        self.new_line_D_key = "literal_D_new_line"
        self.accent_mark_D_key = "accent_mark_D"
        self.literal_D_key = "literal_D"
        self.punctuation_separator_D_key = "punctuation_separator_D"
        self.empty_space_D_key = "empty_space_D"
        self.option_D_key = "option_D"
        self.added_option_D_key = "added_option_D"
        self.pandoc_comment_key = "pandoc_comment"
        
        
        
        '''
        Single line numerals
        '''
        # Single line numerals regex
        self.single_line_pattern = {
            self.numeral_search_key : self.numeral_character,
            self.punctuation_numeral_key : self.punctuation_separator,
            self.empty_space_numeral_key : self.space_character_but_new_line,
            self.accent_prompt_key : self.accent_mark,
            self.prompt_key : r'.*?',
            self.accent_mark_A_key : self.accent_mark,
            self.literal_A_key : self.literal_A_character,
            self.punctuation_separator_A_key : self.punctuation_separator,
            self.empty_space_A_key : self.space_character_but_new_line,
            self.option_A_key : r'.*?',
            self.accent_mark_B_key : self.accent_mark,
            self.literal_B_key : self.literal_B_character,
            self.punctuation_separator_B_key : self.punctuation_separator,
            self.empty_space_B_key : self.space_character_but_new_line,
            self.option_B_key : r'.*?',
            self.accent_mark_C_key : self.accent_mark,
            self.literal_C_key : self.literal_C_character,
            self.punctuation_separator_C_key : self.punctuation_separator,
            self.empty_space_C_key : self.space_character_but_new_line,
            self.option_C_key : r'.*?',
            self.accent_mark_D_key : self.accent_mark,
            self.literal_D_key : self.literal_D_character,
            self.punctuation_separator_D_key : self.punctuation_separator,
            self.empty_space_D_key : self.space_character_but_new_line,
            self.option_D_key : r'.*$'
        }
        # Single line formatted question pattern
        self.ouput_single_line = self.build_search_pattern(
            rf'\g<{self.numeral_search_key}>',
            self.output_punctuation,
            rf'\g<{self.accent_prompt_key}>',
            rf'\g<{self.prompt_key}>\n\n\t',
            rf'\g<{self.literal_A_key}>',
            self.output_punctuation,
            rf'\g<{self.accent_mark_A_key}>',
            rf'\g<{self.option_A_key}>\n\n\t',
            rf'\g<{self.literal_B_key}>',
            self.output_punctuation,
            rf'\g<{self.accent_mark_B_key}>',
            rf'\g<{self.option_B_key}>\n\n\t',
            rf'\g<{self.literal_C_key}>',
            self.output_punctuation,
            rf'\g<{self.accent_mark_C_key}>',
            rf'\g<{self.option_C_key}>\n\n\t',
            rf'\g<{self.literal_D_key}>',
            self.output_punctuation,
            rf'\g<{self.accent_mark_D_key}>',
            rf'\g<{self.option_D_key}>\n\n',
        )

        '''
        Multiple line numerals
        '''
        # Multiple line numerals regex
        self.multiple_line_pattern = {
            self.numeral_search_key : self.numeral_character,
            self.punctuation_numeral_key : self.punctuation_separator,
            self.empty_space_numeral_key : self.space_character_but_new_line,
            self.accent_prompt_key : self.accent_mark,
            self.prompt_key : self.one_line,
            self.added_prompt_text_key : self.get_interine_text(self.literal_A_character),
            self.new_line_A_key : self.new_line,
            self.accent_mark_A_key : self.accent_mark,
            self.literal_A_key : self.literal_A_character,
            self.punctuation_separator_A_key : self.punctuation_separator,
            self.empty_space_A_key : self.space_character_but_new_line,
            self.option_A_key : self.one_line,
            self.added_option_A_key : self.get_interine_text(self.literal_B_character),
            self.new_line_B_key : self.new_line,
            self.accent_mark_B_key : self.accent_mark,
            self.literal_B_key : self.literal_B_character,
            self.punctuation_separator_B_key : self.punctuation_separator,
            self.empty_space_B_key : self.space_character_but_new_line,
            self.option_B_key : self.one_line,
            self.added_option_B_key : self.get_interine_text(self.literal_C_character),
            self.new_line_C_key : self.new_line,
            self.accent_mark_C_key : self.accent_mark,
            self.literal_C_key : self.literal_C_character,
            self.punctuation_separator_C_key : self.punctuation_separator,
            self.empty_space_C_key : self.space_character_but_new_line,
            self.option_C_key : self.one_line,
            self.added_option_C_key : self.get_interine_text(self.literal_D_character),
            self.new_line_D_key : self.new_line,
            self.accent_mark_D_key : self.accent_mark,
            self.literal_D_key : self.literal_D_character,
            self.punctuation_separator_D_key : self.punctuation_separator,
            self.empty_space_D_key : self.space_character_but_new_line,
            self.option_D_key : self.one_line,
            self.added_option_D_key : self.last_added_text,
            self.pandoc_comment_key : self.pandoc_comment,
        }

        # Multiple line formatted question pattern
        self.ouput_multiple_line = self.build_search_pattern(
            # rf'\g<{self.numeral_search_key}>',
            # self.output_punctuation,
            # rf'\g<{self.accent_prompt_key}>',
            # rf'\g<{self.prompt_key}>',
            # rf'\g<{self.added_prompt_text_key}>',
            # rf'\g<{self.literal_A_key}>',
            # self.output_punctuation,
            # rf'\g<{self.accent_mark_A_key}>',
            # rf'\g<{self.option_A_key}>',
            # rf'\g<{self.added_option_A_key}>'
            # rf'\g<{self.literal_B_key}>',
            # self.output_punctuation,
            # rf'\g<{self.accent_mark_B_key}>',
            # rf'\g<{self.option_B_key}>',
            # rf'\g<{self.literal_C_key}>',
            # self.output_punctuation,
            # rf'\g<{self.accent_mark_C_key}>',
            # rf'\g<{self.option_C_key}>',
            # rf'\g<{self.literal_D_key}>',
            # self.output_punctuation,
            # rf'\g<{self.accent_mark_D_key}>',
            # rf'\g<{self.option_D_key}>',
        )

        self.output_multiline_list = [
            self.numeral_search_key,
            self.output_punctuation,
            self.accent_prompt_key,
            self.prompt_key,
            self.added_prompt_text_key,
            self.new_line_A_key,
            self.literal_A_key,
            self.output_punctuation,
            self.accent_mark_A_key,
            self.option_A_key,
            self.added_option_A_key,
            self.new_line_B_key,
            self.literal_B_key,
            self.output_punctuation,
            self.accent_mark_B_key,
            self.option_B_key,
            self.added_option_B_key,
            self.new_line_C_key,
            self.literal_C_key,
            self.output_punctuation,
            self.accent_mark_C_key,
            self.option_C_key,
            self.added_option_C_key,
            self.new_line_D_key,
            self.literal_D_key,
            self.output_punctuation,
            self.accent_mark_D_key,
            self.option_D_key,
            self.added_option_D_key,
            self.pandoc_comment_key,
        ]
    # def replace_empty_html_comment(self, content):
    #     replaced_string = content
    #     html_code = r'<!-- -->'
    #     if html_code in content:
    #         replaced_string = content.replace(html_code,"empty_html_comment")
    #     return replaced_string

    def get_interine_text(self, literal_match):
        return (
            rf'.+?(?={self.new_line}'
            rf'{literal_match}{self.punctuation_separator}'
            rf'{self.space_character_but_new_line}|'
            rf'{self.new_line}'
            rf'{self.accent_mark}{literal_match}{self.punctuation_separator}'
            rf'{self.space_character_but_new_line})'
        )


    def build_search_pattern(self, *args):
        search_pattern=""
        for arg in args:
            search_pattern += rf'{arg}'
        return rf'{search_pattern}'

    def build_group_regex(self, pattern_name, search_pattern):
        return rf'(?P<{pattern_name}>{search_pattern})'

    # Conectores a las posibles entradas
    def build_single_line_pattern_list(self):
        for regex_id, pattern_value in self.single_line_pattern.items():
            self.pattern_list.append(self.build_group_regex(regex_id, pattern_value))

    def build_multiple_line_pattern_list(self):
        for regex_id, pattern_value in self.multiple_line_pattern.items():
            self.pattern_list.append(self.build_group_regex(regex_id, pattern_value))

    def build_regex(self):
        question_search_pattern = self.build_search_pattern(*self.pattern_list)
        self.question_regex = self.build_group_regex(
            "question",
            question_search_pattern,
        )

    '''
    Main Functions
    '''
    def fix_quiz_single_line_numerals(self):
        self.build_single_line_pattern_list()
        self.build_regex()
        
        question_pattern = re.compile(self.question_regex, re.MULTILINE)
        quiz = question_pattern.sub(self.ouput_single_line, self.raw_text)
        
        return quiz

    def fix_quiz_multiple_line_numerals(self):
        self.build_multiple_line_pattern_list()
        self.build_regex()
        question_pattern = re.compile(self.question_regex, flags=re.DOTALL)
        
        # Tabulate added texts
        tabulate_added_prompt = TemplateCompilerFunction(
            function_name = "tabulate_paragraph",
            args = [self.added_prompt_text_key]
        )
        tabulate_quiz_paragraphs = TemplateCompilerTask(
            task_id = "tabulate_quiz",
            functions = [tabulate_added_prompt]
        )

        template_compiler = TemplateCompiler(
            output_order = self.output_multiline_list,
            transformations = tabulate_quiz_paragraphs,
        )
        quiz = question_pattern.sub(template_compiler, self.raw_text)
        
        return quiz

    '''
    Test functions
    '''
    def test_multiple_line_numerals(self):
        self.build_multiple_line_pattern_list()
        self.build_regex()
        
        question_pattern = re.compile(self.question_regex, re.DOTALL)
        quiz = question_pattern.sub(self.ouput_multiple_line, self.raw_text)
        
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
    

    
