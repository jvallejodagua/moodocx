# -*- coding: utf-8 -*-
# files_finder.py

from pathlib import Path
import time

class FilesAbstract:
    def file_exists(self, file_path, time_out_s=600):
        init_time = time.time()

        while (time.time() - init_time) < time_out_s:
            if file_path.exists():
                if file_path.stat().st_size > 0:
                    print(file_path.name," Ubicado con éxito")
                    return True
            time.sleep(0.5)
        
        print(file_path.name," No se generó")
        return False

class FilesInSubfolder(FilesAbstract):

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

class FilesChecker(FilesAbstract):
    pass

if __name__ == "__main__":
    a = FilesChecker
    mas = Path("path_latex_windows.py")

    a.file_exists(mas)