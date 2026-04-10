import re
import sys
from pathlib import Path

class TemplateFormatter:

    def __init__(self, content):
        self.markdown_text = content
        self.pattern_list = []
        self.question_regex = None

        '''
        General regex
        '''
        numeral_character = r'\d+'
        space_character_but_new_line = r'[ \t\r\f\v]+'
        punctuation_separator = r'[\.\)]'
        accent_literal = r'[*]*'
        literal_A_character = r'[aA]'
        literal_B_character = r'[bB]'
        literal_C_character = r'[cC]'
        literal_D_character = r'[dD]'

        '''
        Single line numerals
        '''
        # Single line numerals regex
        self.single_line_pattern = {
            "numeral_search" : numeral_character,
            "punctuation_separator_numeral" : punctuation_separator,
            "empty_space" : space_character_but_new_line,
            "accent_prompt" : accent_literal,
            "prompt" : r'.*?',
            "accent_literal_A" : accent_literal,
            "literal_A" : literal_A_character,
            "punctuation_separator_A" : punctuation_separator,
            "empty_space_A" : space_character_but_new_line,
            "option_A" : r'.*?',
            "accent_literal_B" : accent_literal,
            "literal_B" : literal_B_character,
            "punctuation_separator_B" : punctuation_separator,
            "empty_space_B" : space_character_but_new_line,
            "option_B" : r'.*?',
            "accent_literal_C" : accent_literal,
            "literal_C" : literal_C_character,
            "punctuation_separator_C" : punctuation_separator,
            "empty_space_C" : space_character_but_new_line,
            "option_C" : r'.*?',
            "accent_literal_D" : accent_literal,
            "literal_D" : literal_D_character,
            "punctuation_separator_D" : punctuation_separator,
            "empty_space_D" : space_character_but_new_line,
            "option_D" : r'.*$'
        }
        # Single line formatted question pattern
        self.ouput_single_line_question_pattern = self.build_search_pattern(
            r'\g<numeral_search>',
            r'. ',
            r'\g<accent_prompt>',
            r'\g<prompt>\n\n\t',
            r'\g<literal_A>',
            r'. ',
            r'\g<accent_literal_A>',
            r'\g<option_A>\n\n\t',
            r'\g<literal_B>',
            r'. ',
            r'\g<accent_literal_B>',
            r'\g<option_B>\n\n\t',
            r'\g<literal_C>',
            r'. ',
            r'\g<accent_literal_C>',
            r'\g<option_C>\n\n\t',
            r'\g<literal_D>',
            r'. ',
            r'\g<accent_literal_D>',
            r'\g<option_D>\n\n',
        )

        '''
        Multiple line numerals
        '''
        # Multiple line numerals regex
        self.multiple_line_pattern = {
            "numeral_search" : numeral_character,
            "punctuation_separator_numeral" : punctuation_separator,
            "empty_space" : space_character_but_new_line,
            "accent_prompt" : accent_literal,
            "prompt" : r'.+?(?=\n)',
            "surrounding_prompt_text" : rf'.+(?=\n{literal_A_character}{space_character_but_new_line})',
            # "accent_literal_A" : r'[\n]*[*]*',
            # "literal_A" : literal_A_character,
            # "punctuation_separator_A" : punctuation_separator,
            # "empty_space_A" : space_character_but_new_line,
            # "option_A" : r'.*',
            #"accent_literal_B" : accent_literal,
            #"literal_B" : literal_B_character,
            #"punctuation_separator_B" : punctuation_separator,
            #"empty_space_B" : space_character_but_new_line,
            #"option_B" : r'.*?',
            # "accent_literal_C" : accent_literal,
            # "literal_C" : literal_C_character,
            # "punctuation_separator_C" : punctuation_separator,
            # "empty_space_C" : space_character_but_new_line,
            # "option_C" : r'.*?',
            # "accent_literal_D" : accent_literal,
            # "literal_D" : literal_D_character,
            # "punctuation_separator_D" : punctuation_separator,
            # "empty_space_D" : space_character_but_new_line,
            # "option_D" : r'.*$'
        }

        # Multiple line formatted question pattern
        self.ouput_multiple_line_question_pattern = self.build_search_pattern(
            r'\g<numeral_search>',
            r'. ',
            r'\g<accent_prompt>',
            r'\g<prompt>\n\n',
            # r'\t\g<surrounding_prompt_text>\n\n',
            # r'\g<literal_A>',
            # r'. ',
            # r'\g<accent_literal_A>',
            # r'\g<option_A>\n\n\t',
            # r'\g<literal_B>',
            # r'. ',
            # r'\g<accent_literal_B>',
            # r'\g<option_B>\n\n\t',
            # r'\g<literal_C>',
            # r'. ',
            # r'\g<accent_literal_C>',
            # r'\g<option_C>\n\n\t',
            # r'\g<literal_D>',
            # r'. ',
            # r'\g<accent_literal_D>',
            # r'\g<option_D>\n\n',
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

    # Funciones principales
    def fix_quiz_single_line_numerals(self):
        self.build_single_line_pattern_list()
        self.build_regex()
        
        question_pattern = re.compile(self.question_regex, re.MULTILINE)
        quiz = question_pattern.sub(self.ouput_single_line_question_pattern, content)
        
        return quiz

    def fix_quiz_multiple_line_numerals(self):
        self.build_multiple_line_pattern_list()
        self.build_regex()
        
        question_pattern = re.compile(self.question_regex, flags=re.DOTALL)
        quiz = question_pattern.sub(self.ouput_multiple_line_question_pattern, content)
        
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

    regex_builder = TemplateFormatter(content)
    
    quiz = regex_builder.fix_quiz_multiple_line_numerals()
    output_file_path = tests_path / "EvaluacionTransformada.md"
    with open(output_file_path, 'w', encoding='utf-8') as f2:
        f2.write(quiz)
    

    
