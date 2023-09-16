1. Función `get_page_source(url)`:
   - Espera un tiempo y copia la URL al portapapeles.
   - Emula el atajo de teclado para abrir la página utilizando la URL del portapapeles.
   - Espera a que se cargue la página y abre el código fuente.
   - Copia el contenido del código fuente al portapapeles y lo guarda en una variable.
   - Escribe el contenido del código fuente en el archivo `pagesource.txt`.
   - Imprime un mensaje indicando que el contenido de los elementos `<article>` de la URL se ha agregado al archivo.

2. Función `process_page_source()`:
   - Lee el archivo `pagesource.txt`.
   - Realiza algún procesamiento adicional con el contenido del archivo.
   - Imprime un mensaje indicando que el procesamiento adicional se ha completado.

3. Función `stop_program()`:
   - Imprime un mensaje indicando que el programa se ha detenido.
   - Finaliza el programa.

4. Inicio del programa principal:
   - Lee las URLs desde el archivo `urls.txt`.
   - Imprime un mensaje de inicio y espera un tiempo.
   - Activa la ventana del navegador.
   - Establece la tecla de escape (`esc`) para detener el programa.
   - Para cada URL:
     - Invoca `get_page_source(url)` para obtener el código fuente de la página.
     - Invoca `process_page_source()` para procesar el contenido del código fuente.
     - Obtiene los datos de los elementos `<article>` y los almacena en la lista `rows`.
     - Filtra los nuevos datos para evitar duplicados.
     - Guarda los nuevos IDs en el archivo `ids_inmuebles.txt`.
     - Imprime el número total de nuevos datos guardados.
     - Autentica con Google utilizando un archivo JSON de credenciales.
     - Abre la hoja de cálculo de Google por su URL.
     - Selecciona la hoja de cálculo y obtiene la última fila no vacía.
     - Actualiza la hoja de cálculo con los nuevos datos a partir de la última fila.
     - Imprime un mensaje de confirmación de que los nuevos datos se han enviado a la hoja de cálculo en Google.


DETALLES:

main.py

1. Importación de módulos y configuración inicial.

2. Definición de la función `get_page_source(url)`:
   - Espera 0.5 segundos.
   - Copia la URL al portapapeles.
   - Emula el atajo de teclado para seleccionar la barra de direcciones.
   - Espera 0.2 segundos para que se seleccione la barra de direcciones.
   - Emula el atajo de teclado para pegar la dirección de la página.
   - Espera 0.2 segundos para que se pegue la dirección.
   - Emula la tecla Enter para abrir la página.
   - Espera 1.5 segundos para que se cargue la página.
   - Emula el atajo de teclado para abrir el código fuente de la página.
   - Espera 3 segundos para que se abra el código fuente.
   - Emula el atajo de teclado para seleccionar todo el contenido.
   - Espera 1 segundo para que se realice la selección.
   - Emula el atajo de teclado para copiar el contenido al portapapeles.
   - Espera 1 segundo para que se copie al portapapeles.
   - Cierra la pestaña actual en el navegador.
   - Obtiene el contenido del portapapeles y lo guarda en las variables `html` y `page_source`.
   - Parsea el código fuente con BeautifulSoup.
   - Encuentra todos los elementos `<article>`.
   - Escribe el contenido de cada elemento `<article>` en el archivo `pagesource.txt`.
   - Imprime un mensaje indicando que el contenido de los elementos `<article>` de la URL se ha agregado a `pagesource.txt`.

3. Definición de la función `process_page_source()`:
   - Lee el contenido del archivo `pagesource.txt`.
   - Realiza algún procesamiento adicional con el contenido de la variable `page_source`.
   - Imprime un mensaje indicando que el procesamiento adicional se ha completado.

4. Definición de la función `stop_program()`:
   - Imprime un mensaje indicando que el programa se ha detenido.
   - Finaliza el programa.

5. Inicio del programa principal:
   - Lee las URLs desde el archivo `urls.txt`.
   - Imprime un mensaje indicando que el programa iniciará en 2 segundos.
   - Espera 1.5 segundos.
   - Activa la ventana del navegador utilizando Alt+Tab.
   - Establece la tecla de escape (`esc`) para detener el programa.
   - Para cada URL en la lista de URLs:
     - Invoca la función `get_page_source(url)` para obtener el código fuente de la página.
     - Imprime un separador.
     - Invoca la función `process_page_source()` para procesar el contenido del código fuente.
     - Imprime un separador.
     - Obtiene el contenido HTML desde la variable `page_source`.
     - Crea un objeto BeautifulSoup con el HTML.
     - Encuentra todos los elementos `<article>`.
     - Crea una lista vacía llamada `rows` para almacenar los datos de los elementos `<article>`.
     - Para cada elemento `<article>`:
       - Encuentra el elemento `<a>` que contiene la URL y el título del inmueble.
       - Si el elemento `<a>` existe, extrae la URL y el ID del inmueble de la URL.
       - Extrae el título del inmueble.
       - Realiza alguna manipulación adicional en el título.
       - Encuentra el elemento `<a>` que contiene el título de la agencia.
       - Si el elemento `<a>` existe, extrae el título de la agencia.
       - Encuentra el elemento `<span>` que contiene el precio.
       - Si el elemento `<span>` existe, extrae el precio.
       - Encuentra los elementos `<span>` que contienen los detalles del inmueble.
       - Si existen los elementos `<span>`, extrae los detalles del inmueble.
       - Encuentra el elemento `<div>` que contiene la descripción.
       - Si el elemento `<div>` existe, extrae la descripción.
       - Realiza alguna manipulación adicional en la descripción.
       - Verifica si hay información de ID de inmueble antes de agregar una fila a la lista `rows`.
     - Filtra los nuevos datos para evitar duplicados.
     - Guarda los nuevos IDs en el archivo `ids_inmuebles.txt`.
     - Imprime la cantidad total de nuevos datos guardados en `ids_inmuebles.txt`.
     - Realiza la autenticación de Google utilizando un archivo JSON de credenciales.
     - Abre la hoja de cálculo de Google mediante su URL.
     - Selecciona la hoja de cálculo y obtiene la última fila no vacía.
     - Actualiza la hoja de cálculo con los nuevos datos a partir de la última fila.
     - Imprime un mensaje indicando que los nuevos datos se han enviado a la hoja de cálculo de Google.