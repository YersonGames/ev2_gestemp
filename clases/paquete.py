class Paquete:
    def __init__(self, nombre, fecha_inicio, fecha_fin, disponibilidad):
        self.nombre = nombre
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.disponibilidad = disponibilidad


    #Getters
    def get_nombre(self):
        return self.nombre
    def get_fechai(self):
        return self.fecha_inicio
    def get_fechaf(self):
        return self.fecha_fin
    def get_disponibilidad(self):
        return self.disponibilidad
    
