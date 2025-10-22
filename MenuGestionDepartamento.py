import prettytable
import mysql.connector
import time

# Clases
from clases.departamento import Departamento

# Servicio
import servicios.LimpiarPantalla as screen

def mostrar_menu_gestion_departamento():
    screen.clear()
    print("")
    menu = prettytable.PrettyTable()
    menu.field_names = ["","Opciones"]
    menu.add_rows([
                    [1,"Crear Departamento"],
                    [2,"Modificar Departamento"],
                    [3,"Eliminar Departamento"],
                    [4,"Listar Departamento"],
                    [5,"Buscar Departamento"],
                    [6,"Asignar Empleado"],
                    [7,"Asignar Gerente"],
                    [0,"Volver"]
                  ])
    print(menu)

# def menu_gestion_departamento(connect):
#     conexion = connect

#     salir = 1

#     while salir == 1:

