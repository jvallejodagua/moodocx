# -*- coding: utf-8 -*-
# md_formatter_processor.py

import re
import time
from pathlib import Path
from md_handler.sequence_formatter import SequenceFormatter
from md_handler.template_formatter import TemplateFormatter
from md_handler.template_formatter import FormatterAbstract
from md_handler.sanitizer_formatter import SanitizerFormatter
from md_handler.ai_md_formatter import AIMdFormatter
from filesystem.files_finder import FilesInSubfolder

class MdFormatterProcessor:
    
    def __init__(self, inputs_path: Path, outputs_path: Path):
        self.formatter_abstract = FormatterAbstract()
        self.sanitizer_formatter = None
        self.ai_md_formatter = None
        self.template_formatter = None
        self.sequence_formatter = None
        self.files_finder = FilesInSubfolder(
            files_path = inputs_path,
            suffix_extension = ".md",
        )
        self.inputs_path = inputs_path
        self.outputs_path = outputs_path
        self.content = ""
        
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
            
            #self.sanitizer_formatter = SanitizerFormatter(self.content)
            #self.content = self.sanitizer_formatter.sanitize_text()
            
            self.ai_md_formatter = AIMdFormatter(self.content)
            self.content = self.ai_md_formatter.get_formatted_text_ai()

            self.template_formatter = TemplateFormatter(self.content)
            self.content = self.template_formatter.format_multiline_quiz()
            
            self.sequence_formatter = SequenceFormatter(self.content)
            self.content = self.sequence_formatter.get_formatted_text()
            
            output_file = self.outputs_path / file.name
            no_space_stem = self.files_finder.make_no_space_stem(file)
            images_prefix = self.files_finder.images_prefix
            image_dir_name = f'{images_prefix}-{no_space_stem}'
            
            media_input_folder = self.inputs_path / image_dir_name
            media_output_folder = self.outputs_path / image_dir_name

            print(f"Se escribe {output_file}")
            with open(output_file, 'w', encoding='utf-8') as f2:
                f2.write(self.content)
            
            self.files_finder.copy_directory(
                from_path = media_input_folder,
                to_path = media_output_folder
            )
    
    def add_optative_pandoc_comment(self, content):
        pandoc_comment = self.formatter_abstract.pandoc_comment_raw
        if pandoc_comment in content:
            return f'{content}\n{pandoc_comment}\n'
        else:
            return content
