# -*- coding: utf-8 -*-
# files_finder.py

from pathlib import Path
import shutil
import time

class FilesAbstract:

    def __init__(self):
        self.files_path = None
        self.compile_path = None
        self.images_prefix = "Imagenes"
        self.files = []

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
    
    def make_no_space_stem(self, file_path: Path):
        stem_name = file_path.stem
        return stem_name.replace(" ", "")
    
    def create_compile_dir(self):
        self.compile_path.mkdir(exist_ok=True)

    def remove_compile_dir(self):
        if self.compile_path.exists() and self.compile_path.is_dir():
            shutil.rmtree(self.compile_path)
    
    def copy_directory(self, from_path: Path, to_path: Path):
        shutil.copytree(from_path, to_path, dirs_exist_ok=True)

class FilesInSubfolder(FilesAbstract):

    def __init__(self, files_path: Path, suffix_extension: str):
        super().__init__()
        self.files_path = files_path
        self.files_path.mkdir(exist_ok=True)
        self.suffix_extension = suffix_extension
        self.compile_path = files_path / "__compile_workshop"

    def get_files(self):
        
        print("Buscando archivos "+self.suffix_extension+"...")

        self.files = list(self.files_path.glob(f"*{self.suffix_extension}"))
        
        for counter, file in enumerate(self.files):
            self.files[counter] = file.absolute()

        if self.files:
            print(f"Se encontraron {len(self.files)} archivo(s) {self.suffix_extension}")
            
        else:
            print(f"No se encontraron archivos {self.suffix_extension} en el directorio.")
            
        return self.files

class FilesChecker(FilesAbstract):
    
    def __init__(self, files_path: Path):
        super().__init__()
        self.files_path = files_path
        self.compile_path = files_path / "__compile_workshoop"

if __name__ == "__main__":
    a = FilesChecker
    mas = Path("path_latex_windows.py")

    a.file_exists(mas)