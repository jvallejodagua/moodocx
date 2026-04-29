# -*- mode: python ; coding: utf-8 -*-

import os
import platform
import llama_cpp 

sys_os = platform.system()

llama_cpp_path = os.path.dirname(llama_cpp.__file__)

custom_binaries = []

# Archivos base (Data) que se empaquetan sin importar el SO
custom_datas = [
    (llama_cpp_path, 'llama_cpp'),
    ('md_handler/example1.md', 'md_handler'),
    ('md_handler/example2.md', 'md_handler'),
    ('md_handler/expected_output1.md', 'md_handler'),
    ('md_handler/expected_output2.md', 'md_handler'),
    ('md_handler/system_prompt.md', 'md_handler'),
    ('pandoc_handler/flatten_tables.lua', 'pandoc_handler'),
]

# Lógica Condicional de Sistema Operativo
if sys_os == 'Linux':
    print(">>> Empaquetando para Linux: Usando binarios dinámicos .so")
    custom_binaries = [
        (os.path.join(llama_cpp_path, 'lib', r'*.so'), 'llama_cpp'),
        (os.path.join(llama_cpp_path, 'lib', r'*.so'), 'llama_cpp/lib') 
    ]
elif sys_os == 'Windows':
    print(">>> Empaquetando para Windows: Usando binarios dinámicos .dll")
    custom_binaries = [
        (os.path.join(llama_cpp_path, 'lib', r'*.dll'), 'llama_cpp'),
        (os.path.join(llama_cpp_path, 'lib', r'*.dll'), 'llama_cpp/lib')
    ]
    
    custom_datas.extend([
        ('C:\\Windows\\System32\\vulkan-1.dll', '.'),
        ('C:\\Windows\\System32\\vcruntime140.dll', '.'),
        ('C:\\Windows\\System32\\vcruntime140_1.dll', '.'),
    ])
else:
    print(f">>> Sistema operativo no soportado por esta configuración: {sys_os}")


a = Analysis(
    ['moodocx.py'],
    pathex=['.'],
    binaries=custom_binaries,
    datas=custom_datas, # Se usa el array dinámico
    hiddenimports=['pycparser.lextab', 'pycparser.yacctab', 'pandoc_handler', 'html_css_handler', 'json_handler', 'latex_handler', 'md_handler', 'xml_handler', 'filesystem', 'data_models', 'llama_cpp'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='moodocx',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False, # Como nota: Si crashea llama_cpp en Linux, temporalmente pon esto en True para ver el traceback
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='logo_moodocx.ico', # PyInstaller en Linux simplemente ignorará el icono sin generar error.
)