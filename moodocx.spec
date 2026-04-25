# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['moodocx.py'],
    pathex=['.'],
    binaries=[],
    datas=[('pandoc_handler/flatten_tables.lua', 'pandoc_handler')],
    hiddenimports=['pycparser.lextab', 'pycparser.yacctab', 'pandoc_handler', 'html_css_handler', 'json_handler', 'latex_handler', 'md_handler', 'xml_handler', 'filesystem', 'data_models'],
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
