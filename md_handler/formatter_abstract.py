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
        self.any_literal = (
            rf'\b[aAbBcCdD]\b'
        )
        self.soft_new_line = r'\\\n'
        self.comment_mark = r'^>'
        self.escaped_underline = r'\\_'
        self.open_bracket = r'\['
        self.close_bracket = r'\]'
        self.open_braces = r'\{'
        self.closed_braces = r'\}'
        self.content_but_space = r'[^\s]+'
        self.many_simple_spaces = r'[^\S\n\t\r\f\v]+'

        #html
        self.pandoc_comment_raw = r'<!-- -->'
        self.html_new_line = r'<br>'

        # Dotall
        self.one_line_dotall = r'[^\n]+'
        self.multiline_dotall = r'.+?'
        self.title_mark = r'^#{1,6}'

        # Multiline 
        self.raw_chunk_multiline = r'.+?'
        self.to_end_chunk_multiline = r'.*$'
        
        # No Flags
        self.code_block_pattern = (
            rf'{self.pandoc_comment_raw}\n'
        )
        self.windows_r_chars = r'\r'
        
        # Output regex
        self.output_punctuation = r'.'
        self.simple_new_line = r'\n'
        self.md_newline = r'\n\n'
        self.underline = r'_'
        self.simple_space = r' '