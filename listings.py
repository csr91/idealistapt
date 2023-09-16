# ESTE CODIGO RECORRE LISTINGS POR PAGINAS NUMERADAS
# PEGA LA INFO EN LA HOJA datos DEL SHEET
# UTILIZA EL TXT listing.txt POR CADA URL A SCRAPEAR
# UTILIZA EL TXT ids_inmuebles.txt PARA VALIDAD DUPLICIDAD DE INMUEBLES
# UTILIZA EL TXT inmopagesource.txt PARA ALMACENAR INFORMACION DE LOS LISTINGS

import sys
import time
import pyperclip
import pyautogui
import keyboard
from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings("ignore")
import csv
import re
import gspread
from google.oauth2.service_account import Credentials
import datetime
import pygetwindow as gw

## PARTE 1 | OBTENCION DE HTML Y GUARDADO EN VARIABLE PAGESOURCE

html = ""
page_source = ""

fecha_actual = datetime.datetime.now().strftime('%Y%m%d')
PAIS = "Portugal"

def get_page_source(url):
    time.sleep(0.5)

    pyperclip.copy(url)

    # Emula el atajo de teclado Ctrl+L para seleccionar la barra de direcciones 
    pyautogui.hotkey('ctrl', 'l')

    # Espera 0.2 segundos para que se seleccione la barra de direcciones
    time.sleep(0.2)

    # Emula el atajo de teclado Ctrl+V para pegar la dirección de la página
    pyautogui.hotkey('ctrl', 'v')

    # Espera 0.2 segundos para que se pegue la dirección
    time.sleep(0.2)

    # Emula la tecla Enter para abrir la página
    pyautogui.press('enter')

    # Espera 1 segundo para que se cargue la página
    time.sleep(6.5)

    # Emula el atajo de teclado Ctrl+U para abrir el código fuente de la página
    pyautogui.hotkey('ctrl', 'u')

    # Espera 1 segundo para que se abra el código fuente
    time.sleep(4)

    # Emula el atajo de teclado Ctrl+A para seleccionar todo el contenido
    pyautogui.hotkey('ctrl', 'a')

    # Espera 1 segundo para que se realice la selección
    time.sleep(1.5)

    # Emula el atajo de teclado Ctrl+C para copiar el contenido al portapapeles
    pyautogui.hotkey('ctrl', 'c')

    # Espera 1 segundo para que se copie al portapapeles
    time.sleep(1)

    pyautogui.hotkey('ctrl', 'w')
    time.sleep(0.5)

    # Obtiene el contenido del portapapeles
    global html
    global page_source
    html = pyperclip.paste()
    page_source = html

    # Parsea el código fuente con BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

    # Encuentra todos los elementos <article>
    articles = soup.find_all('article')

    # Abre el archivo "pagesource.txt" en modo append
    with open('inmopagesource.txt', 'a', encoding='utf-8') as file:
        for article in articles:
            file.write(str(article))
            file.write('\n\n')

    print(f"El contenido de los elementos <article> de {url} se ha agregado a 'pagesource.txt'")

def process_page_source():
    # Leer el archivo "pagesource.txt"
    with open('pagesource.txt', 'r', encoding='utf-8') as file:
        page_source = file.read()

    # Imprimir el resultado
    print("Procesamiento adicional completado.")

def stop_program():
    print("Programa detenido")
    exit()

