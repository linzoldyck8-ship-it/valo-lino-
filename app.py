import os
from flask import Flask, render_template, request, jsonify
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/api/jefes', methods=['GET'])
def obtener_jefes():
    respuesta = supabase.table("jefes").select("*").order("creado_en", desc=True).execute()
    return jsonify(respuesta.data)

@app.route('/api/jefes', methods=['POST'])
def agregar_jefe():
    datos = request.json
    supabase.table("jefes").insert(datos).execute()
    return jsonify({"mensaje": "Jefe agregado"}), 201

@app.route('/api/jefes/<id>', methods=['DELETE'])
def eliminar_jefe(id):
    supabase.table("jefes").delete().eq("id", id).execute()
    return jsonify({"mensaje": "Jefe eliminado"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)