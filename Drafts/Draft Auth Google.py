import gspread
from google.oauth2.service_account import Credentials

# Ruta al archivo JSON de las credenciales
credenciales_json = 'auth.json'  # Reemplaza con la ruta real de tu archivo JSON

# Alcance de acceso a la hoja de cálculo
alcance = ['https://www.googleapis.com/auth/spreadsheets']

# Crea el objeto de autenticación desde las credenciales JSON
credenciales = Credentials.from_service_account_file(credenciales_json)
credenciales = credenciales.with_scopes(alcance)

# Autentica el cliente
cliente = gspread.authorize(credenciales)

# Abre la hoja de cálculo por su URL
hoja_calculo = cliente.open_by_url('https://docs.google.com/spreadsheets/d/1hVN_O1jFfP3YhRilSNmeMZqQbfw4FXi1p0pOSvCIunk/edit#gid=1100087305')

# Selecciona la hoja de cálculo por su índice o por su nombre
hoja = hoja_calculo.get_worksheet(0)
