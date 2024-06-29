import mysql.connector

class Catalogo:
    
    def __init__(self, host, user, password, database):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        
        self.cursor = self.conn.cursor(dictionary=True)
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS productos (
            codigo INT AUTO_INCREMENT PRIMARY KEY,
            descripcion VARCHAR(255) NOT NULL,
            cantidad INT NOT NULL,
            precio DECIMAL(10, 2) NOT NULL,
            imagen_url VARCHAR(255),
            proveedor INT(4))''')
        self.conn.commit()
        
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
    
    
    
catalogo= Catalogo(host='localhost', user='root', password='root', database='miapp')

# Agregamos productos a la tabla
#catalogo.agregar_producto('Teclado USB 101 teclas', 10, 4500, 'teclado.jpg', 101)
#catalogo.agregar_producto('Mouse USB 3 botones', 5, 2500, 'mouse.jpg', 102)
#catalogo.agregar_producto('Monitor LED', 5, 25000, 'monitor.jpg', 102)

# Consultamos un producto y lo mostramos
"""cod_prod = int(input("Ingrese el código del producto: "))
producto = catalogo.consultar_producto(cod_prod)
if producto: 
    print(f"Producto encontrado: {producto['codigo']} -{producto['descripcion']}")
else:
    print(f'Producto {cod_prod} no encontrado.')
    """
##catalogo.modificar_producto(1, 'Teclado USB 101 teclassssssssss', 10, 4500, 'teclado.jpg', 101)

#catalogo.eliminar_producto(2)