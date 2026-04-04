# Moodocx

Conversor de documentos de word (.docx) y markdown (.md) a moodle para importar (.xml), escrito en Python, con soporte para ecuaciones y tablas insertables como imágenes.(empleando LaTeX).

Destaca su principal uso para la conversión de cuestionarios tipo pruebas saber 11 con numerales y cuatro opciones de pregunta (A., B., C. y D.). Bajo ciertas condiciones también con textos reutilizables.

## Tipos de estructura de documento

Se diseña en especial para las estructuras esquematizadas en esta sección (sin estar limitado su uso si se desea otra aplicación como ordenar listas numéricas en un documento de word u otras).

### Lista de preguntas y respuestas

1. Estímulo de la pregunta.
    Imagen de la pregunta (si existe)
    Prompt de la tarea.
    
    A. opción 1.

    B. opción 2.

    C. opción 3.

    D. opción 4.

2. Demás numerales.

### Estímulos compartidos y preguntas

Estímulo 1.

1. Según el Estímulo 1 ...

2. Según el Estímulo 1 ...

Estímulo 2.

3. Según el Estímulo 2 ...

4. Según el Estímulo 3 ...

## Cómo instalar (ejecutable) o ejecutar (código fuente)

Existen algunos prerrequisitos clave para la instalación ó ejecución exitosa del software que deben ser tenidos en cuenta.

### Instalación y Ejecución

#### pdftocairo 

##### Windows

Descargue pdftocairo del enlace (se encuentra como un .exe dentro del comprimido):

![https://github.com/oschwartz10612/poppler-windows/releases](https://github.com/oschwartz10612/poppler-windows/releases)

Luego se ubica apropiadamente en una carpeta que difícilmente se elimine por error y se configura su acceso con el nombre pdftocairo en las variables de entorno.

##### Linux

Suele estar en el repositorio del sistema.

#### pandoc

##### Windows

Descargue pandoc del enlace (Archivo .msi):

![https://github.com/jgm/pandoc/releases](https://github.com/jgm/pandoc/releases)

##### Linux

Suele estar en el repositorio del sistema.

#### LaTeX

##### Windows

Descargue e instale strawberry perl:

![https://strawberryperl.com/](https://strawberryperl.com/)

Descargue e instale la distribución de MikTeX (pestaña installer):

![https://miktex.org/download](https://miktex.org/download)

Nota: No emplee versión portable.

##### Linux

Instale perl desde el repositorio del sistema

Descargue e instale siguiendo las instrucciones de la sección "tl;dr: Unix(ish)":

![https://www.tug.org/texlive/quickinstall.html](https://www.tug.org/texlive/quickinstall.html)


### Ejecución del código fuente

1. Instale un entorno virtual python.
2. Instale las dependencias usando el comando: ruta_a_entornovirtual/pip install asyncio wheel python-docx panflute flet[all] bs4
3. Ejecute el programa: ruta_a_entornovirtual/python3 moodocx.py

### Ejecutable (No disponible aún)

Descomprima el directorio y úselo.

## Cómo usarlo

1. Los documentos docx ó markdown que se quieran convertir - transformar se deben colocar en la carpeta Temporales al interior del directorio del programa (En caso de borrarse dicha carpeta se puede crear o dejar que el sistema la cree).

Carpeta de Moodocx

|___Moodocx.exe

|___Temporales

Carpeta de moodocx

|___moodocx.py

|___Temporales

2. Seleccionar las opciones (Se recomienda no enviar directamente con la opción moodle para verificar previamente el docx que se procesará).

3. Presionar el botón "Convertir".

3. Una vez verificado el archivo se puede desmarcar todas las opciones y seleccionar la de convertir a moodle.

**Nota**: En caso de requerir *Generar reutilización del estímulo* se produce un archivo adicional que se rotula -modificado.docx para que el estímulo se adhiera a cada pregunta que sigue en el cuestionario hasta el siguiente texto de estímulo. En caso de requerir algunas preguntas sin reutilizar el estímulo y otras sí entonces es preciso hacer una mezcla manual de ambos archivos.