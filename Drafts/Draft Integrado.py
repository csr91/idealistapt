import warnings
warnings.filterwarnings("ignore")
import csv
from bs4 import BeautifulSoup
import re
import gspread
from google.oauth2.service_account import Credentials

# Leer el archivo de texto con el HTML
with open('pagesource.txt', 'r', encoding='utf-8') as file:
    html = file.read()

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
        id_inmueble = re.search(r'/inmueble/(\d+)/', url)
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
        titulo_extraido = titulo.split(',')[-2].strip()
    elif num_comas == 2:
        titulo_extraido = titulo.split(',')[1].strip()
    elif num_comas == 1:
        titulo_extraido = titulo.split('en ')[1].split(',')[0].strip()
    else:
        titulo_extraido = titulo

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

    # Verificar si hay información de ID de inmueble antes de agregar la fila
    if id_inmueble is not None:
        rows.append([id_inmueble, url, titulo, titulo_extraido, precio, habitaciones, metros_cuadrados, f'"{descripcion}"'])

# Guardar los datos en un archivo CSV
with open('datos.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['ID Inmueble', 'URL del inmueble', 'Título original', 'Título del inmueble', 'Precio', 'Habitaciones', 'Metros cuadrados', 'Descripción'])
    writer.writerows(rows)

print("Los datos se han guardado en 'datos.csv'")

# Autenticación de Google
credenciales_json = 'auth.json'  # Ruta al archivo JSON de las credenciales
alcance = ['https://www.googleapis.com/auth/spreadsheets']  # Alcance de acceso a la hoja de cálculo
credenciales = Credentials.from_service_account_file(credenciales_json)
credenciales = credenciales.with_scopes(alcance)
cliente = gspread.authorize(credenciales)

# Abre la hoja de cálculo por su URL
hoja_calculo = cliente.open_by_url('https://docs.google.com/spreadsheets/d/1hVN_O1jFfP3YhRilSNmeMZqQbfw4FXi1p0pOSvCIunk/edit#gid=1100087305')

# Selecciona la hoja de cálculo por su índice o por su nombre
hoja = hoja_calculo.get_worksheet(0)

# Obtiene los datos del archivo CSV
with open('datos.csv', 'r', encoding='utf-8-sig') as csvfile:
    reader = csv.reader(csvfile)
    datos_csv = list(reader)

# Envía los datos a la hoja de cálculo
hoja.update('A1', datos_csv)

print("Los datos se han enviado a la hoja de cálculo en Google.")
