# ESTE CODIGO SE UTILIZA PARA BARRER https://www.idealista.com/agencias-inmobiliarias/madrid-madrid/inmobiliarias-para-alquiler
# PUEDE SER UTILIZADO PARA BARRER EL OBJETO JS DEL FRONT Y OBETNER URLS DE INMOBILIARIAS POR CIUDAD
# NO SE CONECTA A GOOGLE, LOS RESULTADOS LOS VUELCA EN EL TXT urlscajoninmo.txt

import time
import pyautogui
import pyperclip
from bs4 import BeautifulSoup

def alta_tab():
    pyautogui.hotkey('alt', 'tab')
    time.sleep(1)  # Espera 1 segundo para que se complete el cambio de ventana

def realizar_secuencia():
    pyautogui.press('f12')
    time.sleep(1.5)
    pyautogui.click(x=1278, y=285, button='right')
    time.sleep(1)
    pyautogui.press('down', presses=2)
    time.sleep(0.5)
    pyautogui.press('enter')
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'c')

def realizar_secuencia2():
    pyautogui.press('f12')
    time.sleep(0.2)
    pyautogui.hotkey('ctrl', 'f')
    time.sleep(0.2)
    pyautogui.typewrite("siguiente")
    time.sleep(0.5)
    pyautogui.press('esc')
    time.sleep(0.5)
    pyautogui.press('enter')
    time.sleep(2.5)

def guardar_url_ideal(line):
    with open('urlideal.txt', 'a') as file:
        file.write(line + '\n')

def main():
    alta_tab()  # Ejecuta el Alt + Tab una vez

    while True:
        realizar_secuencia()  # Ejecuta la secuencia de acciones en bucle

        # Pegar el contenido del portapapeles utilizando pyperclip
        html_content = pyperclip.paste()

        # Parsear el contenido HTML con Beautiful Soup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Buscar todos los elementos <a> que tengan el atributo role="heading"
        heading_links = soup.find_all('a', {'role': 'heading'})

        # Guardar las URLs en el archivo urlideal.txt
        for link in heading_links:
            url = link.get('href')
            if url:
                guardar_url_ideal(url)

        realizar_secuencia2()

        time.sleep(1)  # Espera 1 segundo entre cada iteración del bucle

if __name__ == "__main__":
    main()
