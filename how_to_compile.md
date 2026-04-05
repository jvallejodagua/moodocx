# Cómo compilar

## Linux

Se debe verificar que los archivos de flet estén disponibles para ejecutar como programas:
chmod +x /home/johan/.flet/client/flet-desktop-light-0.84.0/flet/lib/*.so

Se ejecuta la compilación:
pyinstaller --onefile --windowed \
--paths="." \
--hidden-import=pycparser.lextab \
--hidden-import=pycparser.yacctab \
--hidden-import=pandoc_handler \
--hidden-import=html_css_handler \
--hidden-import=json_handler \
--hidden-import=latex_handler \
--hidden-import=md_handler \
--hidden-import=xml_handler \
--hidden-import=filesystem \
moodocx.py

## Windows

pyinstaller --onefile --windowed --icon=logo_moodocx.ico --paths="." --hidden-import=pycparser.lextab --hidden-import=pycparser.yacctab --hidden-import=pandoc_handler --hidden-import=html_css_handler --hidden-import=json_handler --hidden-import=latex_handler --hidden-import=md_handler --hidden-import=xml_handler --hidden-import=filesystem moodocx.py