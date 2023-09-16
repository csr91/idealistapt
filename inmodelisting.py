# ESTE CODIGO OBTIENE DE UN LISTING EL TITULO Y LA URL DE LA INMOBILIARIA
# PEGA CADA URL Y TITULO EN LA HOJA inmodelisting DEL SHEET
# UTILIZA EL TXT inmodelisting.txt

import pyperclip
import time
import pyautogui
import unicodedata
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from bs4 import BeautifulSoup

def remove_unwanted_characters(text):
    return text.replace('\n', ' ').replace('|', ' ')

def authenticate_google_sheets():
    # Cargamos las credenciales desde el archivo auth.json
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('auth.json', scope)
    client = gspread.authorize(creds)

    # Abrimos la hoja de cálculo por su URL
    spreadsheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1hVN_O1jFfP3YhRilSNmeMZqQbfw4FXi1p0pOSvCIunk/edit#gid=306915816')
    return spreadsheet.worksheet('inmodelistingPT')

def execute_alt_tab():
    # Simula presionar la tecla 'Alt+Tab'
    pyautogui.hotkey('alt', 'tab')
    time.sleep(0.5)  # Espera 0.5 segundos para asegurarnos de que se haya realizado el cambio de ventana

def main():
    # Autenticar con Google Sheets
    worksheet_data = authenticate_google_sheets()
    worksheet_nourl = worksheet_data.spreadsheet.worksheet('nourl')
    # Ejecutar Alt+Tab una vez
    execute_alt_tab()
    # Leer las URLs desde el archivo urls.txt
    with open('inmodelisting.txt', 'r') as file:
        urls = file.readlines()
    # Eliminar líneas en blanco y espacios en blanco
    urls = [url.strip() for url in urls if url.strip()]

    # Bucle para copiar y pegar URLs
    for url_original in urls:
        # Simula copiar la URL
        pyautogui.hotkey('ctrl', 'l')
        time.sleep(0.2)

        # Simula pegar la URL
        pyautogui.write(url_original.strip())
        time.sleep(0.2)

        # Simula presionar Enter
        pyautogui.press('enter')
        time.sleep(7.5)

        pyautogui.hotkey('ctrl', 'u')
        time.sleep(4.5)

        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.5)
        
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(0.5)
        
        pyautogui.hotkey('ctrl', 'w')
        time.sleep(0.5)
        
        # Obtén el contenido del portapapeles
        html_doc = pyperclip.paste()

        # Crear un objeto BeautifulSoup para analizar el HTML
        soup = BeautifulSoup(html_doc, 'html.parser')

        # Verificar si el bloque <div class="infoblock"> está presente en el HTML
        infoblock_div = soup.find('div', class_='deactivated-detail_container')

        # Verificar si el bloque <span class="particular"> está presente en el HTML
        particular_spans = soup.find_all('span', class_='particular')

        if infoblock_div:
            # Si se encuentra el bloque, guardar la URL en la hoja "nourl"
            worksheet_nourl.append_row([url_original.strip()])
            print(f"URL de error guardada en la hoja 'nourl': {url_original.strip()}")
        else:
            # Si se encuentra el bloque <span class="particular">, obtener el nombre del anunciante
            for particular_span in particular_spans:
                nombre_anunciante = particular_span.find('p', class_='about-advertiser-name')
                if nombre_anunciante and nombre_anunciante.string:
                    nombre_particular = nombre_anunciante.string.strip()
                    print("--------")
                    print(f"URL original: {url_original.strip()}")
                    print("URL bloque: BLANCO")
                    print("Nombre del anunciante:", nombre_particular)
                    print()
                    # Guardar los resultados en Google Sheets
                    worksheet_data.append_row([url_original.strip(), 'PARTICULAR', nombre_particular])
                    break
            else:
                # Si no se encuentra ninguno de los objetos del HTML que interesan, buscamos el nombre de la inmobiliaria
                a_tag = soup.find('a', class_='about-advertiser-name')
                if a_tag and a_tag.string:
                    nombre_inmobiliaria = a_tag.string.strip()
                    print("--------")
                    print(f"URL original: {url_original.strip()}")
                    print(f"URL bloque: {a_tag['href']}")
                    print("Nombre de la inmobiliaria:", nombre_inmobiliaria)
                    print()
                    # Guardar los resultados en Google Sheets
                    worksheet_data.append_row([url_original.strip(), a_tag['href'], nombre_inmobiliaria])
                else:
                    print(f"No se encontraron datos interesantes para la URL: {url_original.strip()}")
                    print("Continuando con la siguiente URL...")
                    print()
                    continue

if __name__ == "__main__":
    main()