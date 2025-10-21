import prettytable
import mysql.connector

#Clases
from clases.empleado import Empleado
from clases.usuario import Usuario

#Servicios
import MenuGestionEmpleado
import servicios.LimpiarPantalla as screen

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

def mostrar_menu1():
    screen.clear()
    print("")
    menu = prettytable.PrettyTable()
    menu.field_names = ["","Opciones"]
    menu.add_rows([
                    [1,"Gestonar Empleados"],
                    [0,"Salir"]
                  ])
    print(menu)

def main():
    conexion = conexionsql()
    salir = 1

    while salir == 1:
        mostrar_menu1()
        opcion = input("Opcion: ").strip()

        #Gestionar empleados
        if opcion == "1":
            MenuGestionEmpleado.menu_gestion_empelado(conexion)
        elif opcion == "0":
            salir = 0


    
main()