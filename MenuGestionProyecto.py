import prettytable
import mysql.connector
import time

# Clases
from clases.proyecto import Proyecto

# Servicios 
import servicios.CrearProyecto as CrearProyecto
import servicios.LimpiarPantalla as screen
import servicios.ModificarProyecto as ModificarProyecto
from servicios.EncriptarDesencriptar import encriptar,desencriptar

def mostrar_menu_gestion_proyecto():
    screen.clear()
    print("")
    menu = prettytable.PrettyTable()
    menu.field_names = ["","Opciones"]
    menu.add_rows([
                    [1,"Crear Proyecto"],
                    [2,"Modificar Proyecto"],
                    [3,"Eliminar Proyecto"],
                    [4,"Listar Proyecto"],
                    [5,"Buscar Proyecto"],
                    [6,"Gestion Asignación Empleado"],
                    [0,"Volver"]
                  ])
    print(menu)

def mostrar_menu_modificar_proyecto(datos):
    screen.clear()
    print("")
    menu = prettytable.PrettyTable()
    menu.field_names = ["","Opciones","Datos"]
    menu.add_rows([
                    [1,"Modificar Nombre",datos[0]],
                    [2,"Modificar Descripcion",datos[1]],
                    [0,"Volver",""]
                  ])
    print(menu)

