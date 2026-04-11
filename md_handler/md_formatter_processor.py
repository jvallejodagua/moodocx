# -*- coding: utf-8 -*-
# md_formatter_processor.py

import re
from md_handler.md_formatter import MdFormatter
from md_handler.template_formatter import TemplateFormatter
from filesystem.files_finder import FilesInSubfolder
import time

class MdFormatterProcessor:
    
    def __init__(self, source_directory: str):
        self.markdown_formater = None
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
            
            #self.markdown_formater = MdFormatter(content)
            #new_content = self.markdown_formater.get_formatted_markdown_text()
            self.markdown_formater = TemplateFormatter(content)
            new_content = self.markdown_formater.fix_quiz_multiple_line_numerals()
            
            print(f"Se escribe {file}")
            with open(file, 'w', encoding='utf-8') as f2:
                f2.write(new_content)