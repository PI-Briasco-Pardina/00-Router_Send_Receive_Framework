import requests
from flask import jsonify

def login():
    try:
        while True:
            username = input("Ingrese su email o nombre de usuario: ")
            password = input("Ingrese su contraseña: ")
            data = {'username': username, 'password': password}
            # Enviar credenciales al servidor
            response = requests.post('http://127.0.0.1:5000/login', json=data) # Bloqueante => Epera por la respuesta del servidor

            # Verificar si la autenticación fue exiosa (status code 200)
            if response.status_code == 200:
                access_token = response.json().get('access_token')
                return access_token
            # Verificar si las credenciales ingresadas eran válidas (status code 401)
            elif response.status_code == 401:
                print("Invalid username or password. Please try again.")
            # Manejar otros posibles HTTP status codes
            else:
                print(f"Falla al autenticarse. Status code: {response.status_code}")
    except Exception as e:
        print("Ha ocurrido un error:", type(e).__name__, "-", e)
        return None

def send_command(access_token):
    # URL del servidor donde se enviará la solicitud POST
    url = 'http://127.0.0.1:5000/execute_command'
    #url = 'https://108f-190-30-79-98.ngrok-free.app/execute_command'
    
    while True:
        command = input("Ingrese un comando ('exit' para salir): ")
        if command.lower() == 'exit':  # Verificar si el usuario quiere salir
            break
        
        headers = {'Authorization': f'Bearer {access_token}'}
        # Datos a enviar en la solicitud POST (comando)
        data = {'command': command} # En el campo command del json, incluir el comando
        try:
            # Enviar la solicitud POST al servidor incluyendo el comando en 'json' y las credenciales de autenticación en 'headers'
            response = requests.post(url, headers=headers, json=data) # Bloqueante => Epera por la respuesta del servidor
            # Si el http request fue exitoso, imprimir el contenido JSON de la respuesta
            if response.status_code == 200:
                result = response.json()
                print("Resultado:")
                print("Comando ejecutado:", result['command'])
                print("STDOUT:", result['stdout'])
                print("STDERR:", result['stderr'])
                print("Código de retorno:", result['returncode'])
            else:
                print("No se pudo ejecutar el comando. Status code:", response.status_code)
        except Exception as e:
            print("Ha ocurrido un error:", type(e).__name__, "-", e)
            return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    
    access_token = login()
    if access_token:
        send_command(access_token)