from flask import Flask, request, jsonify # pip install Flask
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity # Framework de seguridad
import subprocess                         # El módulo subprocess, que permite ejecutar comandos del sistema operativo desde Python
import secrets                            # Generar JWT_SECRET_KEY aleatoria para mantener la confidencialidad
from flask_sqlalchemy import SQLAlchemy   # Base de datos para registrar clientes
from passlib.hash import pbkdf2_sha256    # Para password hashing

# Generar una clave secreta aleatoria segura
secret_key = secrets.token_hex(32)

# Creación de una instancia de la clase Flask
app = Flask(__name__) 
app.config['JWT_SECRET_KEY'] = secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # SQLite database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar Flask-JWT-Extended
jwt = JWTManager(app)

# Inicializar base de datos
db = SQLAlchemy(app)

# Definir modelo para la base de datos
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# Crear usuarios de prueba (esto va a ser reemplazado por una base de datos)
users = {
    'user1': 'password1',
    'user2': 'password2'
}

# Definir un endpoint para login
@app.route('/login', methods=['POST'])
def login():
    try:    
        username = request.json.get('username')
        password = request.json.get('password')

        # Buscar coincidencias con el usuario en la base de datos
        user = User.query.filter_by(username=username).first()

        # Existen coincidencias => user <User object> ; No existen coincidencias => user = None
        if user and pbkdf2_sha256.verify(password, user.password):  # pbkdf2_sha256.verify realiza la comparación con la contraseña encriptada
            # Crear un JWT token
            access_token = create_access_token(identity=username)
            return jsonify(access_token=access_token), 200
        else:
            return jsonify({'message': 'Usuario o contraseña incorrectos'}), 401
    except Exception as e:
        print("Ha ocurrido un error:", type(e).__name__, "-", e)
        return jsonify({'error': str(e)}), 500

# Definir que recibe solicitudes POST (espera comandos de red en formato json para ejecutar)
@app.route('/execute_command', methods=['POST'])
@jwt_required()  # Requiere autenticación
def execute_command():
    try:
        # Acceder de los datos del HTTP request (enviados en la solicitud POST) en formato JSON
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
    with app.app_context():
        # Crear las tablas de la base de datos (si aún no existen)
        db.create_all()

        # -------------------- Reemplazar por endpoint para registro de usuarios ----------------------
        # Función para agregar usuarios
        def add_user(username, password):
            # Check if the username already exists
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                print("User with username '{}' already exists.".format(username))
                return
            else:
                hashed_password = pbkdf2_sha256.hash(password)
                new_user = User(username=username, password=hashed_password)
                db.session.add(new_user)
                db.session.commit()

        # Agregar usuarios de prueba
        add_user('user1', 'password1')
        # ---------------------------------------------------------------------------------------------
    
    # Iniciar el servidor Flask en la dirección IP 0.0.0.0 (accesible desde cualquier dirección IP) y en el puerto 5000
    app.run(host='0.0.0.0', port=5000)
