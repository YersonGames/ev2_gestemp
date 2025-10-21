class Usuario:
    def __init__(self,nombre:str,direccion:str,telefono:str,email:str,run:str,contrasenahash:str,permiso:int):
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono
        self.email = email
        self.run = run
        self.contrasenahash = contrasenahash
        self.permiso = permiso