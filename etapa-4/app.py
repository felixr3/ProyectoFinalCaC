"""
seccion back    
"""
import os
import time
from flask import Flask, request, jsonify
# Instalar con pip install flask-cors
from flask_cors import CORS
# Instalar con pip install mysql-connector-python
import mysql.connector
# Si es necesario, pip install Werkzeug
from werkzeug.utils import secure_filename
# No es necesario instalar, es parte del sistema standard de Python



app = Flask(__name__)
CORS(app)

class Catalogo:
    #----------------------------------------------------------------
# Constructor de la clase
    def __init__(self, host, user, password, database):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        
        self.cursor = self.conn.cursor()
        
        try:
            self.cursor.execute(f"USE {database}")
        except mysql.connector.Error as err:
           # Si la base de datos no existe, la creamos
            if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                self.cursor.execute(f"CREATE DATABASE {database}")
                self.conn.database = database
            else:
                raise err
            
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS productos (
                codigo INT AUTO_INCREMENT PRIMARY KEY, descripcion VARCHAR(255) NOT NULL,
                cantidad INT NOT NULL,precio DECIMAL(10, 2) NOT NULL,imagen_url VARCHAR(255),
                proveedor INT(4))''')
            
            self.conn.commit()
            
            self.cursor.close()
            self.cursor = self.conn.cursor(dictionary=True)
#######################################################################
#######################################################################
    
    def agregar_producto(self, descripcion, cantidad, precio, imagen, proveedor):
        sql = "INSERT INTO productos (descripcion, cantidad, precio, imagen_url, proveedor) VALUES (%s, %s, %s, %s, %s)"
        valores = (descripcion, cantidad, precio, imagen, proveedor)
        self.cursor.execute(sql, valores)
        self.conn.commit()
        return self.cursor.lastrowid
    
    def consultar_producto(self, codigo):
# Consultamos un producto a partir de su código
        self.cursor.execute(f"SELECT * FROM productos WHERE codigo = {codigo}")
        return self.cursor.fetchone()
    
    
    def modificar_producto(self, codigo, nueva_descripcion, nueva_cantidad, nuevo_precio, nueva_imagen, nuevo_proveedor):
        sql = "UPDATE productos SET descripcion = %s, cantidad = %s, precio = %s, imagen_url = %s, proveedor = %s WHERE codigo = %s"
        valores = (nueva_descripcion, nueva_cantidad, nuevo_precio, nueva_imagen, nuevo_proveedor, codigo)
        self.cursor.execute(sql, valores)
        self.conn.commit()
        return self.cursor.rowcount > 0
    
    def listar_productos(self):
        self.cursor.execute("SELECT * FROM productos")
        productos = self.cursor.fetchall()
        return productos
    
    def eliminar_producto(self, codigo):
# Eliminamos un producto de la tabla a partir de su código
        self.cursor.execute(f"DELETE FROM productos WHERE codigo = {codigo}")
        self.conn.commit()
        return self.cursor.rowcount > 0
    
    def mostrar_producto(self, codigo):
# Mostramos los datos de un producto a partir de su código
        producto = self.consultar_producto(codigo)
        if producto:
            print("-" * 40)
            print(f"Código.....: {producto['codigo']}")
            print(f"Descripción: {producto['descripcion']}")
            print(f"Cantidad...: {producto['cantidad']}")
            print(f"Precio.....: {producto['precio']}")
            print(f"Imagen.....: {producto['imagen_url']}")
            print(f"Proveedor..: {producto['proveedor']}")
            print("-" * 40)
        else:
            print("Producto no encontrado.")
            
    
    
    # Cuerpo del programa
    #--------------------------------------------------------------------
    # Crear una instancia de la clase Catalogo
catalogo = Catalogo(host='cac2024TPF.mysql.pythonanywhere-services.com', user='cac2024TPF', password='123456789_', database='cac2024TPF$tpfinal')
# Carpeta para guardar las imagenes
ruta_destino = '/home/cac2024TPF/mysite/static/imagenes/'


@app.route("/productos", methods=["GET"])
def listar_productos():
    productos = catalogo.listar_productos()
    return jsonify(productos)

@app.route("/productos/<int:codigo>", methods=["GET"])
def mostrar_producto(codigo):
    producto = catalogo.consultar_producto(codigo)
    if producto:
        return jsonify(producto), 201
    else:
        return "Producto no encontrado", 404
    
    
@app.route("/productos", methods=["POST"])
def agregar_producto():
#Recojo los datos del form
    descripcion = request.form['descripcion']
    cantidad = request.form['cantidad']
    precio = request.form['precio']
    imagen = request.files['imagen']
    proveedor = request.form['proveedor']
    nombre_imagen = ""
# Genero el nombre de la imagen
    nombre_imagen = secure_filename(imagen.filename)
    nombre_base, extension = os.path.splitext(nombre_imagen)
    nombre_imagen = f"{nombre_base}_{int(time.time())}{extension}"
    nuevo_codigo = catalogo.agregar_producto(descripcion, cantidad, precio, nombre_imagen, proveedor)
    if nuevo_codigo:
        print(f"Ruta completa de la imagen: {ruta_destino}")
        rutCom= imagen.save(os.path.join(ruta_destino, nombre_imagen))
        print(f"Ruta completa de la imagen: {rutCom}")
        return jsonify({"mensaje": "Producto agregado correctamente.",
                        "codigo": nuevo_codigo, "imagen": nombre_imagen}), 201
    else:
        return jsonify({"mensaje": "Error al agregar el producto."}), 500




@app.route("/productos/<int:codigo>", methods=["PUT"])
def modificar_producto(codigo):
#Se recuperan los nuevos datos del formulario
    nueva_descripcion = request.form.get("descripcion")
    nueva_cantidad = request.form.get("cantidad")
    nuevo_precio = request.form.get("precio")
    nuevo_proveedor = request.form.get("proveedor")
# Verifica si se proporcionó una nueva imagen
    if 'imagen' in request.files:
        imagen = request.files['imagen']
# Procesamiento de la imagen
        nombre_imagen = secure_filename(imagen.filename) 
        nombre_base, extension = os.path.splitext(nombre_imagen) 
        nombre_imagen = f"{nombre_base}_{int(time.time())}{extension}"
# Guardar la imagen en el servidor
        imagen.save(os.path.join(ruta_destino, nombre_imagen))
# Busco el producto guardado
        producto = catalogo.consultar_producto(codigo)
        if producto: # Si existe el producto...
            imagen_vieja = producto["imagen_url"]
# Armo la ruta a la imagen
            ruta_imagen = os.path.join(ruta_destino, imagen_vieja)
# Y si existe la borro.
            if os.path.exists(ruta_imagen):
                os.remove(ruta_imagen)
    else:
        producto = catalogo.consultar_producto(codigo)
        if producto:
            nombre_imagen = producto["imagen_url"]
    
    if catalogo.modificar_producto(codigo, nueva_descripcion, nueva_cantidad, nuevo_precio, nombre_imagen, nuevo_proveedor):
        return jsonify({"mensaje": "Producto modificado"}), 200
    else:
        return jsonify({"mensaje": "Producto no encontrado"}), 403



@app.route("/productos/<int:codigo>", methods=["DELETE"])
def eliminar_producto(codigo):
# Primero, obtiene la información del producto para encontrar la imagen
    producto = catalogo.consultar_producto(codigo)
    if producto:
        ruta_imagen = os.path.join(ruta_destino, producto[4])
        if os.path.exists(ruta_imagen):
            os.remove(ruta_imagen)
        if catalogo.eliminar_producto(codigo):
            return jsonify({"mensaje": "Producto eliminado"}), 200
        else:
            return jsonify({"mensaje": "Error al eliminar el producto"}), 500
    else:
        return jsonify({"mensaje": "Producto no encontrado"}), 404




if __name__ == "__main__":
    app.run(debug=True)
