import prettytable
import mysql.connector
from empleado import Empleado
from usuario import Usuario

#Crear conexion con base de datos
def conexionsql():
    conexion = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        #password="",
        database="gestemp_ecotech"
    )
    return conexion

def main():
    conexion = conexionsql()
    cursor = conexion.cursor()
    cursor.execute("select * from usuario")
    aa = cursor.fetchall()
    cursor.close()
    conexion.commit()

    table = prettytable.PrettyTable()
    table.field_names = ["Nombre","Direccion","Telefono","Email","RUN","Contrasena","Permiso","Fecha de Inicio","Salario"]
    a = Empleado("Hola","hola2","55555","hola2@email.com","222224","contraseña",1,"2025-08-31",15000)
    table.add_row([a.get_nombre(),a.get_direccion(),a.get_telefono(),a.get_email(),a.get_run(),a.get_contrasenahash(),a.get_permiso(),a.get_fecha_inicio(),a.get_salario()])


    parametros = (a.get_nombre(),a.get_direccion(),a.get_telefono(),a.get_email(),a.get_run(),a.get_contrasenahash(),a.get_permiso(),a.get_fecha_inicio(),a.get_salario())
    print(parametros)
    cursor = conexion.cursor()
    cursor.callproc("sp_empleado_registrar",parametros)
    cursor.close()
    conexion.commit()

    print(table)
    print(aa)
    
main()