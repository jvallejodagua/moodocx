import re
import sys
from pathlib import Path

class RegexBuilder:

    def __init__(self):
        self.pattern_list = []
        self.question_regex = None

        # Items has not new lines for options
        self.single_line_pattern = {
            "numeral_search" : r'[\d+][\.\)]',
            "empty_space" : r'[\s*^\n]',
            "accent_prompt" : r'[*]*',
            "prompt" : r'.*?',
            "accent_literal_A" : r'[*]*',
            "literal_A" : r'[aA][\.\)]',
            "empty_space_A" : r'[\s*^\n]',
            "option_A" : r'.*?',
            "accent_literal_B" : r'[*]*',
            "literal_B" : r'[bB][\.\)]',
            "empty_space_B" : r'[\s*^\n]',
            "option_B" : r'.*?',
            "accent_literal_C" : r'[*]*',
            "literal_C" : r'[cC][\.\)]',
            "empty_space_C" : r'[\s*^\n]',
            "option_C" : r'.*?',
            "accent_literal_D" : r'[*]*',
            "literal_D" : r'[dD][\.\)]',
            "empty_space_D" : r'[\s*^\n]',
            "option_D" : r'.*$'
        }

    def build_search_pattern(self, *args):
        search_pattern=""
        for arg in args:
            search_pattern += rf'{arg}'
        return rf'{search_pattern}'

    def build_group_regex(self, pattern_name, search_pattern):
        return rf'(?P<{pattern_name}>{search_pattern})'

    def get_self_path(self):

        if getattr(sys, 'frozen', False):
            self_path = Path(sys.executable).resolve().parent.absolute()
        else:
            self_path = Path(__file__).resolve().parent.absolute()
            
        return self_path

    def build_single_line_pattern_list(self):
        for (regex_id, pattern_value) in self.single_line_pattern:
            self.pattern_list.append(self.build_group_regex(regex_id, pattern_value))

    def build_regex(self):
        question_search_pattern = self.build_search_pattern(self.pattern_list)
        self.question_regex = self.build_group_regex(
            "question",
            question_search_pattern,
        )
        """
        question_search_pattern = build_search_pattern(
            regex_accent_prompt,
            regex_numeral,
            regex_empty_space,
            regex_prompt,
            regex_accent_literal_A,
            regex_literal_A,
            regex_empty_space_A,
            regex_option_A,
            regex_accent_literal_B,
            regex_literal_B,
            regex_empty_space_B,
            regex_option_B,
            regex_accent_literal_C,
            regex_literal_C,
            regex_empty_space_C,
            regex_option_C,
            regex_accent_literal_D,
            regex_literal_D,
            regex_empty_space_D,
            regex_option_D
        )
        """


if __name__ == "__main__":

    tests_path = get_self_path() / "Temporales"
    file_path = tests_path / "EvaluacionCopiada.md"

    content=""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    


    regex_question = build_group_regex(
        "question",
        question_search_pattern,
    )
    question_pattern = re.compile(regex_question, re.MULTILINE)
    for match in question_pattern.finditer(content):
        datos = match.groupdict()

        print(f"question: {datos["question"]}")

    print("\n\n:::::::::::::::::::::::::::::::\n\n")

    # Patrón que describe el nuevo orden de la pregunta
    regex_new_question_order = build_search_pattern(
        r'\g<numeral_search>',
        r' ',
        r'\g<accent_prompt>',
        r'\g<prompt>\n\n'
        r'\g<literal_A>',
        r' ',
        r'\g<accent_literal_A>',
        r'\g<option_A>\n\n',
        r'\g<literal_B>',
        r' ',
        r'\g<accent_literal_B>',
        r'\g<option_B>\n\n',
        r'\g<literal_C>',
        r' ',
        r'\g<accent_literal_C>',
        r'\g<option_C>\n\n',
        r'\g<literal_D>'
        r' ',
        r'\g<accent_literal_D>',
        r'\g<option_D>\n\n',
    )

questions = question_pattern.sub(regex_new_question_order, content)

print(questions)
# for match in questions.finditer(content):
#     datos = match.groupdict()

#     print(f"question: {datos["question"]}")

    
