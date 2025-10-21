import prettytable
import mysql.connector

#Clases
from clases.empleado import Empleado
from clases.usuario import Usuario

#Servicios
import RegistroEmpleado

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

def mostrar_menu_gestion():
    print("")
    menu = prettytable.PrettyTable()
    menu.field_names = ["","Opciones"]
    menu.add_rows([
                    [1,"Registrar/Modificar Empleado"],
                    [2,"Listar Empelados"],
                    [0,"Salir"]
                  ])
    print(menu)

def main():
    conexion = conexionsql()
    salir = 1

    while salir == 1:
        mostrar_menu_gestion()
        opcion = input("Opcion: ")

        if opcion == "1":
            try:
                tabla = prettytable.PrettyTable()
                tabla.field_names = ["Nombre","Direccion","Telefono","Email","RUN","Permiso","Fecha de Inicio","Salario"]

                datos = RegistroEmpleado.registrardatos()

                empleado = Empleado(datos[0],datos[1],datos[2],datos[3],datos[4],datos[5],datos[6],datos[7],datos[8])
                tabla.add_row([empleado.get_nombre(),empleado.get_direccion(),empleado.get_telefono(),empleado.get_email(),empleado.get_run(),empleado.get_permiso(),empleado.get_fecha_inicio(),empleado.get_salario()])

                parametros = (empleado.get_nombre(),empleado.get_direccion(),empleado.get_telefono(),empleado.get_email(),empleado.get_run(),empleado.get_contrasenahash(),empleado.get_permiso(),empleado.get_fecha_inicio(),empleado.get_salario())
                cursor = conexion.cursor()
                cursor.callproc("sp_empleado_registrar",parametros)
                cursor.close()
                conexion.commit()
                print(tabla)
                print("Empleado registrado correctamente!")
            except mysql.connector.errors.Error as error:
                print("Error: ",error)


        elif opcion == "2":

            tabla = prettytable.PrettyTable()
            tabla.field_names = ["ID","Nombre","Direccion","Telefono","Email","RUN","Permiso","Fecha de Inicio","Salario"]

            cursor = conexion.cursor()
            cursor.callproc("sp_empleado_listar")

            for result in cursor.stored_results():
                lista = result.fetchall()
                for l in lista:
                    tabla.add_row([l[0],l[1],l[2],l[3],l[4],l[5],l[6],l[7],l[8]])

            print(tabla)
            cursor.close()
            conexion.commit()
    
main()