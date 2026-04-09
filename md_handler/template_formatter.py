import re
import sys
from pathlib import Path

class TemplateFormatter:

    def __init__(self, content):
        self.markdown_text = content
        self.pattern_list = []
        self.question_regex = None
        '''
        Inputs
        '''
        # Single line numerals regex
        self.single_line_pattern = {
            "numeral_search" : r'[\d+][\.\)]',
            "empty_space" : r'[\s*^\n]',
            "accent_prompt" : r'[*]*',
            "prompt" : r'.*?',
            "accent_literal_A" : r'[*]*',
            "literal_A" : r'[aA]',
            "punctuation_literal_A" : r'[\.\)]',
            "empty_space_A" : r'[\s*^\n]',
            "option_A" : r'.*?',
            "accent_literal_B" : r'[*]*',
            "literal_B" : r'[bB]',
            "punctuation_literal_B" : r'[\.\)]',
            "empty_space_B" : r'[\s*^\n]',
            "option_B" : r'.*?',
            "accent_literal_C" : r'[*]*',
            "literal_C" : r'[cC]',
            "punctuation_literal_C" : r'[\.\)]',
            "empty_space_C" : r'[\s*^\n]',
            "option_C" : r'.*?',
            "accent_literal_D" : r'[*]*',
            "literal_D" : r'[dD]',
            "punctuation_literal_D" : r'[\.\)]',
            "empty_space_D" : r'[\s*^\n]',
            "option_D" : r'.*$'
        }

        '''
        Outputs
        '''
        # Single line formatted question pattern
        self.ouput_question_pattern = self.build_search_pattern(
            r'\g<numeral_search>',
            r' ',
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
        quiz = question_pattern.sub(self.ouput_question_pattern, content)
        
        return quiz

    def get_self_path(self):

        if getattr(sys, 'frozen', False):
            self_path = Path(sys.executable).resolve().parent.absolute()
        else:
            self_path = Path(__file__).resolve().parent.absolute()
            
        return self_path

if __name__ == "__main__":

    tests_path = Path("C:\RepositoriosGit\moodocx\Temporales")
    file_path = tests_path / "EvaluacionCopiada.md"

    content=""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    regex_builder = TemplateFormatter(content)
    
    regex_builder.build_single_line_pattern_list()
    regex_builder.build_regex()
    
    question_pattern = re.compile(regex_builder.question_regex, re.MULTILINE)
    for match in question_pattern.finditer(content):
        datos = match.groupdict()

        print(f"question: {datos["question"]}")

    print("\n\n:::::::::::::::::::::::::::::::\n\n")

    questions = question_pattern.sub(regex_builder.ouput_question_pattern, content)
    output_file_path = tests_path / "EvaluacionTransformada.md"
    with open(output_file_path, 'w', encoding='utf-8') as f2:
        f2.write(questions)
    

    
