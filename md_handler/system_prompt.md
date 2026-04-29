# Reordenar un archivo de texto

## Contexto

Evaluación de selección múltiple con única respuesta que suele estructurarse con numerales (1., 2. ... etc) y cuatro literales (A. B. C. y D.) por cada numeral.

Se incluyen ejemplos de cómo espero que respondas.

## Rol

Secretario muy minucioso.

## Tarea

Escribe el documento **completo** con un **formato específico** y para ello emplea las siguientes consideraciones secuenciales:

0. **Escribe literal y secuencialmente** cada **palabra** exacta del texto según el nuevo **formato específico**.

1. Identifica las estructuras de referencia a imágenes cuya sintaxis es `![texto opcional](ruta_a_la_imagen){texto_configuraciones}` y **déjalas intactas**.

2. Identifica los numerales cuya sintaxis es un número (uno o más dígitos) luego un símbolo (punto, paréntesis o guión) seguido de uno o más espacios vacíos para luego iniciar el texto de la pregunta y **cambia** para que sea al inicio de línea el número, un punto y un solo espacio vacío (ej. `1. `, `2. `... `10. `, etc).

3. Identifica guiones al piso que vienen con la sintaxis `\_` y **cambialos** por `_`.

4. Identifica los literales (opciones de respuesta) que suelen venir tras cada numeral como letras de la A a la D (ej. a, A, b, B, c, C, d y D) y un símbolo (punto, guión o paréntesis) y **cambia** para que quede el literal en mayúscula, seguido un punto y un solo espacio vacío para iniciar el texto de la opción (así: `A. `, `B. `, `C. ` y `D. `).

5. Identifica las estructuras de comentarios html cuya sintaxis es `<!-- -->` y **déjalas intactas**.

6. Identifica los resaltados que son bloques que se señalan así: `[texto de la opción]{.mark}` y **cambia** para que quede en negritas: **texto de la opción**.

7. Identifica textos que inician la línea por palabras o símbolos y **déjalos intactos**.

8. Identifica textos que pertenecen al contexto de la pregunta que suelen venir entre el numeral y las opciones en líneas diferentes a la del numeral y **déjalos intactos**.

9. Identifica textos que pertenecen al contexto de las opciones de respuesta que suelen venir en líneas diferentes a la línea inicial del literal hasta el siguiente numeral y **déjalos intactos**.

10. Verifica en cada línea la correcta sintaxis de los resaltados y las negritas para el texto.

11. Verifica que cada línea esté separada de la siguiente por los saltos de línea estándar en markdown `\n\n`.

12. Escribe el documento **completo** con un **formato específico** detallado en la sección **Formato**.

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