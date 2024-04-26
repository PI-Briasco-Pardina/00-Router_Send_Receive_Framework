from flask import Flask, request, jsonify # pip install Flask

import subprocess   #El módulo subprocess, que permite ejecutar comandos del sistema operativo desde Python

app = Flask(__name__) # Creación de una instancia de la clase Flask

# Definición de un endpoint '/execute_command' que recibe solicitudes POST
@app.route('/execute_command', methods=['POST'])
def execute_command():
    try:
        # Obtención de los datos enviados en la solicitud POST en formato JSON
        data = request.get_json()
        # Extracción del comando enviado en los datos recibidos
        command = data['command']
        # Impresión del comando recibido en la consola del servidor
        print("Comando:", command)
        # Ejecución del comando utilizando la función run_command y almacenamiento del resultado
        result = run_command(command)
        # Conversión del resultado a formato JSON y devolución como respuesta al cliente
        return jsonify(result)
    except Exception as e:
        print("Ha ocurrido un error:", type(e).__name__, "-", e)
        return jsonify({'error': str(e)}), 500
# Función para ejecutar comandos y devolver el resultado en formato JSON
def run_command(command):
    try:
        # Ejecución del comando utilizando subprocess.run()
        result = subprocess.run(command.split(), capture_output=True, text=True)
        # Construcción de un diccionario con el resultado del comando y sus propiedades
        return {
            'command': command,          # Comando ejecutado
            'stdout': result.stdout,     # Salida estándar del comando
            'stderr': result.stderr,     # Salida de error estándar del comando
            'returncode': result.returncode  # Código de retorno del comando
        }
    except Exception as e:
        print("Ha ocurrido un error:", type(e).__name__, "-", e)
        return jsonify({'error': str(e)}), 500

# Condición para ejecutar el servidor si este script es el punto de entrada principal
if __name__ == '__main__':
    # Iniciar el servidor Flask en la dirección IP 0.0.0.0 (accesible desde cualquier dirección IP) y en el puerto 5000
    app.run(host='0.0.0.0', port=5000)
