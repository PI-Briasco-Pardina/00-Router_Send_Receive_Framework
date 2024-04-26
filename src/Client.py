import requests
from flask import jsonify 

def send_command(command):
    # URL del servidor donde se enviará la solicitud POST
    url = 'http://127.0.0.1:5000/execute_command'
    #url = 'https://108f-190-30-79-98.ngrok-free.app/execute_command'
    # Datos a enviar en la solicitud POST (comando)
    data = {'command': command}
    try:
        # Enviar la solicitud POST al servidor
        response = requests.post(url, json=data) # Bloqueante => Epera por la respuesta del servidor
        # Devolver el contenido JSON de la respuesta
        return response.json()
    except Exception as e:
        print("Ha ocurrido un error:", type(e).__name__, "-", e)
        return jsonify({'error': str(e)}), 500
    
while True:
    command = input("Ingrese un comando ('exit' para salir): ")
    if command.lower() == 'exit':  # Verificar si el usuario quiere salir
        break
    result = send_command(command)
    print("Resultado:")
    print("Comando ejecutado:", result['command'])
    print("STDOUT:", result['stdout'])
    print("STDERR:", result['stderr'])
    print("Código de retorno:", result['returncode'])
