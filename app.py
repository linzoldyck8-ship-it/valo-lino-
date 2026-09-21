import os
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from functools import wraps
from supabase import create_client, Client

app = Flask(__name__)

# Clave secreta para la sesión y contraseña del administrador
app.secret_key = os.environ.get("SECRET_KEY", "clave_secreta_mc_wiki_2026")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "12345")  # <-- CAMBIA "12345" POR LA CONTRASEÑA QUE QUIERAS

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase: Client = None
if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Decorador para proteger rutas privadas
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            if request.path.startswith('/api/'):
                return jsonify({"error": "No autorizado"}), 401
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# AUTENTICACIÓN
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        pwd = request.form.get('password')
        if pwd == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('admin'))
        else:
            error = "Contraseña incorrecta. Inténtalo de nuevo."
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('home'))

# RUTAS PRINCIPALES
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/admin')
@admin_required
def admin():
    return render_template('admin.html')

# API JEFES
@app.route('/api/jefes', methods=['GET'])
def get_jefes():
    if not supabase: return jsonify([]), 500
    res = supabase.table('jefes').select('*').execute()
    return jsonify(res.data)

@app.route('/api/jefes', methods=['POST'])
@admin_required
def post_jefes():
    if not supabase: return jsonify([]), 500
    supabase.table('jefes').insert(request.json).execute()
    return jsonify({"status": "ok"}), 201

@app.route('/api/jefes/<id>', methods=['DELETE'])
@admin_required
def delete_jefe(id):
    if supabase: supabase.table('jefes').delete().eq('id', id).execute()
    return jsonify({"status": "deleted"})

# API NOVEDADES
@app.route('/api/novedades', methods=['GET'])
def get_novedades():
    if not supabase: return jsonify([]), 500
    res = supabase.table('novedades').select('*').order('id', desc=True).execute()
    return jsonify(res.data)

@app.route('/api/novedades', methods=['POST'])
@admin_required
def post_novedades():
    if not supabase: return jsonify([]), 500
    supabase.table('novedades').insert(request.json).execute()
    return jsonify({"status": "ok"}), 201

@app.route('/api/novedades/<id>', methods=['DELETE'])
@admin_required
def delete_novedad(id):
    if supabase: supabase.table('novedades').delete().eq('id', id).execute()
    return jsonify({"status": "deleted"})

# API ARMAS
@app.route('/api/armas', methods=['GET'])
def get_armas():
    if not supabase: return jsonify([]), 500
    res = supabase.table('armas').select('*').execute()
    return jsonify(res.data)

@app.route('/api/armas', methods=['POST'])
@admin_required
def post_armas():
    if not supabase: return jsonify([]), 500
    supabase.table('armas').insert(request.json).execute()
    return jsonify({"status": "ok"}), 201

@app.route('/api/armas/<id>', methods=['DELETE'])
@admin_required
def delete_arma(id):
    if supabase: supabase.table('armas').delete().eq('id', id).execute()
    return jsonify({"status": "deleted"})

# API MINERALES
@app.route('/api/minerales', methods=['GET'])
def get_minerales():
    if not supabase: return jsonify([]), 500
    res = supabase.table('minerales').select('*').execute()
    return jsonify(res.data)

@app.route('/api/minerales', methods=['POST'])
@admin_required
def post_minerales():
    if not supabase: return jsonify([]), 500
    supabase.table('minerales').insert(request.json).execute()
    return jsonify({"status": "ok"}), 201

@app.route('/api/minerales/<id>', methods=['DELETE'])
@admin_required
def delete_mineral(id):
    if supabase: supabase.table('minerales').delete().eq('id', id).execute()
    return jsonify({"status": "deleted"})

# API RECETAS
@app.route('/api/recetas', methods=['GET'])
def get_recetas():
    if not supabase: return jsonify([]), 500
    res = supabase.table('recetas').select('*').execute()
    return jsonify(res.data)

@app.route('/api/recetas', methods=['POST'])
@admin_required
def post_recetas():
    if not supabase: return jsonify([]), 500
    supabase.table('recetas').insert(request.json).execute()
    return jsonify({"status": "ok"}), 201

@app.route('/api/recetas/<id>', methods=['DELETE'])
@admin_required
def delete_receta(id):
    if supabase: supabase.table('recetas').delete().eq('id', id).execute()
    return jsonify({"status": "deleted"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
