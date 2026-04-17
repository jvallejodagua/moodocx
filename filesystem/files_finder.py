# -*- coding: utf-8 -*-
# files_finder.py

from pathlib import Path
import shutil
import time

class FilesAbstract:

    def __init__(self):
        self.files_path = None
        self.inputs_path = None
        self.outputs_path = None
        self.compile_path = None
        self.images_prefix = "Imagenes"
        self.compile_dir_name = "__compile_workshop"
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
    
    def get_process_tag(self, tag):
        return f'"\n\n::: --------- {tag} --------- :::\n\n"'

    def make_no_space_stem(self, file_path: Path):
        stem_name = file_path.stem
        return stem_name.replace(" ", "")
    
    def create_compile_dir(self):
        self.compile_path.mkdir(exist_ok=True)

    def remove_compile_dir(self):
        if self.compile_path.exists() and self.compile_path.is_dir():
            shutil.rmtree(self.compile_path)
    
    def copy_directory(self, from_path: Path, to_path: Path):
        if from_path.exists() and from_path.is_dir():
            shutil.copytree(from_path, to_path, dirs_exist_ok=True)

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

class FilesInSubfolder(FilesAbstract):

    def __init__(self, files_path: Path, suffix_extension: str):
        super().__init__()
        self.files_path = files_path
        self.files_path.mkdir(exist_ok=True)
        self.suffix_extension = suffix_extension
        self.compile_path = files_path / self.compile_dir_name

class FilesChecker(FilesAbstract):
    
    def __init__(self, files_path: Path):
        super().__init__()
        self.files_path = files_path
        self.compile_path = files_path / self.compile_dir_name
    

class FilesManager(FilesAbstract):

    def __init__(self, inputs_path: Path, outputs_path: Path):
        super().__init__()
        self.files_path = inputs_path
        self.compile_path = outputs_path / self.compile_dir_name
        self.inputs_path = inputs_path
        self.outputs_path = outputs_path
        self.suffix_extension = ".md"

    # Copia los archivos md del directorio de entradas a salidas
    def run(self):
        self.markdown_files = self.get_files()
        tag_text = f"Copia md: {self.inputs_path.stem} hacia {self.outputs_path.stem}"
        tag = self.get_process_tag(tag_text)
        print(tag)

        for file in self.markdown_files:
            self.content = ""

            print(f"Se lee {file}")
            with open(file, 'r', encoding='utf-8') as f:
                self.content = f.read()
            
            output_file = self.outputs_path / file.name
            no_space_stem = self.make_no_space_stem(file)
            images_prefix = self.images_prefix
            image_dir_name = f'{images_prefix}-{no_space_stem}'
            
            media_input_folder = self.inputs_path / image_dir_name
            media_output_folder = self.outputs_path / image_dir_name

            print(f"Se escribe {output_file}")
            with open(output_file, 'w', encoding='utf-8') as f2:
                f2.write(self.content)
            
            self.copy_directory(
                from_path = media_input_folder,
                to_path = media_output_folder
            )
    
class SimpleLogger(FilesAbstract):
    pass


if __name__ == "__main__":
    a = FilesChecker
    mas = Path("path_latex_windows.py")

    a.file_exists(mas)