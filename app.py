import os
from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
import mysql.connector


app = Flask(__name__)

# Configuración MySQL
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            # Si están en la nube usa la variable de entorno, si no, usa el valor local
            host=os.environ.get('DB_HOST', 'localhost'),       # Cambiar 'localhost' si su servidor local es diferente
            port=int(os.environ.get('DB_PORT', 3306)),         # Cambiar 3306 si usan otro puerto local
            user=os.environ.get('DB_USER', 'root'),             # Tu usuario local de MySQL (ej. root)
            password=os.environ.get('DB_PASSWORD', ''),        # Tu contraseña local de MySQL (dejar '' si no tiene)
            database=os.environ.get('DB_NAME', 'inventario')         # Nombre de tu base de datos local
        )
        return connection
    except mysql.connector.Error as e:
        print(f"X Error de conexión a DB: {e}")
        raise
#app.config['MYSQL_HOST'] = 'localhost'
#app.config['MYSQL_USER'] = 'root'
#app.config['MYSQL_PASSWORD'] = ''
#app.config['MYSQL_DB'] = 'inventario'
#mysql = MySQL(app)

# Ruta principal: listar productos
@app.route('/')
def index():
    cur = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM productos")
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', productos=data)

# Agregar producto
@app.route('/agregar', methods=['POST'])
def agregar():
    if request.method == 'POST':
        nombre = request.form['nombre']
        cantidad = request.form['cantidad']
        precio = request.form['precio']
        cur = mysql.connector.cursor()
        cur.execute("INSERT INTO productos (nombre, cantidad, precio) VALUES (%s,%s,%s)", (nombre, cantidad, precio))
        conn.commit()
        cur.close()
        return redirect('/')
    return render_template('agregar.html')

# Editar producto
@app.route('/editar/<int:id>', methods=['POST'])
def editar(id):
    cur = get_db_connection()
    cur = conn.cursor()
    if request.method == 'POST':
        nombre = request.form['nombre']
        cantidad = request.form['cantidad']
        precio = request.form['precio']
        cur.execute("UPDATE productos SET nombre=%s, cantidad=%s, precio=%s WHERE id=%s", (nombre, cantidad, precio, id))
        conn.commit()
        cur.close()
        return redirect('/')
    cur.execute("SELECT * FROM productos WHERE id=%s", [id])
    producto = cur.fetchone()
    cur.close()
    return render_template('editar.html', producto=producto)

# Eliminar producto
@app.route('/eliminar/<int:id>')
def eliminar(id):
    cur = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM productos WHERE id=%s", [id])
    conn.commit()
    cur.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
