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

    def sanitize_text(self):
        self.clear_empty_characters()
        self.remove_comments_marks()
        return self.sanitized_text
