class Catalogo:
    productos=[]
    
    # agregar un producto
    def agregar_producto(self, codigo, descripcion, cantidad, precio, imagen, proveedor):
        if self.consultar_producto(codigo):
            return False
        nuevo_producto = {
            'codigo': codigo,
            'descripcion': descripcion,
            'cantidad': cantidad,
            'precio': precio,
            'imagen': imagen,
            'proveedor': proveedor
        }
        self.productos.append(nuevo_producto)
        return True   #producto agregado



    def consultar_producto(self, codigo):
        for producto in self.productos:
            if producto['codigo'] == codigo:
                return producto
        return False

    def listar_productos(self):
        print("-" * 50)
        for producto in self.productos:
            print(f"Código.....: {producto['codigo']}")
            print(f"Descripción: {producto['descripcion']}") 
            print(f"Cantidad...: {producto['cantidad']}") 
            print(f"Precio.....: {producto['precio']}") 
            print(f"Imagen.....: {producto['imagen']}") 
            print(f"Proveedor..: {producto['proveedor']}") 
            print("-" * 50) 


    def modificar_producto(self, codigo, nueva_descripcion, nueva_cantidad, nuevo_precio, nueva_imagen, nuevo_proveedor): 
        for producto in self.productos: 
            if producto['codigo'] == codigo: 
                producto['descripcion'] = nueva_descripcion 
                producto['cantidad'] = nueva_cantidad 
                producto['precio'] = nuevo_precio 
                producto['imagen'] = nueva_imagen 
                producto['proveedor'] = nuevo_proveedor 
                return True 
        return False 

    def eliminar_producto(self, codigo): 
        for producto in self.productos: 
            if producto['codigo'] == codigo: 
                self.productos.remove(producto) 
                return True 
        return False 
    
    
    def mostrar_producto(self, codigo): 
        producto = self.consultar_producto(codigo) 
        if producto: 
            print("-" * 50) 
            print(f"Código.....: {producto['codigo']}") 
            print(f"Descripción: {producto['descripcion']}") 
            print(f"Cantidad...: {producto['cantidad']}") 
            print(f"Precio.....: {producto['precio']}") 
            print(f"Imagen.....: {producto['imagen']}") 
            print(f"Proveedor..: {producto['proveedor']}") 
            print("-" * 50) 
        else: 
            print("Producto no encontrado.")

catalogo = Catalogo()
catalogo.agregar_producto(1, 'Teclado USB 101 teclas', 10, 4500, 'teclado.jpg', 101) 
catalogo.agregar_producto(2, 'Mouse USB 3 botones', 5, 2500, 'mouse.jpg', 102) 
catalogo.agregar_producto(3, 'Monitor LCD 22 pulgadas', 15, 52500, 'monitor22.jpg', 103) 

#catalogo.listar_productos()

#catalogo.modificar_producto(1, 'Teclado USB 101 teclasssssssss', 10, 4500, 'teclado.jpg', 101)
#catalogo.eliminar_producto(2)
catalogo.mostrar_producto(20)