# -*- coding: utf-8 -*-
# files_finder.py

from pathlib import Path

class FilesInSubfolder:

    def __init__(self, route_to_subfolder: Path, suffix_extension: str):
        self.files_path = route_to_subfolder
        self.files_path.mkdir(exist_ok=True)
        self.suffix_extension = suffix_extension

    def get_files(self):
        
        print("Buscando archivos "+self.suffix_extension+"...")

        _files = list(self.files_path.glob(f"*{self.suffix_extension}"))
        
        for counter, file in enumerate(_files):
            _files[counter] = file.absolute()

        if _files:
            print(f"Se encontraron {len(_files)} archivo(s) {self.suffix_extension}")
            
        else:
            print(f"No se encontraron archivos {self.suffix_extension} en el directorio.")
            
        return _files