if __name__ == '__main__':
    with open('listing.txt', 'r') as file:
        urls = file.read().splitlines()

    print("Presiona 'esc' en cualquier momento para detener el programa.")
    print("El programa iniciará en 2 segundos.")
    time.sleep(1.5)

    # Esperar 2 segundos
    time.sleep(2)

    # Obtener la ventana de Google Chrome por título
    chrome_windows = gw.getWindowsWithTitle("Google Chrome")

    if not chrome_windows:
        print("No se encontraron ventanas de Google Chrome abiertas.")
        sys.exit()
    
    # Si hay ventanas de Chrome abiertas, activa la primera
    chrome_window = chrome_windows[0]
    chrome_window.activate()

    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 't')
    time.sleep(0.5)

    for url in urls:
        get_page_source(url)
        print("----------------------------------")

        # Llamar a la función para procesar el contenido del archivo "pagesource.txt"
        process_page_source()
        print("----------------------------------")

        ## PARTE 2 | PROCESAMIENTO DE INFORMACION DEL HTML ALOJADO EN PAGESOURCE

        # Obtener el contenido HTML desde la variable
        html = page_source

        # Crear el objeto BeautifulSoup con el HTML
        soup = BeautifulSoup(html, 'html.parser')

        # Obtener todos los elementos <article>
        articles = soup.find_all('article')

        # Guardar los datos en una lista de filas
        rows = []

        # Procesar cada artículo
        for article in articles:
            # Encontrar el elemento <a> que contiene la URL y el título del inmueble
            a_element = article.find('a', class_='item-link')

            # Verificar si el elemento existe antes de acceder a su atributo 'href'
            if a_element is not None:
                # Extraer la URL del inmueble
                url = a_element['href']

                # Extraer el ID del inmueble de la URL
                id_inmueble = re.search(r'/imovel/(\d+)/', url)
                id_inmueble = id_inmueble.group(1) if id_inmueble is not None else ""
            else:
                # Si el elemento no existe, asignar una cadena vacía a la URL e ID del inmueble
                url = ""
                id_inmueble = None

            # Extraer el título del inmueble
            titulo = a_element.text.strip() if a_element is not None else ""

            # Contar las comas en el título y extraer el texto correspondiente
            num_comas = titulo.count(',')
            if num_comas > 2:
                # If there are more than two commas, extract the second-to-last part
                titulo_extraido = titulo.split(',')[-2].strip()
            elif num_comas == 2:
                # If there are exactly two commas, extract the middle part
                titulo_extraido = titulo.split(',')[1].strip()
            elif num_comas == 1 and 'e ' in titulo:
                # If there is a single comma and 'e ' (with a space) before it, extract the part after 'e ' and before the comma
                titulo_extraido = titulo.split('e ')[1].split(',')[0].strip()
            elif num_comas == 1:
                # If there is a single comma without 'e ', extract the part before the comma
                titulo_extraido = titulo.split(',')[0].strip()
            else:
                # If there are no commas, keep the original titulo value
                titulo_extraido = titulo

            a2_element = article.find('a', attrs={'data-markup': 'listado::logo-agencia'})
            titulo_agencia = a2_element.get('title', "") if a2_element is not None else ""
            titulo_agencia = titulo_agencia.replace('|', '')  # Eliminar pipes

            # Obtener el dato del atributo href
            enlace_agencia = a2_element.get('href', "") if a2_element is not None else ""

            # Encontrar el elemento <span> que contiene el precio
            precio_element = article.find('span', class_='item-price')
            precio = re.sub(r'\D', '', precio_element.text.strip()) if precio_element is not None else ""

            # Encontrar los elementos <span> que contienen los detalles del inmueble
            detalles_element = article.find_all('span', class_='item-detail')
            habitaciones = re.sub(r'\D', '', detalles_element[0].text.strip()) if len(detalles_element) > 0 else "0"
            metros_cuadrados = re.sub(r'\D', '', detalles_element[1].text.strip()) if len(detalles_element) > 1 else ""

            # Encontrar el elemento <div> que contiene la descripción
            descripcion_element = article.find('div', class_='item-description')
            descripcion = descripcion_element.text.strip() if descripcion_element is not None else ""
            descripcion = re.sub(r'\n+', ' ', descripcion)  # Eliminar saltos de línea
            descripcion = descripcion.replace('|', '')  # Eliminar pipes

            # Encontrar el segundo elemento <li> con la clase "breadcrumb-navigation-element"
            li_element = soup.find_all('li', class_='breadcrumb-navigation-element')[1]

            # Encontrar el elemento <span> dentro del <a> del segundo elemento <li>
            span_element = li_element.find('span', itemprop='name')

            # Extraer el contenido del elemento <span>
            CIUDAD = span_element.get_text(strip=True)


            # Verificar si hay información de ID de inmueble antes de agregar la fila
            if id_inmueble is not None:
                rows.append([fecha_actual, PAIS, CIUDAD, id_inmueble, url, titulo, titulo_extraido, enlace_agencia, titulo_agencia, precio, habitaciones, metros_cuadrados])

        ## PARTE 3 | GUARDADO EN CSV LOCAL Y GOOGLE SHEET

        # Leer los IDs de los inmuebles existentes en el archivo de texto
        existing_ids = set()
        with open('ids_inmuebles.txt', 'r', encoding='utf-8') as file:
            for line in file:
                existing_ids.add(line.strip())

        # Filtrar los nuevos datos para evitar duplicados
        new_rows = [row for row in rows if row[3] not in existing_ids]

        # Guardar los nuevos IDs en el archivo de texto
        with open('ids_inmuebles.txt', 'a', encoding='utf-8') as file:
            for row in new_rows:
                id_inmueble = row[3]  # Cambiar 2 a la posición correcta del ID en la lista row
                file.write(str(id_inmueble))
                file.write('\n')

        num_datos_guardados = len(new_rows)
        print(f"Se han guardado en total {num_datos_guardados} nuevos datos en 'ids_inmuebles.txt'")

        # Autenticación de Google
        credenciales_json = 'auth.json'  # Ruta al archivo JSON de las credenciales
        alcance = ['https://www.googleapis.com/auth/spreadsheets']  # Alcance de acceso a la hoja de cálculo
        credenciales = Credentials.from_service_account_file(credenciales_json)
        credenciales = credenciales.with_scopes(alcance)
        cliente = gspread.authorize(credenciales)

        # Abre la hoja de cálculo por su URL
        hoja_calculo = cliente.open_by_url('https://docs.google.com/spreadsheets/d/1hVN_O1jFfP3YhRilSNmeMZqQbfw4FXi1p0pOSvCIunk/edit#gid=1100087305')

        # Selecciona la hoja de cálculo por su nombre (pestaña)
        nombre_pestaña = 'Portugal'
        hoja = hoja_calculo.worksheet(nombre_pestaña)

        # Obtener la última fila no vacía en la primera columna
        columna_primera = hoja.col_values(1)
        last_non_empty_row = len(columna_primera)

        # Obtener la referencia de la celda para la actualización (la siguiente fila)
        next_row = last_non_empty_row + 1
        cell_range = f'A{next_row}'

        # Actualizar la hoja de cálculo con los nuevos datos en la siguiente fila a la última fila no vacía en la PRIMERA columna
        hoja.update(cell_range, new_rows, value_input_option='USER_ENTERED')

        print("Los nuevos datos se han enviado a la hoja de cálculo en Google.")