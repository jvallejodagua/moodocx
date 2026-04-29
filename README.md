# Moodocx

Conversor de documentos de word (.docx) y markdown (.md) a moodle para importar (.xml), escrito en Python, con soporte para ecuaciones y tablas insertables como imágenes.(empleando LaTeX).

Destaca su principal uso para la conversión de cuestionarios tipo pruebas saber 11 con numerales y cuatro opciones de pregunta (A., B., C. y D.). Bajo ciertas condiciones también con textos reutilizables.

## Tipos de estructura de documento

Se diseña en especial para las estructuras esquematizadas en esta sección (sin estar limitado su uso si se desea otra aplicación como ordenar listas numéricas en un documento de word u otras).

### Lista de preguntas y respuestas

Título del estímulo [nivel 1, 2, 3, ... 6] (opcional)

Texto del estímulo (opcional)

1. Estímulo de la pregunta.

    Imagen de la pregunta (si existe)

    Prompt de la tarea.
    
    A. opción 1.

    B. opción 2.

    C. opción 3.

    D. opción 4.

Título del estímulo [nivel 1, 2, 3, ... 6] (opcional)

Texto del estímulo (opcional)

2. Demás numerales.

### Estímulos compartidos y preguntas

Título del estímulo 1 [nivel 1, 2, 3, ... 6] (opcional)

Texto del estímulo 1 (opcional)

1. Según el Estímulo 1 ...

2. Según el Estímulo 1 ...

Título del estímulo 2 [nivel 1, 2, 3, ... 6] (opcional)

Texto del estímulo 2 (opcional)

3. Según el Estímulo 2 ...

4. Según el Estímulo 2 ...

## Cómo instalar (ejecutable) o ejecutar (código fuente)

Existen algunos prerrequisitos clave para la instalación ó ejecución exitosa del software que deben ser tenidos en cuenta.

### Instalación y Ejecución

Descargue el archivo de la IA generativa sintonizada para español en el enlace:

[https://huggingface.co/hugoramallo/gemma-4-ria-spanish-finetune/tree/main](https://huggingface.co/hugoramallo/gemma-4-ria-spanish-finetune/tree/main)

Archivo .gguf de 5Gb aproximadamente. Debe ser ubicado junto al ejecutable moodocx.exe ó moodocx.run

#### pandoc

##### Windows

Descargue pandoc del enlace (Archivo .msi):

[https://github.com/jgm/pandoc/releases](https://github.com/jgm/pandoc/releases)

##### Linux

Suele estar en el repositorio del sistema.

#### LaTeX

##### Windows

Descargue e instale strawberry perl:

[https://strawberryperl.com](https://strawberryperl.com)

Descargue e instale la distribución de MikTeX (pestaña installer):

[https://miktex.org/download](https://miktex.org/download)

Nota: No emplee versión portable.

##### Linux

Instale perl desde el repositorio del sistema

Descargue e instale siguiendo las instrucciones de la sección "tl;dr: Unix(ish)":

[https://www.tug.org/texlive/quickinstall.html](https://www.tug.org/texlive/quickinstall.html)


### Ejecución del código fuente

1. Instale un entorno virtual python.
2. Instale las dependencias usando el comando: ruta_a_entornovirtual/pip install asyncio wheel python-docx panflute flet[all] bs4 PIL pypdfium2
3. Ejecute el programa: ruta_a_entornovirtual/python3 moodocx.py

### Ejecutable (Ver la sección de releases)

Se ubica en un directorio que se desee para trabajar con la aplicación y se hace doble click (los usuarios linux deben asegurar el permiso de ejecución). Automáticamente el programa creará dos directorios "_Entradas" y "_Salidas".

En la carpeta "_Entradas" se ubican los archivos de .docx o markdown que se quieran convertir. (El sistema automáticamente convierte docx a markdown y lo ubican en la misma carpeta de _Entradas). También se crea en "_Entradas" una carpeta para las imágenes contenidas originalmente en el archivo de .docx.

En la carpeta "_Salidas" se ubican los archivos generados con el mismo nombre de los archivos originales pero que contienen las modificaciones que se desee aplicar en la interfaz gráfica de la aplicación.

## Cómo usarlo

1. Los documentos docx ó markdown que se quieran convertir - transformar se deben colocar en la carpeta "_Entradas" al interior del directorio del programa (En caso de borrarse dicha carpeta se puede crear o dejar que el sistema la cree).

Carpeta de Moodocx

|___Moodocx.exe

|___ _Entradas

|___ _Salidas

Carpeta de moodocx

|___moodocx.py

|___ _Entradas

|___ _Salidas

2. Seleccionar las opciones (Se recomienda no enviar directamente con la opción moodle para verificar previamente el docx que se procesará).

3. Presionar el botón "Convertir".

3. Una vez verificado el archivo se puede desmarcar todas las opciones y seleccionar la opción de convertir a Moodle para que el archivo verificado sea convertido a xml Moodle.

**Nota**: En caso de requerir *Generar reutilización del estímulo* se produce un archivo adicional que se rotula -modificado.docx para que el estímulo se adhiera a cada pregunta que sigue en el cuestionario hasta el siguiente texto de estímulo. En caso de requerir algunas preguntas sin reutilizar el estímulo y otras sí entonces es preciso hacer una mezcla manual de ambos archivos antes de producir el xml de Moodle.