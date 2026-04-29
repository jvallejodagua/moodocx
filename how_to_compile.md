# Cómo compilar

Para compilar el código fuente en ejecutables viables es necesario compilar llama_cpp con vulkan habilitado en la máquina donde se va a compilar.
Dicha compilación genera un resultado en el entorno virtual que se referencia automáticamente en el archivo .spec.

## Linux

Se debe verificar que los archivos de flet estén disponibles para ejecutar como programas:
chmod +x /home/johan/.flet/client/flet-desktop-light-0.84.0/flet/lib/*.so

Se ejecuta la compilación:
pyinstaller moodocx.spec

## Windows

pyinstaller moodocx.spec