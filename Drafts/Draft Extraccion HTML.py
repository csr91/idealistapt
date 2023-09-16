import time
import pyperclip
import pyautogui
import keyboard
from bs4 import BeautifulSoup

def get_page_source(url):
    # Espera 3 segundos antes de comenzar
    time.sleep(1.5)

    # Copia la URL al portapapeles
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
    time.sleep(2.5)

    # Emula el atajo de teclado Ctrl+U para abrir el código fuente de la página
    pyautogui.hotkey('ctrl', 'u')

    # Espera 1 segundo para que se abra el código fuente
    time.sleep(3)

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
    page_source = pyperclip.paste()

    # Parsea el código fuente con BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

    # Encuentra todos los elementos <article>
    articles = soup.find_all('article')

    # Abre el archivo "pagesource.txt" en modo append
    with open('pagesource.txt', 'a', encoding='utf-8') as file:
        for article in articles:
            file.write(str(article))
            file.write('\n\n')

    print(f"El contenido de los elementos <article> de {url} se ha agregado a 'pagesource.txt'")

def process_page_source():
    # Leer el archivo "pagesource.txt"
    with open('pagesource.txt', 'r', encoding='utf-8') as file:
        page_source = file.read()

    # Realizar el procesamiento adicional con la variable "page_source"
    # ...

    # Imprimir el resultado
    print("Procesamiento adicional completado.")

def stop_program():
    print("Programa detenido")
    exit()

if __name__ == '__main__':
    with open('urls.txt', 'r') as file:
        urls = file.read().splitlines()

    print("Presiona 'esc' en cualquier momento para detener el programa.")
    print("El programa iniciará en 2 segundos.")
    time.sleep(1.5)

    # Activa la ventana del navegador utilizando Alt+Tab
    pyautogui.keyDown('alt')
    pyautogui.press('tab')
    pyautogui.keyUp('alt')

    keyboard.on_press_key('esc', stop_program)

    for url in urls:
        get_page_source(url)
        print("----------------------------------")

        # Llamar a la función para procesar el contenido del archivo "pagesource.txt"
        process_page_source()
        print("----------------------------------")
