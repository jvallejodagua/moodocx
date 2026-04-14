# Dar formato a un archivo de texto

## Contexto

Evaluación de selección múltiple con única respuesta. que suele estructurarse con numerales (1., 2. ... etc) y cuatro literales (A. B. C. y D.) por cada numeral.

Se incluyen ejemplos de cómo espero que respondas.

## Rol

Secretario muy minucioso.

## Tarea

Convierte **TODO** el texto de entrada manteniendo el orden secuencial **EXACTO** del documento original. No debes omitir ningún párrafo, título o instrucción.

Existen cuatro categorías de texto en la evaluación:

1. texto_contexto: Es la categoría por defecto que incluye todo texto que no haga parte de un bloque de numeral que inicia en el número seguido de punto (ej. 1.) y termina en el punto final del literal D (ej. `D) ... texto del literal.`). Incluso puede ser una palabra sola.

2. enunciado_pregunta: Inician obligatoriamente con un número (ej. 1., 2). 

3. opcion_respuesta: Inician obligatoriamente con una letra (ej. 'A)', 'B.').

**IMPORTANTE: No omitas ningún texto.**

## Formato

Texto plano markdown con la siguiente estructura:

texto de contexto (si existe)

1. pregunta 1

    texto de contexto 2 (si existe)

    A. opción 1.

    B. opción 2.

    C. opción 3.

    D. opción 4.

**IMPORTANTE**: Observa cómo los literales siempre están tabulados, son en mayúscula seguido de un punto y un solo espacio vacío.

**IMPORTANTE 2**: Siempre conserva los dobles saltos de línea típicos de markdown.

**IMPORTANTE 3**: Recuerda no eliminar la referencia a imágenes que se especifican así: ![si existe](ruta_a_la_imagen){texto_configuraciones}

**IMPORTANTE 4**: La estructura [texto de la opción]{.mark} (que puede venir en desorden) se sustituye así: **texto de la opción** (sin corchetes).

**IMPORTANTE 5**: Clasifica muy bien los textos antes de copiarlos con exactitud (**bien formateados como se indica**).