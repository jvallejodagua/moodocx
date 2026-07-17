# -*- coding: utf-8 -*-
# files_finder.py

from pathlib import Path
import shutil
import time
import sys

class FilesAbstract:

    def __init__(self):
        self.files_path = None
        self.inputs_path = None
        self.outputs_path = None
        self.compile_path = None
        self.images_prefix = "Imagenes"
        self.compile_dir_name = "__compile_workshop"
        self.files = []
    
    def resolve_user_folder_path(self, relative_path: str | Path):

        if getattr(sys, 'frozen', False):
            self_path = Path(sys.executable).resolve().parent.absolute()
        else:
            self_path = Path(__file__).resolve().parent.parent.absolute()
            
        return self_path / relative_path

    def resolve_internal_path(self, relative_path: str | Path):
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            base_path = Path(sys._MEIPASS)
        else:
            base_path = Path(__file__).resolve().parent.parent

        return base_path / relative_path

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

    def run(self):
        input_folder_path = Path(self.resolve_user_folder_path("_Entradas"))
        output_folder_path = Path(self.resolve_user_folder_path("_Salidas"))
        
        for item in input_folder_path.rglob('*'):
            ruta_relativa = item.relative_to(input_folder_path)
            final_path = output_folder_path / ruta_relativa
            
            if item.is_dir():
                final_path.mkdir(parents=True, exist_ok=True)
            else:
                # Asegurar que la estructura de directorios exista antes de procesar el archivo
                final_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Regla de negocio: Sincronización basada en st_mtime
                if final_path.exists():
                    mtime_origen = item.stat().st_mtime
                    mtime_destino = final_path.stat().st_mtime
                    
                    # Cortocircuito: Si el archivo destino es idéntico en fecha o más reciente, saltamos la copia
                    if mtime_destino >= mtime_origen:
                        continue
                
                # Ejecutamos la copia nativa desde el objeto Path preservando los metadatos (mtime)
                item.copy(final_path, preserve_metadata=True)

class FolderCleaner(FilesAbstract):

    def __init__(self):
        super().__init__()

    def delete_empty_folder(self, folder_path: Path):
        for current_root, dirs, _ in folder_path.walk(top_down=False):
            for directory in dirs:
                dir_to_check = current_root / directory
                try:
                    dir_to_check.rmdir()
                    print(f"[+] Directorio podado: {dir_to_check.resolve()}")
                except OSError:
                    pass        

    def run(self):
        input_folder_path = Path(self.resolve_user_folder_path("_Entradas"))
        output_folder_path = Path(self.resolve_user_folder_path("_Salidas"))
        self.delete_empty_folder(input_folder_path)
        self.delete_empty_folder(output_folder_path)

class SimpleLogger(FilesAbstract):
    pass


if __name__ == "__main__":
    a = FilesChecker
    mas = Path("path_latex_windows.py")

    a.file_exists(mas)