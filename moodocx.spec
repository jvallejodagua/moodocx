# -- mode: python ; coding: utf-8 --

import os
import platform
import llama_cpp # Aún lo necesitamos para ubicar el código python puro

# 1. Detectar el sistema operativo en tiempo de empaquetado (Build time)
sys_os = platform.system()

# 2. Definir los binarios a empaquetar de forma condicional
custom_binaries = []
if sys_os == 'Linux':
    print(">>> Empaquetando para Arch Linux: Usando binarios personalizados .so")
    custom_binaries = [
        # (origen relativo a donde ejecutas pyinstaller, destino dentro del empaquetado)
        (r'/home/johan/_virtualP/lib/python3.14/site-packages/llama_cpp/lib/*.so', 'llama_cpp'),
        (r'/home/johan/_virtualP/lib/python3.14/site-packages/llama_cpp/lib/*.so', 'llama_cpp/lib') # Respaldo para versiones recientes del wrapper
    ]
elif sys_os == 'Windows':
    print(">>> Empaquetando para Windows 11: Usando binarios personalizados .dll")
    custom_binaries = [
        (r'C:/_virtualP/Lib/site-packages/llama_cpp/lib/*.dll', 'llama_cpp'),
        (r'C:/_virtualP/Lib/site-packages/llama_cpp/lib/*.dll', 'llama_cpp/lib')
    ]
else:
    print(f">>> Sistema operativo no soportado por esta configuración: {sys_os}")

# 3. Ubicar la ruta del paquete de Python puro
llama_cpp_path = os.path.dirname(llama_cpp._file_)

a = Analysis(
    ['moodocx.py'],
    pathex=['.'],
    binaries=custom_binaries,
    datas=[
        (llama_cpp_path, 'llama_cpp'),
        ('md_handler/example1.md', 'md_handler'),
        ('md_handler/example2.md', 'md_handler'),
        ('md_handler/expected_output1.md', 'md_handler'),
        ('md_handler/expected_output2.md', 'md_handler'),
        ('md_handler/system_prompt.md', 'md_handler'),
        ('pandoc_handler/flatten_tables.lua', 'pandoc_handler'),
        ('C:\\Windows\\System32\\vulkan-1.dll', '.'), # Pone vulkan en la raíz del exe
        ('C:\\Windows\\System32\\vcruntime140.dll', '.'),
        ('C:\\Windows\\System32\\vcruntime140_1.dll', '.'),
    ],
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
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='logo_moodocx.ico',
)