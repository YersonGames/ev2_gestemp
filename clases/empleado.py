from clases.usuario import Usuario

class Empleado(Usuario):
    def __init__(self, nombre, direccion, telefono, email, run, contrasenahash, permiso,fecha_inicio,salario):
        super().__init__(nombre, direccion, telefono, email, run, contrasenahash, permiso)
        self.fecha_inicio = fecha_inicio
        self.salario = salario

    #Getters
    def get_nombre(self):
        return self.nombre
    def get_direccion(self):
        return self.direccion
    def get_telefono(self):
        return self.telefono
    def get_email(self):
        return self.email
    def get_run(self):
        return self.run
    def get_contrasenahash(self):
        return self.contrasenahash
    def get_permiso(self):
        return self.permiso
    def get_fecha_inicio(self):
        return self.fecha_inicio
    def get_salario(self):
        return self.salario
    def get_departamentos(self):
        return self.departamentos
    def get_proyectos(self):
        return self.proyectos
    
    def mostrar_info(self):
        info = self.nombre,self.direccion,self.telefono,self.email,self.run,self.permiso,self.fecha_inicio,self.salario
        return info
    
