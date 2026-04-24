# -*- coding: utf-8 -*-
# sanitizer_formatter.py

import re
from md_handler.formatter_abstract import FormatterAbstract

class SanitizerFormatter(FormatterAbstract):

    def __init__(self, content):
        super().__init__()

        self.sanitized_text = content

    def apply_regex(self, pattern, replace):
        self.sanitized_text= re.sub(
            pattern,
            replace,
            self.sanitized_text,
        )

    def clear_empty_characters(self):
        #¿Cuándo ocurren los otros caracteres vacíos?
        #empty_characters_pattern = r'[\r\x0b\x0c\u200b\ufeff]'
        #Retroceso de carro para limpiar
        empty_characters_pattern = r'[\r]'
        empty_characters_regex = re.compile(empty_characters_pattern)
        self.apply_regex(empty_characters_regex, r'')

    def remove_new_line_empty_space(self):
        new_line_empty_space_pattern = (
            rf'^{self.many_simple_spaces}({self.one_line_dotall})'
        )

        new_line_empty_space_regex = re.compile(
            new_line_empty_space_pattern,
            re.MULTILINE
        )

        self.apply_regex(new_line_empty_space_regex, r'\1')

    def remove_comments_marks(self):
        comment_mark_pattern = (
            rf'{self.comment_mark}({self.optional_space_but_new_line})'
            rf'({self.to_end_chunk_multiline}$)'
        )
        comment_mark_regex = re.compile(comment_mark_pattern, re.MULTILINE)
        self.apply_regex(comment_mark_regex, r'\2')

    def remove_soft_new_lines(self):
        soft_new_line_pattern = rf'{self.soft_new_line}'
        simple_new_line_pattern = rf'{self.simple_new_line}'
        soft_new_line_regex = re.compile(soft_new_line_pattern)
        self.apply_regex(soft_new_line_regex, simple_new_line_pattern)

    def remove_escaped_underline(self):
        escaped_underline_pattern = rf'{self.escaped_underline}'
        underline_pattern = rf'{self.underline}'
        escaped_underline_regex = re.compile(escaped_underline_pattern)
        self.apply_regex(escaped_underline_regex, underline_pattern)

    def reorder_marks(self, match):
        mark = match.group(1)
        literal = match.group(2)
        content = match.group(3).strip()
        mark_closing = match.group(4)

        return f'{literal} {mark}{content}{mark_closing}'

    def apply_marks_to_options(self):
        marks_pattern = (
            rf'({self.open_bracket})'
            rf'({self.any_literal})'
            rf'({self.space_but_new_line}{self.multiline_dotall})'
            rf'({self.close_bracket}{self.open_braces}'
            rf'{self.multiline_dotall}{self.closed_braces})'
        )
        marks_regex = re.compile(marks_pattern, re.DOTALL)
        self.sanitized_text = re.sub(
            marks_regex,
            self.reorder_marks,
            self.sanitized_text
        )

    def refactorize_marks(self):
        diluted_mark_pattern = (
            rf'({self.open_bracket}{self.one_line_dotall})'
            rf'({self.new_line}{self.optional_space_but_new_line})'
            rf'({self.close_bracket}'
            rf'{self.open_braces}{self.one_line_dotall}{self.closed_braces})'
        )
        diluted_mark_regex = re.compile(diluted_mark_pattern, re.DOTALL)
        self.apply_regex(diluted_mark_regex, r'\1\3')

    def expand_options_marks(self):
        colapsed_pattern = (
            rf'(^{self.any_literal}'
            rf'{self.space_but_new_line}'
            rf'{self.open_bracket}{self.raw_chunk_multiline}'
            rf'{self.close_bracket}{self.open_braces}'
            rf'{self.raw_chunk_multiline}{self.closed_braces})'
            rf'({self.any_literal}'
            rf'{self.space_but_new_line})'
        )
        colapsed_regex = re.compile(colapsed_pattern, re.MULTILINE)
        self.apply_regex(colapsed_regex, rf'\1{self.simple_new_line}\2')

    def expand_options_general(self):

        expand_options_pattern = (
            rf'((?:{self.any_literal}|' #literal or numeral
            rf'(?:{self.numeral_character}{self.punctuation_separator}))'
            rf'{self.space_but_new_line}'
            rf'{self.raw_chunk_multiline})'
            rf'({self.any_literal}'
            rf'{self.space_but_new_line}'
            rf'{self.raw_chunk_multiline})'
        )

        expand_options_regex = re.compile(expand_options_pattern, re.MULTILINE|re.VERBOSE)
        self.apply_regex(
            expand_options_regex,
            rf'\1{self.md_newline}\2'
        )

    def expand_single_literal(self):

        single_literal_pattern = (
            rf'({self.closed_braces})({self.any_literal}'
            rf'{self.space_but_new_line}'
            rf'{self.one_line_dotall})'
        )

        single_literal_regex = re.compile(single_literal_pattern)

        self.apply_regex(single_literal_regex, rf'\1{self.simple_new_line}\2')

    def delete_code_blocks(self):
        code_block_pattern = (
            rf'{self.code_block_pattern}'
        )

        code_block_regex = re.compile(code_block_pattern)
        self.apply_regex(code_block_regex, r'')

    def fix_literals(self):

        compact_literal_pattern = (
            rf'({self.any_literal})({self.optional_space_but_new_line})'
            rf'({self.one_line_dotall})'
        )

        compact_literal_regex = re.compile(compact_literal_pattern)

        self.apply_regex(compact_literal_regex, r'\1 \3')

    def fix_excesive_new_lines(self):

        new_line_pattern = rf'{self.excesive_new_line}'
        new_line_regex = re.compile(new_line_pattern)
        
        self.apply_regex(new_line_regex, rf'{self.md_newline}')
    
    def fix_collapsed_options(self):

        collapsed_option_pattern = (
            rf'({self.content_but_space})'
            rf'\n'
            rf'({self.optional_space_but_new_line}'
            rf'{self.any_literal} {self.one_line_dotall})'
        )

        collapsed_option_regex = re.compile(collapsed_option_pattern)
        
        self.apply_regex(
            collapsed_option_regex,
            rf'\1{self.md_newline}\2'
            )

    def replace_if_not_interine_numeral(self, match):
        data = match.groupdict()
        interine_text = data.get(self.added_prompt_text_key)
        self.build_pattern_list(self.simple_numeral_pattern)
        self.build_regex()
        numeral_regex = re.compile(
            self.working_regex,
            re.MULTILINE
        )

        not_replace = numeral_regex.search(interine_text)
        original_text = match.group(0)

        if not_replace:
            return original_text
        
        target_key = self.numeral_search_key
        new_value = self.numeral_example

        modified_text = original_text

        if target_key in data and data[target_key] is not None:

            initial_group = match.start(target_key) - match.start(0)
            end_group = match.end(target_key) - match.start(0)

            modified_text = (
                original_text[:initial_group] +
                new_value +
                original_text[end_group:]
            )
        
        return modified_text

    def fix_wrong_headings_replacing_numerals(self):
        self.build_pattern_list(self.headings_but_numerals_pattern)
        self.build_regex()
        
        question_regex = re.compile(
            self.working_regex,
            flags=re.DOTALL|re.MULTILINE
        )

        self.sanitized_text = re.sub(
            question_regex,
            self.replace_if_not_interine_numeral,
            self.sanitized_text
        )

    def sanitize_text(self):
        self.clear_empty_characters()
        self.remove_new_line_empty_space()
        self.remove_comments_marks()
        self.remove_soft_new_lines()
        self.remove_escaped_underline()
        self.apply_marks_to_options()
        self.refactorize_marks()
        self.expand_options_marks()
        self.expand_options_general()
        self.expand_options_general()
        self.expand_options_general()
        self.expand_single_literal()
        self.expand_single_literal()
        self.expand_single_literal()
        self.delete_code_blocks()
        self.fix_literals()
        self.fix_excesive_new_lines()
        self.fix_collapsed_options()
        self.fix_collapsed_options()
        self.fix_collapsed_options()
        self.fix_wrong_headings_replacing_numerals()
        return self.sanitized_text
