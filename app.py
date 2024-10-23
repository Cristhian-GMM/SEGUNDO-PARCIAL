from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Inicializa los productos en la sesión
def inicializar_productos():
    if 'productos' not in session:
        session['productos'] = []

@app.route('/')
def index():
    inicializar_productos()
    return render_template('index.html', productos=session['productos'])

@app.route('/nuevo', methods=['GET', 'POST'])
def nuevo_producto():
    if request.method == 'POST':
        id = len(session['productos']) + 1
        nombre = request.form['nombre']
        cantidad = int(request.form['cantidad'])
        precio = float(request.form['precio'])
        fecha_vencimiento = request.form['fecha_vencimiento']
        categoria = request.form['categoria']

        producto = {
            'id': id,
            'nombre': nombre,
            'cantidad': cantidad,
            'precio': precio,
            'fecha_vencimiento': fecha_vencimiento,
            'categoria': categoria
        }

        session['productos'].append(producto)
        session.modified = True
        flash('¡Producto agregado exitosamente!', 'success')
        return redirect(url_for('index'))

    return render_template('nuevo.html')

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    inicializar_productos()
    producto = next((p for p in session['productos'] if p['id'] == id), None)

    if request.method == 'POST':
        producto['nombre'] = request.form['nombre']
        producto['cantidad'] = int(request.form['cantidad'])
        producto['precio'] = float(request.form['precio'])
        producto['fecha_vencimiento'] = request.form['fecha_vencimiento']
        producto['categoria'] = request.form['categoria']

        session.modified = True
        flash('¡Producto actualizado exitosamente!', 'info')
        return redirect(url_for('index'))

    return render_template('editar.html', producto=producto)

@app.route('/eliminar/<int:id>')
def eliminar_producto(id):
    inicializar_productos()
    session['productos'] = [p for p in session['productos'] if p['id'] != id]
    session.modified = True
    flash('¡Producto eliminado exitosamente!', 'danger')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)