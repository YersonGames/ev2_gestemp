import prettytable
import mysql.connector
import time

# Clases
from clases.destino import Destino
# Servicios 
import servicios.ModificarDestino as ModificarDestino
import servicios.CrearDestino as CrearDestino
import servicios.LimpiarPantalla as screen
from servicios.EncriptarDesencriptar import encriptar,desencriptar

def mostrar_menu_gestion_destinos():
    screen.clear()
    print("")
    menu = prettytable.PrettyTable()
    menu.field_names = ["","Opciones"]
    menu.add_rows([
                    [1,"Crear Destino"],
                    [2,"Mostrar Destinos"],
                    [3,"Modificar Destino"],
                    [4,"Eliminar Destino"],
                    [0,"Volver"]
                  ])
    print(menu)

def mostrar_menu_modificar(datos):
    screen.clear()
    print("")
    menu = prettytable.PrettyTable()
    menu.field_names = ["","Opciones","Datos"]
    menu.add_rows([
                    [1,"Modificar Nombre",datos[0]],
                    [2,"Modificar Descripcion",""],
                    [3,"Modificar Actividades",""],
                    [4,"Modificar Costo",datos[3]],
                    [0,"Volver",""]
                  ])
    print(menu)

def menu_gestion_destinos(connect):
    conexion = connect
    salir = 0
    while salir == 0:
        mostrar_menu_gestion_destinos()
        opcion = input("Opcion: ")

        #Crear Destino
        if opcion == "1":
            tabla = prettytable.PrettyTable()
            tabla.field_names = ["Nombre","Descripcion","Actividades","Costo"]

            screen.clear()
            datos = CrearDestino.registrardatosdestino()
            destino = Destino(datos[0],datos[1],datos[2],datos[3])
            parametros = (destino.get_nombre(),destino.get_descripcion(),destino.get_actividades(),destino.get_costo())
            tabla.add_row([destino.get_nombre(),destino.get_descripcion(),destino.get_actividades(),destino.get_costo()])
            cursor = conexion.cursor()
            cursor.callproc("sp_destinos_crear",parametros)
            cursor.close()
            conexion.commit()
            screen.clear()
            print(tabla)
            print("Destino creado correctamente!")
            time.sleep(2)
        #Mostrar Destinos
        elif opcion == "2":
            tabla = prettytable.PrettyTable()
            tabla.field_names = ["Nombre Destino","Descripcion","Actividades","Costo"]

            cursor = conexion.cursor()
            cursor.callproc("sp_destino_listar")

            for result in cursor.stored_results():
                        lista = result.fetchall()
                        for l in lista:
                            tabla.add_row([l[0],l[1],l[2],l[3]])

            if len(tabla._rows) > 0:
                screen.clear()
                print(tabla)
                input("\nPresione [ENTER] para volver")
            else:
                print("\nNo hay destinos registrados")
                time.sleep(2)
            cursor.close()

        #Modificar Destino
        elif opcion == "3":
            nombre = input("Ingrese el nombre del Destino: ").title()
            parametros_ver  = (nombre,-1)
            cursor = conexion.cursor()
            verificar = cursor.callproc("sp_destino_verificar_nombre",parametros_ver)
            cursor.close()

            if verificar[-1] > 0:
                salir2 = 0
                while salir2 == 0:
                    parametros_mod = (verificar[-1],-1)
                    cursor = conexion.cursor()
                    cursor.callproc("sp_destino_get_id",parametros_mod)

                    for result in cursor.stored_results():
                        lista = result.fetchall()
                        for l in lista:
                            datos = l

                    cursor.close()
                    mostrar_menu_modificar(datos)
                    opcion = input("Opcion: ")

                    if opcion != "0":
                        data = ModificarDestino.modificardatosdestino(opcion,datos)
                        destino = Destino(data[0],data[1],data[2],data[3])
                        parametrosdestino = (destino.get_nombre(),destino.get_descripcion(),destino.get_actividades(),destino.get_costo(),verificar[-1])
                        cursor = conexion.cursor()
                        cursor.callproc("sp_destino_modificar",parametrosdestino)
                        cursor.close()
                        conexion.commit()
                        print("Datos modificados correctamente")
                        time.sleep(2)
                    else:
                        salir2 = 1
            else:
                print("El nombre no coincide con ningun destino")
                conexion.commit()
                time.sleep(2)

        #Eliminar destino
        elif opcion == "4":
            nombre = input("Ingrese el nombre del destino: ").title()
            parametros = (nombre,-1)
            cursor = conexion.cursor()
            verificar = cursor.callproc("sp_destino_verificar_nombre",parametros)
            cursor.close()
            if verificar[-1] > 0:
                cursor = conexion.cursor()
                cursor.callproc("sp_destino_eliminar",(verificar[-1],))
                cursor.close()
                conexion.commit()
                print("El Destino ha sido eliminado correctamente")
                time.sleep(2)
            else:
                print("El nombre no coincide con ningun destino")
                conexion.commit()
                time.sleep(2)
        #Salir
        elif opcion == "0":
            salir = 1
