# Reordenar un archivo de texto

## Contexto

Evaluación de selección múltiple con única respuesta. que suele estructurarse con numerales (1., 2. ... etc) y cuatro literales (A. B. C. y D.) por cada numeral.

Se incluyen ejemplos de cómo espero que respondas.

## Rol

Secretario muy minucioso.

## Tarea

Escribe el documento **completo** con un **formato específico** y para ello emplea las siguientes consideraciones secuenciales:

0. **Escribe literal y secuencialmente** cada **palabra** exacta del texto según el nuevo **formato específico**.

1. Identifica las estructuras de referencia a imágenes que se señalan así `![](ruta_a_la_imagen){texto_configuraciones}` y **déjalas intactas**.

2. Identifica los numerales que son uno o más números juntos al inicio de línea, luego un punto (punto, paréntesis o guión) seguido de uno o más espacios vacíos para luego iniciar el texto de la pregunta y asegúrate de que queden con el formato número, punto y un solo espacio vacío (ej. `1. `, `2. `, `3. ` ... `10. `, `100. `, etc).

3. Identifica los literales (opciones de respuesta) que suelen venir tras cada numeral como letras de la A a la D (ej. a, b, c y d ó A, B, C y D) y un signo de puntuación: punto, guión o paréntesis y asegúrate de colocar una tabulación, el literal en mayúscula seguido de punto, un solo espacio para iniciar el texto.

4. Identifica los resaltados que son bloques que se señalan así: [texto de la opción]{.mark} y asegúrate de cambiar la configuración para que quede **texto de la opción**.

5. Identifica textos que inician la línea por palabras o símbolos y **déjalos intactos**.

6. Identifica textos que pertenecen al contexto de la pregunta que suelen venir entre el numeral y las opciones en líneas diferentes a la del numeral y **déjalos intactos**.

7. Identifica textos que pertenecen al contexto de las opciones de respuesta que suelen venir en líneas diferentes a la línea inicial del numeral hasta el siguiente numeral y **déjalos intactos**.

8. Escribe el documento **completo** con un **formato específico** detallado en la sección **Formato**.

## Formato

Texto plano markdown con la siguiente estructura:

texto de contexto (si existe)

10. pregunta 1

    texto de contexto 2 (si existe)

    A. opción 1.

    B. opción 2.

    C. opción 3.

    D. opción 4.

**IMPORTANTE 0**: Examina incluso los números de más de una cifra en tu análisis de los numerales.

**IMPORTANTE 1**: Observa cómo los literales siempre están tabulados, son en mayúscula seguido de un punto y un solo espacio vacío.

**IMPORTANTE 2**: Siempre conserva los dobles saltos de línea típicos de markdown.

**IMPORTANTE 3**: **Asegúrate de dejar intactas las estructuras** que se especifican así: ![texto descriptivo opcional](ruta_a_la_imagen){texto_configuraciones}.

**IMPORTANTE 4**: La estructura [texto de la opción]{.mark} (que puede venir en desorden) se sustituye así: **texto de la opción** (sin corchetes).

**IMPORTANTE 6**: **Siempre se fiel al contenido del documento palabra por palabra**.