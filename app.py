import os
from flask import Flask, render_template, request, jsonify
from supabase import create_client, Client

app = Flask(__name__)

# Configuración de Supabase
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase: Client = None
if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# RUTAS DE PÁGINAS
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

# API JEFES
@app.route('/api/jefes', methods=['GET', 'POST'])
def handle_jefes():
    if not supabase: return jsonify([]), 500
    if request.method == 'POST':
        data = request.json
        supabase.table('jefes').insert(data).execute()
        return jsonify({"status": "ok"}), 201
    res = supabase.table('jefes').select('*').execute()
    return jsonify(res.data)

@app.route('/api/jefes/<id>', methods=['DELETE'])
def delete_jefe(id):
    if supabase:
        supabase.table('jefes').delete().eq('id', id).execute()
    return jsonify({"status": "deleted"})

# API NOVEDADES (ACTUALIZACIONES)
@app.route('/api/novedades', methods=['GET', 'POST'])
def handle_novedades():
    if not supabase: return jsonify([]), 500
    if request.method == 'POST':
        data = request.json
        supabase.table('novedades').insert(data).execute()
        return jsonify({"status": "ok"}), 201
    res = supabase.table('novedades').select('*').order('id', desc=True).execute()
    return jsonify(res.data)

@app.route('/api/novedades/<id>', methods=['DELETE'])
def delete_novedad(id):
    if supabase:
        supabase.table('novedades').delete().eq('id', id).execute()
    return jsonify({"status": "deleted"})

# API ARMAS
@app.route('/api/armas', methods=['GET', 'POST'])
def handle_armas():
    if not supabase: return jsonify([]), 500
    if request.method == 'POST':
        data = request.json
        supabase.table('armas').insert(data).execute()
        return jsonify({"status": "ok"}), 201
    res = supabase.table('armas').select('*').execute()
    return jsonify(res.data)

@app.route('/api/armas/<id>', methods=['DELETE'])
def delete_arma(id):
    if supabase:
        supabase.table('armas').delete().eq('id', id).execute()
    return jsonify({"status": "deleted"})

# API RECETAS
@app.route('/api/recetas', methods=['GET', 'POST'])
def handle_recetas():
    if not supabase: return jsonify([]), 500
    if request.method == 'POST':
        data = request.json
        supabase.table('recetas').insert(data).execute()
        return jsonify({"status": "ok"}), 201
    res = supabase.table('recetas').select('*').execute()
    return jsonify(res.data)

@app.route('/api/recetas/<id>', methods=['DELETE'])
def delete_receta(id):
    if supabase:
        supabase.table('recetas').delete().eq('id', id).execute()
    return jsonify({"status": "deleted"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
