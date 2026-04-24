# -*- coding: utf-8 -*-
# formatter_abstract.py

class FormatterAbstract:

    def __init__(self):
        '''
        General regex
        '''
        # Simple regex
        self.numeral_character = r'\b\d{1,3}\b'
        self.space_but_new_line = r'[^\S\n]+'
        self.optional_space_but_new_line = r'[^\S\n]*'
        self.new_line = r'[^\S \t\r\f\v]+'
        self.excesive_new_line = r'[^\S \t\r\f\v]{3,}+'
        self.punctuation_separator = r'[\.\)]'
        self.accent_mark = r'[*]*'
        self.literal_A_character = r'\b[aA]\b'
        self.literal_B_character = r'\b[bB]\b'
        self.literal_C_character = r'\b[cC]\b'
        self.literal_D_character = r'\b[dD]\b'
        self.soft_new_line = r'\\\n'
        self.pandoc_comment_raw = r'<!-- -->'
        self.worng_italic_mark = r'\*{3}'
        self.worng_bold_mark = r'\*{4}'
        self.comment_mark = r'^>'
        self.escaped_underline = r'\\_'
        self.open_bracket = r'\['
        self.close_bracket = r'\]'
        self.open_braces = r'\{'
        self.closed_braces = r'\}'
        self.content_but_space = r'[^\s]+'
        self.many_simple_spaces = r'[^\S\n\t\r\f\v]+'
        # Dotall
        self.one_line_dotall = r'[^\n]+'
        self.multiline_dotall = r'.+?'
        self.title_mark = r'^#{1,6}'

        self.pandoc_comment = rf'\n{self.pandoc_comment_raw}\n'
        self.end_document = r'\Z'
        
        # Multiline 
        self.raw_chunk_multiline = r'.+?'
        self.to_end_chunk_multiline = r'.*$'
        
        # No Flags
        self.bracket_mark = r'\[(.+?)\]\{.+?\}'
        self.code_block_pattern = (
            rf'{self.pandoc_comment_raw}'
        )
        self.windows_r_chars = r'\r'
        
        self.any_literal = (
            rf'(?:\b[aAbBcCdD]\b)'
            rf'{self.punctuation_separator}'
        )

        # regex compuestos
        self.added_prompt_text = self.get_interine_text(self.literal_A_character)
        self.added_option_A = self.get_interine_text(self.literal_B_character)
        self.added_option_B = self.get_interine_text(self.literal_C_character)
        self.added_option_C = self.get_interine_text(self.literal_D_character)
        self.added_option_D = (
            rf'{self.multiline_dotall}(?=(?:(?:{self.accent_mark}'
            rf'{self.numeral_character}'
            rf'{self.punctuation_separator}{self.accent_mark}'
            rf'{self.space_but_new_line}{self.accent_mark}'
            rf'{self.one_line_dotall})'
            rf'|'
            rf'(?:{self.title_mark}{self.one_line_dotall}))'
            rf'|\Z)'
        )

        # Output regex
        self.output_punctuation = r'.'
        self.simple_new_line = r'\n'
        self.md_newline = r'\n\n'
        self.italic_mark = '*'
        self.bold_mark = '**'
        self.underline = r'_'
        self.simple_space = r' '
        self.numeral_example = "1."
        
        '''
        Regex dictionary keys
        '''
        self.accent_mark_numeral_key = "accent_mark_numeral"
        self.numeral_search_key = "numeral_search"
        self.accent_mark_post_numeral_key = "accent_mark_post_numeral"
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
        
        '''
        Multiline numerals
        '''
        # Options pattern
        self.options_pattern ={
            self.new_line_A_key : self.new_line,
            self.accent_mark_A_key : self.accent_mark,
            self.literal_A_key : self.literal_A_character,
            self.punctuation_separator_A_key : self.punctuation_separator,
            self.empty_space_A_key : self.space_but_new_line,
            self.option_A_key : self.one_line_dotall,
            self.added_option_A_key : self.added_option_A,
            self.new_line_B_key : self.new_line,
            self.accent_mark_B_key : self.accent_mark,
            self.literal_B_key : self.literal_B_character,
            self.punctuation_separator_B_key : self.punctuation_separator,
            self.empty_space_B_key : self.space_but_new_line,
            self.option_B_key : self.one_line_dotall,
            self.added_option_B_key : self.added_option_B,
            self.new_line_C_key : self.new_line,
            self.accent_mark_C_key : self.accent_mark,
            self.literal_C_key : self.literal_C_character,
            self.punctuation_separator_C_key : self.punctuation_separator,
            self.empty_space_C_key : self.space_but_new_line,
            self.option_C_key : self.one_line_dotall,
            self.added_option_C_key : self.added_option_C,
            self.new_line_D_key : self.new_line,
            self.accent_mark_D_key : self.accent_mark,
            self.literal_D_key : self.literal_D_character,
            self.punctuation_separator_D_key : self.punctuation_separator,
            self.empty_space_D_key : self.space_but_new_line,
            self.option_D_key : self.one_line_dotall,
            self.added_option_D_key : self.added_option_D
        }

        self.simple_numeral_pattern = {
            self.accent_mark_numeral_key : self.accent_mark,
            self.numeral_search_key : self.numeral_character,
            self.punctuation_numeral_key : self.punctuation_separator,
            self.accent_mark_post_numeral_key : self.accent_mark,
            self.empty_space_numeral_key : self.space_but_new_line,
            self.accent_prompt_key : self.accent_mark,
            self.prompt_key : self.one_line_dotall,
        }

        self.added_text_numeral_pattern = {
            self.added_prompt_text_key : self.added_prompt_text
        }

        self.regular_numerals_pattern = (
            self.simple_numeral_pattern |
            self.added_text_numeral_pattern
        )

        # Multiline numerals pattern
        self.multiline_pattern = (
            self.regular_numerals_pattern |
            self.options_pattern
        )

        self.headings_pattern = {
            self.numeral_search_key : self.title_mark,
            self.empty_space_numeral_key : self.space_but_new_line,
            self.accent_prompt_key : self.accent_mark,
            self.prompt_key : self.one_line_dotall
        }

        self.headings_replacing_numerals_pattern = {
            self.added_prompt_text_key : self.added_prompt_text
        }

        #Headings but numeral pattern
        self.headings_but_numerals_pattern = (
            self.headings_pattern |
            self.headings_replacing_numerals_pattern |
            self.options_pattern
        )

        self.output_multiline_list = [
            self.numeral_search_key,
            self.output_punctuation,
            self.simple_space,
            self.accent_mark_numeral_key,
            self.accent_prompt_key,
            self.prompt_key,
            self.accent_mark_post_numeral_key,
            self.added_prompt_text_key,
            self.new_line_A_key,
            self.literal_A_key,
            self.output_punctuation,
            self.simple_space,
            self.accent_mark_A_key,
            self.option_A_key,
            self.added_option_A_key,
            self.new_line_B_key,
            self.literal_B_key,
            self.output_punctuation,
            self.simple_space,
            self.accent_mark_B_key,
            self.option_B_key,
            self.added_option_B_key,
            self.new_line_C_key,
            self.literal_C_key,
            self.output_punctuation,
            self.simple_space,
            self.accent_mark_C_key,
            self.option_C_key,
            self.added_option_C_key,
            self.new_line_D_key,
            self.literal_D_key,
            self.output_punctuation,
            self.simple_space,
            self.accent_mark_D_key,
            self.option_D_key,
            self.added_option_D_key,
        ]

        self.pattern_list = []
        self.working_regex = None

    # Funciones auxiliares
    def build_search_pattern(self, *args):
        search_pattern=""
        for arg in args:
            search_pattern += rf'{arg}'
        return rf'{search_pattern}'

    def get_interine_text(self, literal_match):
        return (
            rf'.+?(?={self.new_line}'
            rf'{self.accent_mark}{literal_match}{self.punctuation_separator}'
            rf'{self.space_but_new_line}{self.one_line_dotall})'
        )

    def build_group_atomic_regex(self, pattern_name, search_pattern):
        return rf'(?P<{pattern_name}>(?>{search_pattern}))'

    def build_group_simple_regex(self, pattern_name, search_pattern):
        return rf'(?P<{pattern_name}>{search_pattern})'

    # Conectores a las posibles entradas
    def build_pattern_list(self, pattern_dict: dict):
        self.pattern_list = []
        for regex_id, pattern_value in pattern_dict.items():
            self.pattern_list.append(
                self.build_group_simple_regex(regex_id, pattern_value)
            )

    def build_regex(self):
        question_search_pattern = self.build_search_pattern(*self.pattern_list)
        self.working_regex = self.build_group_simple_regex(
            "question",
            rf'{question_search_pattern}',
        )