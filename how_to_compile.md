# Cómo compilar

## Linux

Se debe verificar que los archivos de flet estén disponibles para ejecutar como programas:
chmod +x /home/johan/.flet/client/flet-desktop-light-0.84.0/flet/lib/*.so

Se ejecuta la compilación:
pyinstaller moodocx.spec

## Windows

pyinstaller moodocx.spec