# -*- coding: utf-8 -*-
# md_formatter_processor.py

import re
import time
from pathlib import Path
from md_handler.formatter_abstract import FormatterAbstract
from md_handler.sanitizer_formatter import SanitizerFormatter
from filesystem.files_finder import FilesInSubfolder

class MdFormatterProcessor:
    
    def __init__(self, inputs_path: Path, outputs_path: Path, is_collapsed_content):
        self.formatter_abstract = FormatterAbstract()
        self.sanitizer_formatter = None
        self.template_formatter = None
        self.sequence_formatter = None
        self.files_finder = FilesInSubfolder(
            files_path = inputs_path,
            suffix_extension = ".md",
        )
        self.inputs_path = inputs_path
        self.outputs_path = outputs_path
        self.content = ""
        self.is_collapsed_content = is_collapsed_content
        
    def run(self):
        input_name = self.inputs_path.stem
        output_name = self.outputs_path.stem
        tag_text = f"Formateando md en {input_name} -> {output_name}"
        tag = self.files_finder.get_process_tag(tag_text)
        print(tag)

        self.markdown_files = self.files_finder.get_files()

        for file in self.markdown_files:
            self.content = ""

            print(f"Se lee {file}")
            with open(file, 'r', encoding='utf-8') as f:
                self.content = f.read()
            
            #self.template_formatter = SequenceFormatter(content)
            #new_content = self.template_formatter.get_formatted_markdown_text()
            self.content = self.add_optative_pandoc_comment(self.content)
            
            self.sanitizer_formatter = SanitizerFormatter(self.content, self.is_collapsed_content)
            self.content = self.sanitizer_formatter.sanitize_text()
            
            output_file = self.outputs_path / file.name
            print(f"Se escribe {output_file}")
            with open(output_file, 'w', encoding='utf-8') as f2:
                f2.write(self.content)
                
    def add_optative_pandoc_comment(self, content):
        pandoc_comment = self.formatter_abstract.pandoc_comment_raw
        if pandoc_comment in content:
            return f'{content}\n{pandoc_comment}\n'
        else:
            return content
