class Proyecto():
    def __init__(self, nombre: str, descripcion: str, fecha_inicio: str):
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha_inicio = fecha_inicio

    # Getters
    def get_nombre(self):
        return self.nombre
    def get_descripcion(self):
        return self.descripcion
    def get_fecha_inicio(self):
        return self.fecha_inicio
    
    def mostrar_info(self):
        info = self.nombre, self.descripcion, self.fecha_inicio
        return info