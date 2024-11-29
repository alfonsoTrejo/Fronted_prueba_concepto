from flask import Flask, jsonify, request
from supabase import create_client, Client
from dotenv import load_dotenv
import os
from flask_cors import CORS  # Importa CORS de forma correcta

# Cargar variables de entorno
load_dotenv()

# Configuración de Supabase
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

# Inicializar cliente de Supabase
supabase: Client = create_client(supabase_url, supabase_key)

# Nombre de la tabla
TABLE_NAME = "eventos"

# Inicializar la aplicación Flask
app = Flask(__name__)
CORS(app)  # Configuración de CORS para permitir todas las solicitudes

@app.route("/")
def home():
    return "Bienvenido a la API de Flask para Supabase."

@app.route("/CrearEvento", methods=["POST"])
def crear_evento():
    """
    Crear un nuevo registro en la tabla 'eventos'.
    """
    try:
        # Obtener los datos enviados en la solicitud POST
        data = request.json  # Usamos request.json para obtener el cuerpo de la solicitud
        
        # Validar los campos requeridos
        nombre = data.get("nombre")
        canal = data.get("canal")
        fecha = data.get("fecha")

        if not nombre or not canal or not fecha:
            return jsonify({"error": "Faltan datos obligatorios: 'nombre', 'canal', 'fecha'"}), 400

        # Insertar el registro en la tabla
        response = supabase.table(TABLE_NAME).insert({
            "nombre_evento": nombre,
            "canal_evento": canal,
            "fecha_evento": fecha
        }).execute()

        # Comprobar si la respuesta tiene algún error
        if not response:
            return jsonify({"error": response.error.message}), 400

        return jsonify({"message": "Evento creado exitosamente", "data": response.data}), 201
    except Exception as e:
        print(str(e))  
        return jsonify({"error": str(e)}), 500

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)