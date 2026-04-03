# -*- coding: utf-8 -*-
# path_latex_windows.py

import os
import shutil
from pathlib import Path

def get_system_path_executable(executable_name: str) -> str | None:
    return shutil.which(executable_name)

def get_local_appdata_directory() -> Path | None:
    local_appdata = os.getenv("LOCALAPPDATA")
    if not local_appdata:
        return None
    return Path(local_appdata)

def build_miktex_executable_path(base_directory: Path) -> Path:
    return base_directory / "Programs" / "MiKTeX" / "miktex" / "bin" / "x64" / "pdflatex.exe"

def verify_executable_exists(file_path: Path) -> bool:
    return file_path.is_file() and os.access(file_path, os.X_OK)

def get_miktex_local_executable() -> str | None:
    local_appdata_path = get_local_appdata_directory()
    if not local_appdata_path:
        return None
        
    pdflatex_path = build_miktex_executable_path(local_appdata_path)
    if verify_executable_exists(pdflatex_path):
        return str(pdflatex_path)
        
    return None

def resolve_pdflatex_path() -> str:
    system_executable = get_system_path_executable("pdflatex")
    if system_executable:
        return system_executable
        
    local_executable = get_miktex_local_executable()
    if local_executable:
        return local_executable
        
    raise FileNotFoundError("The pdflatex executable could not be found in the system.")