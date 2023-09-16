import pygetwindow as gw
import sys
import pyperclip
import time
import pyautogui
import unicodedata
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from bs4 import BeautifulSoup

def execute_alt_tab():
    # Simula presionar la tecla 'Alt+Tab'
    pyautogui.hotkey('alt', 'tab')
    time.sleep(0.5)  # Espera 0.5 segundos para asegurarnos de que se haya realizado el cambio de ventana

def main():
    # Ejecutar Alt+Tab una vez
    execute_alt_tab()

    # Abrir el archivo en modo de escritura
    with open('conteoresult.txt', 'a') as output_file:
        # Leer las URLs desde el archivo urls.txt
        with open('urlconteo.txt', 'r') as file:
            urls = file.readlines()

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
            time.sleep(4)

            pyautogui.hotkey('ctrl', 'u')
            time.sleep(3)

            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.3)
            
            pyautogui.hotkey('ctrl', 'c')
            time.sleep(0.3)
            
            pyautogui.hotkey('ctrl', 'w')
            time.sleep(0.3)
            
            # Obtén el contenido del portapapeles
            html = pyperclip.paste()

            # Crear un objeto BeautifulSoup para analizar el HTML
            soup = BeautifulSoup(html, 'html.parser')

            # Buscar los elementos <a> y <span> dentro de los <li> específicos
            breadcrumb_items = soup.find_all('li', class_='breadcrumb-dropdown-subitem-element-list')
            
            for item in breadcrumb_items:
                a_element = item.find('a')
                span_element = item.find('span')

                if a_element and span_element:
                    href = a_element['href']
                    span_text = span_element.get_text(strip=True)
                    span_text = span_text.replace('.', '')
                    
                    try:
                        span_value = int(span_text)
                        divided_value = (span_value / 32) + 1
                        integer_result = int(divided_value)
                        
                        output_file.write(f"Href: {href}\n")
                        output_file.write(f"Divided Value: {integer_result}\n")
                                                
                        base_url = "idealista.pt"
                        url_list = []
                        for i in range(1, integer_result + 1):
                            page_url = f"{base_url}{href}pagina-{i}"
                            url_list.append(page_url)
                        
                        for page_url in url_list:
                            output_file.write(page_url + "\n")
                        output_file.write("----------------------\n")
                    except ValueError:
                        output_file.write(f"Error parsing span value: {span_text}\n")

if __name__ == "__main__":
    main()