# -*- coding: utf-8 -*-
# md_formatter.py

import re
from pathlib import Path
from md_handler.ai_md_formatter import AIMdFormatter

class MdFormatter:
    
    def __init__(self, content, root_path):
        self.markdown_text = content
        self.numeral_counter = 0
        self.root_path = root_path
    
    def apply_regex(self, pattern, replace):
        self.markdown_text= re.sub(
            pattern,
            replace,
            self.markdown_text,
        )

    def markdown_ai_format(self):
        ai_formatter = AIMdFormatter(self.root_path)
        self.markdown_text = ai_formatter.get_formatted_text_gemma(self.markdown_text)

    def remove_code_blocks(self):
        #code_block_pattern = re.compile(r'```.*?```',re.DOTALL)
        #code_block_pattern = re.compile(r'```[\s\S]*?```')
        code_block_pattern1 = re.compile(r'```[\s\S]*?```\s*', re.MULTILINE)
        code_block_pattern2 = re.compile(r'<!-- -->\n')
        self.apply_regex(code_block_pattern1, r'')
        self.apply_regex(code_block_pattern2, r'')

    def remove_comments_marks(self):
        comment_mark_pattern =re.compile(r'>( *)(.*\n)')
        self.apply_regex(comment_mark_pattern, r'\t\2')

    def extract_match_components(self, match: re.Match) -> tuple[str, str, str]:
        prefix = match.group(1).strip()
        literal = match.group(2).strip().upper()
        literal = literal.replace(")",".")
        content = match.group(3).strip()
        return prefix, literal, content        

    def format_reordered_literal_line(self, match: re.Match) -> str:
        prefix, literal, content = self.extract_match_components(match)
        if prefix:
            return f"{literal} {prefix}{content}"
        return f"{literal} {content}"

    def format_literals(self):
        literal_pattern = re.compile(r'^([^a-zA-Z\n]*)([a-zA-Z][\.\)])\s*(.*)$', re.MULTILINE)
        self.markdown_text = literal_pattern.sub(
            self.format_reordered_literal_line,
            self.markdown_text)

    # \ from chatgpt exams
    def fix_soft_new_line(self):
        new_line_pattern = re.compile(r'\\\n')
        self.apply_regex(new_line_pattern, r'\n\n')

    def remove_double_space(self):
        double_space_numeral_pattern = re.compile(r'(\d+\.)[ \t]{2,}')
        self.apply_regex(double_space_numeral_pattern, r'\1 ')

        double_space_literal_pattern = re.compile(r'([a-zA-Z]\.)[ \t]{2,}')
        self.apply_regex(double_space_literal_pattern, r'\1 ')
    
    def get_fixed_numeral_text(self, match: re.Match) -> str:
        normal_text = match.group(2)
        self.numeral_counter += 1

        return f'{self.numeral_counter}. {normal_text}'

    def fix_numerals_sequence(self):
        numeral_pattern = re.compile(r'^([\d+][\.\)] )\s*(.*)$', re.MULTILINE)
        self.markdown_text = numeral_pattern.sub(
            self.get_fixed_numeral_text,
            self.markdown_text,
        )

    def standardize_indentation(self, match) -> str:
        options_block = match.group(0)
        cleaned_block = re.sub(
            r'^[ \t]*',
            '\t',
            options_block,
            flags=re.MULTILINE,
        )
        return cleaned_block

    def process_question_block(self, match) -> str:
        numeral_line = match.group(1)
        options_block = match.group(2)
        cleaned_options = self.standardize_indentation(
            re.match(r'[\s\S]*', options_block),
        )
        return f"{numeral_line}{cleaned_options}"

    def tabulate_numeral_text(self):
        pattern = re.compile(
            r'^(\d+\.[^\n]*\n)([\s\S]*?^[ \t]*[Dd]\.[^\n]*)',
            re.MULTILINE,
        )
        self.markdown_text = pattern.sub(
            self.process_question_block,
            self.markdown_text,
        )

    def fix_sigle_new_lines(self):
        sigle_new_line_pattern = re.compile(r'(\t[A-Z]\. .*)\r?\n(?=\t[A-Z]\. .*)')
        self.apply_regex(sigle_new_line_pattern, r'\1\n\n')

    def marks_to_bold(self):
        mark_pattern = re.compile(r'\[(.+?)\]\{.+?\}')
        self.apply_regex(mark_pattern, r'**\1**')
    
    # Función que reúne el formato standar del cuestionario
    def get_formatted_markdown_text(self):
        self.numeral_counter = 0
        self.markdown_ai_format()
        # self.remove_code_blocks()
        # self.remove_comments_marks()
        # self.format_literals()
        # self.fix_numerals_sequence()
        # self.fix_soft_new_line()
        # self.remove_double_space()
        # self.tabulate_numeral_text()
        # self.fix_sigle_new_lines()
        # self.marks_to_bold()
        self.numeral_counter = 0
        
        return self.markdown_text

