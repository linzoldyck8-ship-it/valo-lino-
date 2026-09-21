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

# API JEFES (ACTUALIZAR)
@app.route('/api/jefes/<id>', methods=['PUT'])
@admin_required
def update_jefe(id):
    if supabase: supabase.table('jefes').update(request.json).eq('id', id).execute()
    return jsonify({"status": "updated"})

# API NOVEDADES (ACTUALIZAR)
@app.route('/api/novedades/<id>', methods=['PUT'])
@admin_required
def update_novedad(id):
    if supabase: supabase.table('novedades').update(request.json).eq('id', id).execute()
    return jsonify({"status": "updated"})

# API ARMAS (ACTUALIZAR)
@app.route('/api/armas/<id>', methods=['PUT'])
@admin_required
def update_arma(id):
    if supabase: supabase.table('armas').update(request.json).eq('id', id).execute()
    return jsonify({"status": "updated"})

# API MINERALES (ACTUALIZAR)
@app.route('/api/minerales/<id>', methods=['PUT'])
@admin_required
def update_mineral(id):
    if supabase: supabase.table('minerales').update(request.json).eq('id', id).execute()
    return jsonify({"status": "updated"})

# API RECETAS (ACTUALIZAR)
@app.route('/api/recetas/<id>', methods=['PUT'])
@admin_required
def update_receta(id):
    if supabase: supabase.table('recetas').update(request.json).eq('id', id).execute()
    return jsonify({"status": "updated"})

# API UBICACIONES (ACTUALIZAR)
@app.route('/api/ubicaciones/<id>', methods=['PUT'])
@admin_required
def update_ubicacion(id):
    if supabase: supabase.table('ubicaciones').update(request.json).eq('id', id).execute()
    return jsonify({"status": "updated"})
