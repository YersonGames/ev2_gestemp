import prettytable
import mysql.connector
import time

# Clases
from clases.proyecto import Proyecto

# Servicios 
import servicios.CrearProyecto as CrearProyecto
import servicios.LimpiarPantalla as screen

def mostrar_menu_gestion_proyecto():
    screen.clear()
    print("")
    menu = prettytable.PrettyTable()
    menu.field_names = ["","Opciones"]
    menu.add_rows([
                    [1,"Crear Proyecto"],
                    [2,"Eliminar Proyecto"],
                    [3,"Listar Proyecto"],
                    [4,"Buscar Proyecto"],
                    [0,"Volver"]
                  ])
    print(menu)


def menu_gestion_proyecto(connect):
    conexion = connect
    salir = 1
    while salir == 1:
        mostrar_menu_gestion_proyecto()
        opcion = input("Opcion: ").strip()

        #Crear proyecto
        if opcion == "1":
            try:
                tabla = prettytable.PrettyTable()
                tabla.field_names = ["Nombre","Descripcion","Fecha de inicio"]

                datos = CrearProyecto.registrardatosproyectos()

                proyecto = Proyecto(datos[0],datos[1], datos[2])
                tabla.add_row([proyecto.get_nombre(),proyecto.get_descripcion(),proyecto.get_fecha_inicio])

                parametros = (proyecto.get_nombre(),proyecto.get_descripcion,proyecto.get_fecha_inicio())
                cursor = conexion.cursor()
                cursor.callproc("sp_proyectos_crear",parametros)
                cursor.close()
                conexion.commit()
                print(tabla)
                print("proyecto creado correctamente!")
                time.sleep(2)
            except mysql.connector.errors.Error as error:
                print("Error: ",error)
                time.sleep(2)

        # Eliminar proyecto
        elif opcion == "2":
            nombre = input("Ingrese el nombre del proyecto: ").strip()
            parametros = (nombre,-1)

            cursor = conexion.cursor()
            verificar = cursor.callproc("sp_proyecto_eliminar_nombre",parametros)

            for result in cursor.stored_results():
                lista = result.fetchall()
                for l in lista:
                    nombre = l[0]

            if verificar[-1] != -1:
                print(f"El proyecto {nombre} ha sido eliminado")
            else:
                print("El nombre no coincide con ningun proyecto")

            time.sleep(2)

        # Listar proyecto
        elif opcion == "3":
            tabla = prettytable.PrettyTable()
            tabla.field_names = ["ID","Nombre","Descripcion","fecha_inicio"]

            cursor = conexion.cursor()
            cursor.callproc("sp_proyectos_listar")

            for result in cursor.stored_results():
                lista = result.fetchall()
                for l in lista:
                    verificar = l
                    tabla.add_row([l[0],l[1],l[2],l[3]])

            cursor.close()
            conexion.commit()
            if len(tabla._rows) > 0:
                screen.clear()
                print(tabla)
                input("\nPresione [ENTER] para volver")
            else:
                print("\nNo hay proyecto registrados")
                time.sleep(2)
        
        #Buscar proyecto por nombre
        elif opcion == "4":

            tabla = prettytable.PrettyTable()
            tabla.field_names = ["ID","Nombre","Descripcion","fecha_inicio"]

            nombre = input("Ingrese el nombre: ").strip()
            parametros = (nombre,-1)

            cursor = conexion.cursor()
            verificar = cursor.callproc("sp_proyectos_buscar",parametros)
            if verificar[-1] != -1:
                for result in cursor.stored_results():
                    lista = result.fetchall()
                    for l in lista:
                        tabla.add_row([l[0],l[1],l[2],l[3]])
                screen.clear()
                print(tabla)
                input("\nPresione [ENTER] para volver")
            else:
                print("\nProyecto no encontrado")
                time.sleep(2)
            
            cursor.close()
            conexion.commit()
        elif opcion == "0":
            salir = 0
    