import prettytable
import mysql.connector
import time

# Clases
from clases.paquete import Paquete
# Servicios 
import servicios.ModificarPaquete as ModificarPaquete
import servicios.CrearPaquete as CrearPaquete
import servicios.LimpiarPantalla as screen
from servicios.EncriptarDesencriptar import encriptar,desencriptar

def mostrar_menu_gestion_paquetes():
    screen.clear()
    print("")
    menu = prettytable.PrettyTable()
    menu.field_names = ["","Opciones"]
    menu.add_rows([
                    [1,"Crear Paquete"],
                    [2,"Mostrar Paquetes"],
                    [3,"Modificar Paquete"],
                    [4,"Agregar Destino"],
                    [5,"Mostrar Destinos"],
                    [6,"Eliminar Destino"],
                    [7,"Eliminar Paquete"],
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
                    [2,"Modificar Fecha Inicio",datos[1]],
                    [3,"Modificar Fecha Fin",datos[2]],
                    [4,"Modificar Disponibilidad",datos[3]],
                    [0,"Volver",""]
                  ])
    print(menu)

def menu_gestion_paquetes(connect):
    conexion = connect
    salir = 0
    while salir == 0:
        mostrar_menu_gestion_paquetes()
        opcion = input("Opcion: ")

        #Crear Paquete
        if opcion == "1":
            tabla = prettytable.PrettyTable()
            tabla.field_names = ["Nombre","Fecha Inicio","Fecha Fin","Disponibilidad"]

            screen.clear()
            datos = CrearPaquete.registrardatosdestino()
            paquete = Paquete(datos[0],datos[1],datos[2],datos[3])
            parametros = (paquete.get_nombre(),paquete.get_fechai(),paquete.get_fechaf(),paquete.get_disponibilidad())
            tabla.add_row([paquete.get_nombre(),paquete.get_fechai(),paquete.get_fechaf(),paquete.get_disponibilidad()])
            cursor = conexion.cursor()
            cursor.callproc("sp_paquetes_crear",parametros)
            cursor.close()
            conexion.commit()
            screen.clear()
            print(tabla)
            print("Paquete creado correctamente!")
            time.sleep(2)
        #Mostrar Paquetes
        elif opcion == "2":
            tabla = prettytable.PrettyTable()
            tabla.field_names = ["Nombre","Fecha Inicio","Fecha Fin","Disponibilidad","Precio"]

            cursor = conexion.cursor()
            cursor.callproc("sp_paquete_listar")

            for result in cursor.stored_results():
                        lista = result.fetchall()
                        for l in lista:
                            tabla.add_row([l[0],l[1],l[2],l[3],l[4]])

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
            nombre = input("Ingrese el nombre del Paquete: ").title()
            parametros_ver  = (nombre,-1)
            cursor = conexion.cursor()
            verificar = cursor.callproc("sp_paquete_verificar_nombre",parametros_ver)
            cursor.close()

            if verificar[-1] > 0:
                salir2 = 0
                while salir2 == 0:
                    parametros_mod = (verificar[-1],-1)
                    cursor = conexion.cursor()
                    cursor.callproc("sp_paquete_get_id",parametros_mod)

                    for result in cursor.stored_results():
                        lista = result.fetchall()
                        for l in lista:
                            datos = l

                    cursor.close()
                    mostrar_menu_modificar(datos)
                    opcion = input("Opcion: ")

                    if opcion != "0":
                        data = ModificarPaquete.registrardatospaquete(opcion,datos)
                        paquete = Paquete(data[0],data[1],data[2],data[3])
                        parametrospaquete = (paquete.get_nombre(),paquete.get_fechai(),paquete.get_fechaf(),paquete.get_disponibilidad(),verificar[-1])
                        cursor = conexion.cursor()
                        cursor.callproc("sp_paquete_modificar",parametrospaquete)
                        cursor.close()
                        conexion.commit()
                        print("Datos modificados correctamente")
                        time.sleep(2)
                    else:
                        salir2 = 1
            else:
                print("El nombre no coincide con ningun paquete")
                conexion.commit()
                time.sleep(2)

        #Agregar destino
        elif opcion == "4":
            nombre_paquete = input("Ingrese el nombre del paquete: ").title()
            parametros_paq  = (nombre_paquete,-1)
            cursor = conexion.cursor()
            verificar_paq = cursor.callproc("sp_paquete_verificar_nombre",parametros_paq)
            cursor.close()
            if verificar_paq[-1] > 0:
                nombre_destino = input("Ingrese el nombre del destino: ").title()
                parametros_des  = (nombre_destino,-1)
                cursor = conexion.cursor()
                verificar_des = cursor.callproc("sp_destino_verificar_nombre",parametros_des)
                cursor.close()
                if verificar_des[-1] > 0:
                    parametros = (verificar_paq[-1],verificar_des[-1])
                    cursor = conexion.cursor()
                    verificar_des = cursor.callproc("sp_paquete_destino_anadir",parametros)
                    cursor.close()
                    print("Destino añadido correctamente al Paquete")
                    time.sleep(2)
                    conexion.commit()
                else:
                    print("El nombre no coincide con ningun destino")
                    conexion.commit()
                    time.sleep(2)
            else:
                print("El nombre no coincide con ningun paquete")
                conexion.commit()
                time.sleep(2)
        
        #Mostrar Destinos
        elif opcion == "5":
            tabla = prettytable.PrettyTable()
            tabla.field_names = ["Destinos","Costo"]
            nombre_paquete = input("Ingrese el nombre del paquete: ").title()
            parametros_paq  = (nombre_paquete,-1)
            cursor = conexion.cursor()
            verificar_paq = cursor.callproc("sp_paquete_verificar_nombre",parametros_paq)
            cursor.close()
            if verificar_paq[-1] > 0:
                parametros = (verificar_paq[-1],)
                cursor = conexion.cursor()
                cursor.callproc("sp_paquete_destino_listar",parametros)

                for result in cursor.stored_results():
                    lista = result.fetchall()
                    for l in lista:
                        tabla.add_row([l[0],l[1]])

                if len(tabla._rows) > 0:
                    screen.clear()
                    print(tabla)
                    input("\nPresione [ENTER] para volver")
                else:
                    print("\nNo hay destinos registrados")
                    time.sleep(2)
                cursor.close()
            else:
                print("El nombre no coincide con ningun paquete")
                conexion.commit()
                time.sleep(2)
        #Eliminar destino
        elif opcion == "7":
            nombre = input("Ingrese el nombre del paquete: ")
            parametros = (nombre,-1)
            cursor = conexion.cursor()
            verificar = cursor.callproc("sp_paquete_verificar_nombre",parametros)
            cursor.close()
            if verificar[-1] > 0:
                cursor = conexion.cursor()
                cursor.callproc("sp_paquete_eliminar",(verificar[-1],))
                cursor.close()
                conexion.commit()
                print("El Paquete ha sido eliminado correctamente")
                time.sleep(2)
            else:
                print("El nombre no coincide con ningun paquete")
                conexion.commit()
                time.sleep(2)
        #Salir
        elif opcion == "0":
            salir = 1
