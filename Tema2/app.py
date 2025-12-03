from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from config import DB_CONFIG

app = Flask(__name__)
app.secret_key = 'cambiame_por_una_clave_segura'

def get_db():
    return mysql.connector.connect(**DB_CONFIG)

@app.route('/')
def dashboard():
    return render_template('index.html')

@app.route('/formulario')
def formulario():
    return render_template('formulario.html')

@app.route('/guardar', methods=['POST'])
def guardar():
    nombre = request.form.get('nombre')
    correo = request.form.get('correo')
    cel = request.form.get('cel')
    horario = request.form.get('horario')
    ganado = request.form.get('ganado')

    if not nombre or not correo:
        flash('Nombre y correo son obligatorios')
        return redirect(url_for('formulario'))

    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO solicitudes (nombre, correo, cel, horario, ganado) VALUES (%s, %s, %s, %s, %s)",
        (nombre, correo, cel, horario, ganado)
    )
    db.commit()
    cursor.close()
    db.close()

    flash('Solicitud guardada correctamente')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    # 0.0.0.0 para ser accesible desde cualquier IPv4 del equipo
    app.run(host='0.0.0.0', port=5000)
