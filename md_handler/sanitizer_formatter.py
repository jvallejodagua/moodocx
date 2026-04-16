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


    def remove_comments_marks(self):
        comment_mark_pattern = (
            rf'^>(?:{self.space_character_but_new_line})?'
            rf'(.*)({self.new_line})?'
        )
        comment_mark_regex = re.compile(comment_mark_pattern, re.MULTILINE)
        self.apply_regex(comment_mark_regex, r'\1\2')

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
            rf'({self.space_character_but_new_line}{self.multiline_dotall})'
            rf'({self.close_bracket}{self.open_braces}'
            rf'{self.multiline_dotall}{self.closed_braces})'
        )
        marks_regex = re.compile(marks_pattern, re.DOTALL)
        self.sanitized_text = re.sub(
            marks_regex,
            self.reorder_marks,
            self.sanitized_text
        )

    def expand_options_marks(self):
        colapsed_pattern = (
            rf'(^{self.any_literal}'
            rf'{self.space_character_but_new_line}'
            rf'{self.open_bracket}{self.raw_chunk_multiline}'
            rf'{self.close_bracket}{self.open_braces}'
            rf'{self.raw_chunk_multiline}{self.closed_braces})'
            rf'({self.any_literal}'
            rf'{self.space_character_but_new_line})'
        )
        colapsed_regex = re.compile(colapsed_pattern, re.MULTILINE)
        self.apply_regex(colapsed_regex, r'\1\n\2')

    def expand_options_general(self):

        expand_options_pattern = (
            rf'({self.any_literal}'
            rf'{self.space_character_but_new_line}'
            rf'{self.raw_chunk_multiline})'
            rf'({self.any_literal}'
            rf'{self.space_character_but_new_line}'
            rf'{self.raw_chunk_multiline})'
        )

        expand_options_regex = re.compile(expand_options_pattern, re.MULTILINE)
        self.apply_regex(
            expand_options_regex,
            rf'\1{self.md_newline}\2'
        )

    def expand_single_literal(self):

        single_literal_pattern = (
            rf'({self.closed_braces})({self.any_literal}'
            rf'{self.space_character_but_new_line})'
        )

        single_literal_regex = re.compile(single_literal_pattern)

        self.apply_regex(single_literal_regex, r'\1\n\n\2')

    def sanitize_text(self):
        self.clear_empty_characters()
        self.remove_comments_marks()
        self.remove_soft_new_lines()
        self.remove_escaped_underline()
        self.apply_marks_to_options()
        self.expand_options_marks()
        self.expand_options_general()
        self.expand_options_general()
        self.expand_options_general()
        self.expand_single_literal()
        return self.sanitized_text