def mostrar_menu_gestion_empleado():
    screen.clear()
    print("")
    menu = prettytable.PrettyTable()
    menu.field_names = ["","Opciones"]
    menu.add_rows([
                    [1,"Asignar Empleado a Proyecto"],
                    [2,"Eliminar Empelado a Proyecto"],
                    [3,"Listar Empleados a Proyectos"],
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
                tabla.add_row([proyecto.get_nombre(),proyecto.get_descripcion(),proyecto.get_fecha_inicio()])

                parametros = (proyecto.get_nombre(),proyecto.get_descripcion(),proyecto.get_fecha_inicio())
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
        
        #Modificar Proyecto
        elif opcion == "2":
            nombre = input("Ingrese el nombre del proyecto: ").strip()
            parametros = (nombre,-1)

            cursor = conexion.cursor()
            verificar = cursor.callproc("sp_proyecto_verificar_nombre",parametros)
            cursor.close()
            if verificar[-1] > 0:
                salir2 = 1
                while salir2 == 1:
                    parametros_id = (verificar[-1],-1)
                    cursor = conexion.cursor()
                    cursor.callproc("sp_proyecto_obtener_id",parametros_id)

                    for result in cursor.stored_results():
                        lista = result.fetchall()
                        for l in lista:
                            datos = l

                    cursor.close()
                    mostrar_menu_modificar_proyecto(datos)
                    opcion = input("Opcion: ").strip()

                    if opcion != "0":
                        data = ModificarProyecto.modificardatosproyecto(opcion,datos)
                        proyecto = Proyecto(data[0],data[1],data[2])
                        parametrosproyecto = (proyecto.get_nombre(),proyecto.get_descripcion(),verificar[-1])
                        cursor = conexion.cursor()
                        cursor.callproc("sp_proyecto_modificar",parametrosproyecto)
                        cursor.close()
                        conexion.commit()
                        print("Datos modificados correctamente")
                        time.sleep(2)
                    else:
                        salir2 = 0

            elif verificar[-1] == -1:
                print("El nombre no coincide con ningun proyecto")
                time.sleep(2)

        # Eliminar proyecto
        elif opcion == "3":
            nombre = input("Ingrese el nombre del proyecto: ").strip()
            parametros = (nombre,-1)

            cursor = conexion.cursor()
            verificar = cursor.callproc("sp_proyectos_eliminar_nombre",parametros)

            for result in cursor.stored_results():
                lista = result.fetchall()
                for l in lista:
                    nombre = l[0]

            if verificar[-1] != -1:
                print(f"El proyecto {nombre} ha sido eliminado")
            else:
                print("El nombre no coincide con ningun proyecto")

            cursor.close()
            conexion.commit()
            time.sleep(2)

        # Listar proyecto
        elif opcion == "4":
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
        elif opcion == "5":

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

        #Menu asignacion empleado
        elif opcion == "6":
            salir3 = 1
            while salir3 == 1:
                mostrar_menu_gestion_empleado()
                opcion = input("Opcion: ").strip()

                #Asignar empleado
                if opcion == "1":
                    run = input("Ingrese el RUN del empleado: ").strip()
                    parametros_empleado = (encriptar(run),-1)
                    cursor = conexion.cursor()
                    verificar_empleado = cursor.callproc("sp_empleado_verificar_run",parametros_empleado)
                    cursor.close()

                    if verificar_empleado[-1] > 0:
                        nombre_pro = input("Ingrese el nombre del proyecto: ").strip()
                        parametros_proyecto = (nombre_pro,-1)
                        cursor = conexion.cursor()
                        verificar_proyecto = cursor.callproc("sp_proyecto_verificar_nombre",parametros_proyecto)
                        cursor.close()
                        if verificar_proyecto[-1] > 0:
                            parametros_asig = (verificar_empleado[-1],verificar_proyecto[-1],-1)
                            cursor = conexion.cursor()
                            verificar_asig = cursor.callproc("sp_proyecto_asignar_empleado",parametros_asig)
                            cursor.close()
                            conexion.commit()

                            if verificar_asig[-1] > 0:
                                print("Empleado asignado correctamente al proyecto")
                                time.sleep(2)
                            else:
                                print("El empleado ya esta asignado al proyecto")
                                time.sleep(2)
                        else:
                            print("El nombre no coincide con ningun proyecto")
                            time.sleep(2)
                    else:
                        print("El RUN no coincide con ningun empleado")
                        time.sleep(2)

                #Eliminar empleado
                if opcion == "2":
                    run = input("Ingrese el RUN del empleado: ").strip()
                    parametros_empleado = (encriptar(run),-1)
                    cursor = conexion.cursor()
                    verificar_empleado = cursor.callproc("sp_empleado_verificar_run",parametros_empleado)
                    cursor.close()

                    if verificar_empleado[-1] > 0:
                        nombre_pro = input("Ingrese el nombre del proyecto: ").strip()
                        parametros_proyecto = (nombre_pro,-1)
                        cursor = conexion.cursor()
                        verificar_proyecto = cursor.callproc("sp_proyecto_verificar_nombre",parametros_proyecto)
                        cursor.close()
                        if verificar_proyecto[-1] > 0:
                            parametros_eli = (verificar_empleado[-1],verificar_proyecto[-1],-1)
                            cursor = conexion.cursor()
                            verificar_eli = cursor.callproc("sp_proyecto_eliminar_empleado",parametros_eli)
                            cursor.close()
                            conexion.commit()

                            if verificar_eli[-1] > 0:
                                print("El empleado ha sido eliminado del proyecto")
                                time.sleep(2)
                            else:
                                print("El empleado no esta asignado al proyecto, no se puede eliminar")
                                time.sleep(2)
                        else:
                            print("El nombre no coincide con ningun proyecto")
                            time.sleep(2)
                    else:
                        print("El RUN no coincide con ningun empleado")
                        time.sleep(2)

                elif opcion == "3":
                    lista_empro = prettytable.PrettyTable()

                    lista_empro.field_names = ["ID Empleado","Empleado","ID Proyecto","Proyecto"]

                    cursor = conexion.cursor()
                    cursor.callproc("sp_proyecto_listar_empleados")

                    for result in cursor.stored_results():
                        lista = result.fetchall()
                        for l in lista:
                            if l[1] == None:
                                lista_empro.add_row([l[0],l[1],l[2],l[3]])
                            else:
                                lista_empro.add_row([l[0],desencriptar(l[1]),l[2],l[3]])
                    cursor.close()

                    if len(lista_empro._rows) > 0:
                        screen.clear()
                        print(lista_empro)
                        input("Presiona [ENTER] para salir")
                    else:
                        print("\nNo hay empleados asignados a proyectos")
                        time.sleep(2)

                elif opcion == "0":
                    salir3 = 0


        elif opcion == "0":
            salir = 0
    