# -*- coding: utf-8 -*-
# md_formatter.py

import re
from md_handler.formatter_abstract import FormatterAbstract

class SequenceFormatter(FormatterAbstract):
    
    def __init__(self, content):
        super().__init__()
        self.markdown_text = content
        self.numeral_counter = 0
    
    def apply_regex(self, pattern, replace):
        self.markdown_text= re.sub(
            pattern,
            replace,
            self.markdown_text,
        )

    def get_fixed_numeral_text(self, match: re.Match) -> str:
        normal_text = match.group(2)
        self.numeral_counter += 1

        return f'{self.numeral_counter}{self.output_punctuation}{normal_text}'

    def fix_numerals_sequence(self):
        numeral_pattern = (
            rf'^({self.numeral_character}{self.output_punctuation})'
            rf'({self.to_end_chunk_multiline})'
        )
        numeral_regex = re.compile(numeral_pattern, re.MULTILINE)
        self.markdown_text = numeral_regex.sub(
            self.get_fixed_numeral_text,
            self.markdown_text,
        )

    # Función que reúne el formato standar del cuestionario
    def get_formatted_text(self):
        self.numeral_counter = 0
        self.fix_numerals_sequence()
        self.numeral_counter = 0
        
        return self.markdown_text

