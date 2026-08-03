# -*- coding: utf-8 -*-
# formatter_recipes.py

from dataclasses import dataclass, field

@dataclass
class FormatterRecipes:
    accent_mark: str = r'[*]*'
    any_literal: str = r'\b[aAbBcCdD]\b'
    close_bracket: str = r'\]'
    closed_braces: str = r'\}'
    code_block_pattern: str = field(init=False)
    comment_mark: str = r'^>'
    content_but_space: str = r'[^\s]+'
    escaped_underline: str = r'\\_'
    excesive_new_line: str = r'[^\S \t\r\f\v]{3,}+'
    html_new_line: str = r'<br>'
    literal_A_character: str = r'\b[aA]\b'
    literal_B_character: str = r'\b[bB]\b'
    literal_C_character: str = r'\b[cC]\b'
    literal_D_character: str = r'\b[dD]\b'
    many_simple_spaces: str = r'[^\S\n\t\r\f\v]+'
    md_newline: str = r'\n\n'
    multiline_dotall: str = r'.+?'
    new_line: str = r'[^\S \t\r\f\v]+'
    numeral_character: str = r'\b\d{1,3}\b'
    one_line_dotall: str = r'[^\n]+'
    open_braces: str = r'\{'
    open_bracket: str = r'\['
    optional_space_but_new_line: str = r'[^\S\n]*'
    output_punctuation: str = r'.'
    pandoc_comment_raw: str = r'<!-- -->'
    punctuation_separator: str = r'[\.\)]'
    raw_chunk_multiline: str = r'.+?'
    simple_new_line: str = r'\n'
    simple_space: str = r' '
    soft_new_line: str = r'\\\n'
    space_but_new_line: str = r'[^\S\n]+'
    title_mark: str = r'^#{1,6}'
    to_end_chunk_multiline: str = r'.*$'
    underline: str = r'_'
    windows_r_chars: str = r'\r'

    def __post_init__(self) -> None:
        self.code_block_pattern = f"{self.pandoc_comment_raw}\n"