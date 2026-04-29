# Cómo compilar

Para compilar el código fuente en ejecutables viables es necesario compilar llama_cpp con vulkan habilitado en la máquina donde se va a compilar.
Dicha compilación genera un resultado en el entorno virtual que debe ser referenciado en el archivo .spec.

## Archivo .spec

Se sugiere copiar este contenido y modificar /ruta/al/archivo según corresponda.

# -*- mode: python ; coding: utf-8 -*-

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
        ('/ruta/al/archivo/llama_cpp/lib/*.so', 'llama_cpp'),
        ('/ruta/al/archivo/llama_cpp/lib/*.so', 'llama_cpp/lib') # Respaldo para versiones recientes del wrapper
    ]
elif sys_os == 'Windows':
    print(">>> Empaquetando para Windows 11: Usando binarios personalizados .dll")
    custom_binaries = [
        ('/ruta/al/archivo/windows/*.dll', 'llama_cpp'),
        ('/ruta/al/archivo/windows/*.dll', 'llama_cpp/lib')
    ]
else:
    print(f">>> Sistema operativo no soportado por esta configuración: {sys_os}")

# 3. Ubicar la ruta del paquete de Python puro
llama_cpp_path = os.path.dirname(llama_cpp.__file__)

a = Analysis(
    ['moodocx.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        (llama_cpp_path, 'llama_cpp'),
        ('md_handler/example1.md', 'md_handler'),
        ('md_handler/example2.md', 'md_handler'),
        ('md_handler/expected_output1.md', 'md_handler'),
        ('md_handler/expected_output2.md', 'md_handler'),
        ('md_handler/system_prompt.md', 'md_handler'),
        ('pandoc_handler/flatten_tables.lua', 'pandoc_handler'),
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
)


## Linux

Se debe verificar que los archivos de flet estén disponibles para ejecutar como programas:
chmod +x /home/johan/.flet/client/flet-desktop-light-0.84.0/flet/lib/*.so

Se ejecuta la compilación:
pyinstaller moodocx.spec

## Windows

pyinstaller moodocx.spec