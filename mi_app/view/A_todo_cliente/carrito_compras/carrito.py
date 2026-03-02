class Carrito:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        carrito = self.session.get("carrito")
        if not carrito:
            carrito = self.session["carrito"] = {}
        self.carrito = carrito

    def agregar(self, producto, cantidad=1):
        id = str(producto.id)
        if id not in self.carrito.keys():
            self.carrito[id] = {
                "producto_id": producto.id,
                "nombre": producto.id_presentacion.nombre,
                "precio": int(producto.valor_unitario),
                "cantidad": int(cantidad),
                "imagen": producto.logo_producto.url if producto.logo_producto else "",
                "total": int(producto.valor_unitario) * int(cantidad)
            }
        else:
            self.carrito[id]["cantidad"] += int(cantidad)
            self.carrito[id]["total"] = int(self.carrito[id]["precio"]) * self.carrito[id]["cantidad"]
        self.guardar_carrito()
        
    def guardar_carrito(self):
        self.session["carrito"] = self.carrito
        self.session.modified = True

    @property
    def total_carrito(self):
        # Usamos int() para evitar la aparición de .0 en el front-end
        return sum(int(item['precio']) * item['cantidad'] for item in self.carrito.values())
    
    def restar(self, producto):
        id = str(producto.id)
        if id in self.carrito.keys():
            self.carrito[id]["cantidad"] -= 1
            # Actualizamos total usando int()
            self.carrito[id]["total"] = int(self.carrito[id]["precio"]) * self.carrito[id]["cantidad"]
            if self.carrito[id]["cantidad"] <= 0:
                self.eliminar(producto)
            else:
                self.guardar_carrito()

    def eliminar(self, producto):
        id = str(producto.id)
        if id in self.carrito.keys():
            del self.carrito[id]
            self.guardar_carrito()