from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'clave-secreta-para-sesiones'  # Necesaria para usar sesiones.

# Ruta para la página principal y registro de inscritos.
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Obtener datos del formulario
        fecha = request.form['fecha']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        turno = request.form['turno']
        seminarios = request.form.getlist('seminarios')  # Obtener lista de seminarios

        # Crear el diccionario del registro
        registro = {
            'fecha': fecha,
            'nombre': nombre,
            'apellido': apellido,
            'turno': turno,
            'seminarios': ', '.join(seminarios)
        }

        # Guardar en la sesión (inicializa si no existe)
        if 'registros' not in session:
            session['registros'] = []

        session['registros'].append(registro)
        session.modified = True  # Indicar que la sesión ha cambiado

        return redirect(url_for('listado'))  # Redirigir a la lista de inscritos

    return render_template('index.html')

# Ruta para mostrar el listado de inscritos
@app.route('/listado')
def listado():
    registros = session.get('registros', [])  # Obtener registros de la sesión
    return render_template('listado.html', registros=registros)

# Ruta para eliminar un registro específico
@app.route('/eliminar/<int:id>')
def eliminar(id):
    registros = session.get('registros', [])
    if 0 <= id < len(registros):
        registros.pop(id)
        session.modified = True  # Indicar que la sesión ha cambiado
    return redirect(url_for('listado'))

# Ruta para editar un registro específico
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    registros = session.get('registros', [])
    
    if request.method == 'POST':
        # Actualizar el registro en la posición específica
        registros[id] = {
            'fecha': request.form['fecha'],
            'nombre': request.form['nombre'],
            'apellido': request.form['apellido'],
            'turno': request.form['turno'],
            'seminarios': ', '.join(request.form.getlist('seminarios'))
        }
        session.modified = True  # Marcar que la sesión ha cambiado
        return redirect(url_for('listado'))  # Redirigir al listado de inscritos

    # Si es un GET, mostrar los datos actuales en el formulario
    registro = registros[id]
    return render_template('index.html', registro=registro, id=id)

if __name__ == '__main__':
    app.run(debug=True)
