import requests

# API key and secret
api_key = "md45n49h40x5fspy88k9ayg6krfbeimu"
api_secret = "rocjZ7kxM0qH"

# URL de la API para la búsqueda de alquileres de pisos en Madrid
url = 'https://api.idealista.com/3.5/es/search'

# Parámetros de la consulta
params = {
    'propertyType': 'homes',
    'operation': 'rent',
    'center': '40.4168,-3.7038',  # Coordenadas de Madrid
    'distance': '10000',          # Distancia máxima a la ubicación en metros
    'maxItems': '10',             # Número máximo de resultados a obtener
}

# Headers con la autenticación
headers = {
    'Authorization': 'Bearer ' + access_token
}

# Realizar la consulta a la API
response = requests.post(url, params=params, headers=headers)

# Comprobar si la solicitud fue exitosa (código de estado 200)
if response.status_code == 200:
    # Obtener el contenido JSON de la respuesta
    data = response.json()

    # Mostrar los detalles de cada propiedad encontrada
    for property_info in data.get('elementList', []):
        print(f"ID de propiedad: {property_info.get('propertyCode')}")
        print(f"Dirección: {property_info.get('address')}")
        print(f"Precio: {property_info.get('price')} euros")
        print(f"Número de habitaciones: {property_info.get('rooms')}")
        print(f"Número de baños: {property_info.get('bathrooms')}")
        print("------------------------------------")
else:
    print(f"Error en la consulta: {response.status_code}")
