# -*- coding: utf-8 -*-
# md_formatter_processor.py

import re
from md_handler.sequence_formatter import SequenceFormatter
from md_handler.template_formatter import TemplateFormatter
from filesystem.files_finder import FilesInSubfolder
import time

class SequenceFormatterProcessor:
    
    def __init__(self, source_directory: str):
        self.template_formatter = None
        self.sequence_formatter = None
        self.files_finder = FilesInSubfolder(
            route_to_subfolder = source_directory,
            suffix_extension = ".md",
        )
        
    def run(self):
        self.markdown_files = self.files_finder.get_files()

        for file in self.markdown_files:
            content = ""

            print(f"Se lee {file}")
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            #self.template_formatter = SequenceFormatter(content)
            #new_content = self.template_formatter.get_formatted_markdown_text()
            self.template_formatter = TemplateFormatter(content)
            fixed_sigleline = self.template_formatter.reorder_singleline_quiz()
            
            self.template_formatter = TemplateFormatter(fixed_sigleline)
            fixed_template_content = self.template_formatter.format_multiline_quiz()
            
            self.sequence_formatter = SequenceFormatter(fixed_template_content)
            new_content = self.sequence_formatter.get_formatted_text()
            # new_content = self.template_formatter.test_multiple_line_numerals()
            
            print(f"Se escribe {file}")
            with open(file, 'w', encoding='utf-8') as f2:
                f2.write(new_content)