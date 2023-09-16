# ESTE CODIGO RECORRE LAS URL DE LAS INMOBILIARIAS Y PEGA TITULO DIRECCION Y CODIGO POSTAL EN LA HOJA inmodire
# NECESITA DE HOJA nourls PARA PEGAR LAS URLS QUE FALLAN
# UTILIZA EL TXT urlinmos.txt PARA BARRER LAS URLS

import pyperclip
import time
import pyautogui
import unicodedata
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from bs4 import BeautifulSoup

def extract_postal_code(text):
    # Buscar la última coma en el texto
    last_comma_index = text.rfind(',')

    if last_comma_index != -1:
        # Extraer el texto después de la última coma (excluyendo el espacio después de la coma)
        postal_code_text = text[last_comma_index + 2:]

        # Buscar el código postal dentro del texto extraído
        import re
        postal_code_match = re.search(r'\b\d{5}\b', postal_code_text)
        return postal_code_match.group() if postal_code_match else "N/A"
    else:
        return "N/A"

def remove_unwanted_characters(text):
    return text.replace('\n', ' ').replace('|', ' ')

def authenticate_google_sheets():
    # Cargamos las credenciales desde el archivo auth.json
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('auth.json', scope)
    
    try:
        client = gspread.authorize(creds)
        print("Autenticación con Google Sheets exitosa.")
    except Exception as e:
        print("Error al autenticar con Google Sheets:", e)
        return None

    # Abrimos la hoja de cálculo por su URL
    spreadsheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1hVN_O1jFfP3YhRilSNmeMZqQbfw4FXi1p0pOSvCIunk/edit#gid=306915816')
    return spreadsheet.worksheet('Inmobiliarias')

def execute_alt_tab():
    # Simula presionar la tecla 'Alt+Tab'
    pyautogui.hotkey('alt', 'tab')
    time.sleep(0.5)  # Espera 0.5 segundos para asegurarnos de que se haya realizado el cambio de ventana

def main():
    # Autenticar con Google Sheets
    worksheet_data = authenticate_google_sheets()
    worksheet_nourl = worksheet_data.spreadsheet.worksheet('nourlinmo')
    # Ejecutar Alt+Tab una vez
    execute_alt_tab()
    # Leer las URLs desde el archivo urls.txt
    with open('urlinmos.txt', 'r') as file:
        urls = file.readlines()
    # Eliminar líneas en blanco y espacios en blanco
    urls = [url.strip() for url in urls if url.strip()]

    # Bucle para copiar y pegar URLs
    for url in urls:
        # Simula copiar la URL
        pyautogui.hotkey('ctrl', 'l')
        time.sleep(0.2)

        # Simula pegar la URL
        pyautogui.write(url)
        time.sleep(0.2)

        # Simula presionar Enter
        pyautogui.press('enter')
        time.sleep(7)

        pyautogui.hotkey('ctrl', 'u')
        time.sleep(5)

        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.5)
        
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(0.5)
        
        pyautogui.hotkey('ctrl', 'w')
        time.sleep(0.5)
        
        # Obtén el contenido del portapapeles
        html = pyperclip.paste()

        # Crear un objeto BeautifulSoup para analizar el HTML
        soup = BeautifulSoup(html, 'html.parser')

        # Verificar si el bloque <div class="infoblock"> está presente en el HTML
        infoblock_div = soup.find('div', class_='infoblock')

        url_parts = url.split("/")
        subpath = url_parts[-2]

        print("Subpath:", subpath)  # Imprimir en terminal

        if infoblock_div:
            # Si se encuentra el bloque, guardar la URL en la hoja "nourl"
            worksheet_nourl.append_row([url])
            print(f"URL de error guardada en la hoja 'nourl': {url}")
        else:
            # Extraer la información del HTML
            location_info = soup.select_one('button.location')
            agency_info = soup.select_one('div.office-title h1')

            # Preparar datos para Google Sheets
            location_text = location_info.text.strip() if location_info else "N/A"
            agency_name = agency_info.text.strip() if agency_info else "N/A"

            # Eliminar caracteres no deseados de los datos
            location_text = remove_unwanted_characters(location_text)
            agency_name = remove_unwanted_characters(agency_name)

            # Convertir caracteres especiales a su forma normalizada
            location_text = unicodedata.normalize('NFKD', location_text)
            agency_name = unicodedata.normalize('NFKD', agency_name)

            # Extraer el código postal
            postal_code = extract_postal_code(location_text)

            specific_url = f"/pro/{subpath}/"

            # Imprimir los resultados en pantalla
            print("URL:", url)
            print("Specific url:", specific_url)
            print("Nombre de la agencia:", agency_name)
            print("Ubicación:", location_text)
            print("Código Postal:", postal_code)
            print()

            # Guardar los resultados en Google Sheets
            worksheet_data.append_row([specific_url, url, agency_name, location_text, postal_code])

if __name__ == "__main__":
    main()