import re
import sys
from pathlib import Path
#from md_handler.template_compiler import TemplateCompiler
from template_compiler import TemplateCompiler
#from data_models.template_compiler_model import TemplateCompilerTask, TemplateCompilerFunction

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
        
        numeral_search_key = "numeral_search"
        punctuation_numeral_key = "punctuation_numeral"
        empty_space_numeral_key = "empty_space_numeral"
        accent_prompt_key = "accent_prompt"
        prompt_key = "prompt"
        added_prompt_text_key = "added_prompt_text"
        new_line_A_key = "literal_A_new_line"
        accent_mark_A_key = "accent_mark_A"
        literal_A_key = "literal_A"
        punctuation_separator_A_key = "punctuation_separator_A"
        empty_space_A_key = "empty_space_A"
        option_A_key = "option_A"
        added_option_A_key = "added_option_A"
        new_line_B_key = "literal_B_new_line"
        accent_mark_B_key = "accent_mark_B"
        literal_B_key = "literal_B"
        punctuation_separator_B_key = "punctuation_separator_B"
        empty_space_B_key = "empty_space_B"
        option_B_key = "option_B"
        added_option_B_key = "added_option_B"
        new_line_C_key = "literal_C_new_line"
        accent_mark_C_key = "accent_mark_C"
        literal_C_key = "literal_C"
        punctuation_separator_C_key = "punctuation_separator_C"
        empty_space_C_key = "empty_space_C"
        option_C_key = "option_C"
        added_option_C_key = "added_option_C"
        new_line_D_key = "literal_D_new_line"
        accent_mark_D_key = "accent_mark_D"
        literal_D_key = "literal_D"
        punctuation_separator_D_key = "punctuation_separator_D"
        empty_space_D_key = "empty_space_D"
        option_D_key = "option_D"
        added_option_D_key = "added_option_D"
        pandoc_comment_key = "pandoc_comment"
        
        
        
        '''
        Single line numerals
        '''
        # Single line numerals regex
        self.single_line_pattern = {
            numeral_search_key : self.numeral_character,
            punctuation_numeral_key : self.punctuation_separator,
            empty_space_numeral_key : self.space_character_but_new_line,
            accent_prompt_key : self.accent_mark,
            prompt_key : r'.*?',
            accent_mark_A_key : self.accent_mark,
            literal_A_key : self.literal_A_character,
            punctuation_separator_A_key : self.punctuation_separator,
            empty_space_A_key : self.space_character_but_new_line,
            option_A_key : r'.*?',
            accent_mark_B_key : self.accent_mark,
            literal_B_key : self.literal_B_character,
            punctuation_separator_B_key : self.punctuation_separator,
            empty_space_B_key : self.space_character_but_new_line,
            option_B_key : r'.*?',
            accent_mark_C_key : self.accent_mark,
            literal_C_key : self.literal_C_character,
            punctuation_separator_C_key : self.punctuation_separator,
            empty_space_C_key : self.space_character_but_new_line,
            option_C_key : r'.*?',
            accent_mark_D_key : self.accent_mark,
            literal_D_key : self.literal_D_character,
            punctuation_separator_D_key : self.punctuation_separator,
            empty_space_D_key : self.space_character_but_new_line,
            option_D_key : r'.*$'
        }
        # Single line formatted question pattern
        self.ouput_single_line = self.build_search_pattern(
            rf'g<{numeral_search_key}>',
            r'. ',
            rf'g<{accent_prompt_key}>',
            r'\g<prompt>\n\n\t',
            rf'g<{literal_A_key}>',
            r'. ',
            rf'g<{accent_mark_A_key}>',
            r'\g<option_A>\n\n\t',
            r'\g<literal_B>',
            r'. ',
            r'\g<accent_mark_B>',
            r'\g<option_B>\n\n\t',
            r'\g<literal_C>',
            r'. ',
            r'\g<accent_mark_C>',
            r'\g<option_C>\n\n\t',
            r'\g<literal_D>',
            r'. ',
            r'\g<accent_mark_D>',
            r'\g<option_D>\n\n',
        )

        '''
        Multiple line numerals
        '''
        # Multiple line numerals regex
        self.multiple_line_pattern = {
            numeral_search_key : self.numeral_character,
            punctuation_numeral_key : self.punctuation_separator,
            empty_space_numeral_key : self.space_character_but_new_line,
            accent_prompt_key : self.accent_mark,
            prompt_key : self.one_line,
            added_prompt_text_key : self.get_interine_text(self.literal_A_character),
            new_line_A_key : self.new_line,
            accent_mark_A_key : self.accent_mark,
            literal_A_key : self.literal_A_character,
            punctuation_separator_A_key : self.punctuation_separator,
            empty_space_A_key : self.space_character_but_new_line,
            option_A_key : self.one_line,
            added_option_A_key : self.get_interine_text(self.literal_B_character),
            new_line_B_key : self.new_line,
            accent_mark_B_key : self.accent_mark,
            literal_B_key : self.literal_B_character,
            punctuation_separator_B_key : self.punctuation_separator,
            empty_space_B_key : self.space_character_but_new_line,
            option_B_key : self.one_line,
            added_option_B_key : self.get_interine_text(self.literal_C_character),
            new_line_C_key : self.new_line,
            accent_mark_C_key : self.accent_mark,
            literal_C_key : self.literal_C_character,
            punctuation_separator_C_key : self.punctuation_separator,
            empty_space_C_key : self.space_character_but_new_line,
            option_C_key : r'.*?',
            added_option_C_key : self.get_interine_text(self.literal_D_character),
            new_line_D_key : self.new_line,
            accent_mark_D_key : self.accent_mark,
            literal_D_key : self.literal_D_character,
            punctuation_separator_D_key : self.punctuation_separator,
            empty_space_D_key : self.space_character_but_new_line,
            option_D_key : self.one_line,
            added_option_D_key : self.last_added_text,
            pandoc_comment_key : self.pandoc_comment,
        }

        # Multiple line formatted question pattern
        self.ouput_multiple_line = self.build_search_pattern(
            # rf'g<{numeral_search_key}>',
            # r'. ',
            # rf'g<{accent_prompt_key}>',
            # rf'g<{prompt_key}>',
            # rf'\g<{added_prompt_text_key}>',
            # rf'g<{literal_A_key}>',
            # r'. ',
            # rf'g<{accent_mark_A_key}>',
            # rf'g<{option_A_key}>',
            # rf'\g<{added_option_A_key}>'
            # r'\g<literal_B>',
            # r'. ',
            # r'\g<accent_mark_B>',
            # r'\g<option_B>\n\n\t',
            # r'\g<literal_C>',
            # r'. ',
            # r'\g<accent_mark_C>',
            # r'\g<option_C>\n\n\t',
            # r'\g<literal_D>',
            # r'. ',
            # r'\g<accent_mark_D>',
            # r'\g<option_D>\n\n',
        )
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
        template_compiler = TemplateCompiler(
            self.ouput_multiple_line,
            '')
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
    

    
