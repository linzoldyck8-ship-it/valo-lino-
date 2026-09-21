import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from functools import wraps
from supabase import create_client, Client

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'clave_secreta_scarletcraft')

SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')

supabase: Client = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        print("Error al conectar con Supabase:", e)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return jsonify({'error': 'No autorizado. Inicia sesión nuevamente.'}), 401
        return f(*args, **kwargs)
    return decorated_function

# --- VISTAS / PÁGINAS ---
@app.route('/')
def index():
    jefes = []
    if supabase:
        try:
            res = supabase.table('jefes').select('*').order('creado_en', desc=True).execute()
            jefes = res.data if res.data else []
        except Exception as e:
            print("Error cargando jefes en inicio:", e)
    return render_template('index.html', jefes=jefes)

@app.route('/admin')
def admin():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('admin.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin123')
        if password == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('admin'))
        return render_template('login.html', error='Contraseña incorrecta')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

# --- API CRUD UNIFICADA ---
TABLAS_PERMITIDAS = ['jefes', 'novedades', 'armas', 'minerales', 'recetas', 'ubicaciones']

@app.route('/api/<tabla>', methods=['GET'])
def get_items(tabla):
    if tabla not in TABLAS_PERMITIDAS:
        return jsonify({'error': 'Tabla no válida'}), 400
    if not supabase:
        return jsonify([])
    try:
        res = supabase.table(tabla).select('*').execute()
        return jsonify(res.data if res.data else [])
    except Exception as e:
        print(f"Error al obtener {tabla}:", e)
        return jsonify([]), 500

@app.route('/api/<tabla>', methods=['POST'])
@admin_required
def create_item(tabla):
    if tabla not in TABLAS_PERMITIDAS:
        return jsonify({'error': 'Tabla no válida'}), 400
    if not supabase:
        return jsonify({'error': 'Base de datos no conectada'}), 500
    try:
        data = request.get_json()
        res = supabase.table(tabla).insert(data).execute()
        return jsonify({'status': 'created', 'data': res.data})
    except Exception as e:
        print(f"Error al crear en {tabla}:", e)
        return jsonify({'error': str(e)}), 500

@app.route('/api/<tabla>/<id>', methods=['PUT'])
@admin_required
def update_item(tabla, id):
    if tabla not in TABLAS_PERMITIDAS:
        return jsonify({'error': 'Tabla no válida'}), 400
    if not supabase:
        return jsonify({'error': 'Base de datos no conectada'}), 500
    try:
        data = request.get_json()
        res = supabase.table(tabla).update(data).eq('id', id).execute()
        return jsonify({'status': 'updated', 'data': res.data})
    except Exception as e:
        print(f"Error al actualizar {tabla}:", e)
        return jsonify({'error': str(e)}), 500

@app.route('/api/<tabla>/<id>', methods=['DELETE'])
@admin_required
def delete_item(tabla, id):
    if tabla not in TABLAS_PERMITIDAS:
        return jsonify({'error': 'Tabla no válida'}), 400
    if not supabase:
        return jsonify({'error': 'Base de datos no conectada'}), 500
    try:
        res = supabase.table(tabla).delete().eq('id', id).execute()
        return jsonify({'status': 'deleted', 'data': res.data})
    except Exception as e:
        print(f"Error al eliminar de {tabla}:", e)
        return jsonify({'error': str(e)}), 500
