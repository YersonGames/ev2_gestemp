class Destino:
    def __init__(self, nombre, descripcion, actividades, costo):
        self.nombre = nombre
        self.descripcion = descripcion
        self.actividades = actividades
        self.costo = costo


    #Getters
    def get_nombre(self):
        return self.nombre
    def get_descripcion(self):
        return self.descripcion
    def get_actividades(self):
        return self.actividades
    def get_costo(self):
        return self.costo
    
