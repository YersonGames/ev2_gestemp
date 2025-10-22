class Departamento():
    def __init__(self, nombre:str, descripcion:str):
        self.nombre = nombre
        self.descripcion = descripcion

    #Getters
    def get_nombre(self):
        return self.nombre
    def get_descripcion(self):
        return self.descripcion
    
    def mostrar_info(self):
        info = self.nombre,self.descripcion
        return info