import prettytable
import mysql.connector
import time

# Clases
from clases.departamento import Departamento

# Servicio
import servicios.CrearDepartamento as CrearDepartamento
import servicios.LimpiarPantalla as screen
import servicios.ModificarDepartamento as ModificarDepartamento

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


def mostrar_menu_modificar_departamento(datos):
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

def menu_gestion_departamento(connect):
    conexion = connect
    salir = 1
    while salir == 1:
        mostrar_menu_gestion_departamento()
        opcion = input("Opcion: ").strip()

        #Crear departamento
        if opcion == "1":
            try:
                tabla = prettytable.PrettyTable()
                tabla.field_names = ["Nombre","Descripcion"]

                datos = CrearDepartamento.registrardatosdepartamento()

                departamento = Departamento(datos[0],datos[1])
                tabla.add_row([departamento.get_nombre(),departamento.get_descripcion()])

                parametros = (departamento.get_nombre(),departamento.get_descripcion())
                cursor = conexion.cursor()
                cursor.callproc("sp_departamento_crear",parametros)
                cursor.close()
                conexion.commit()
                print(tabla)
                print("Departamento creado correctamente!")
                time.sleep(2)
            except mysql.connector.errors.Error as error:
                print("Error: ",error)
                time.sleep(2)

# ---

        # Modificar departamento
        elif opcion == "2":
            nombre = input("Ingrese el nombre del departamento: ").strip()
            parametros = (nombre,-1)
            cursor = conexion.cursor()

            verificar = cursor.callproc("sp_departamento_verificar_nombre",parametros)
            cursor.close()
            if verificar[-1] != -1:
                salir2 = 1
                while salir2 == 1:
                    parametros_id = (verificar[-1],)
                    cursor = conexion.cursor()
                    cursor.callproc("sp_departamento_obtener_id",parametros_id)

                    for result in cursor.stored_results():
                        lista = result.fetchall()
                        for l in lista:
                            datos = l

                    cursor.close()
                    mostrar_menu_modificar_departamento(datos)
                    opcion = input("Opcion: ").strip()

                    if opcion != "0":
                        data = ModificarDepartamento.modificardatosdepartamento(opcion,datos)
                        departamento = Departamento(data[0],data[1])
                        parametrosdepartamento = (departamento.get_nombre(),departamento.get_descripcion(),verificar[-1])
                        cursor = conexion.cursor()
                        cursor.callproc("sp_departamento_modificar",parametrosdepartamento)
                        cursor.close()
                        conexion.commit()
                        print("Datos modificados correctamente")
                        time.sleep(2)
                    else:
                        salir2 = 0
            else:
                print("El nombre no coincide con ningun departamento")
                conexion.commit()
                time.sleep(2)
        
        # Eliminar departamento
        elif opcion == "3":
            nombre = input("Ingrese el nombre del departamento: ").strip()
            parametros = (nombre,-1)

            cursor = conexion.cursor()
            verificar = cursor.callproc("sp_departamento_eliminar_nombre",parametros)

            for result in cursor.stored_results():
                lista = result.fetchall()
                for l in lista:
                    nombre = l[0]

            if verificar[-1] != -1:
                print(f"El departamento {nombre} ha sido eliminado")
            else:
                print("El nombre no coincide con ningun departamento")

            time.sleep(2)

        # Listar departamentos
        elif opcion == "4":
            tabla = prettytable.PrettyTable()
            tabla.field_names = ["ID","Nombre","Descripcion","ID Gerente"]

            cursor = conexion.cursor()
            cursor.callproc("sp_departamento_listar")

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
                print("\nNo hay departamentos registrados")
                time.sleep(2)
        
        #Buscar departamento por nombre
        elif opcion == "5":

            tabla = prettytable.PrettyTable()
            tabla.field_names = ["ID","Nombre","Descripcion","ID Gerente"]

            nombre = input("Ingrese el nombre: ").strip()
            parametros = (nombre,-1)

            cursor = conexion.cursor()
            verificar = cursor.callproc("sp_departamento_buscar",parametros)
            if verificar[-1] != -1:
                for result in cursor.stored_results():
                    lista = result.fetchall()
                    for l in lista:
                        tabla.add_row([l[0],l[1],l[2],l[3]])
                screen.clear()
                print(tabla)
                input("\nPresione [ENTER] para volver")
            else:
                print("\nDepartamento no encontrado")
                time.sleep(2)
                
            cursor.close()
            conexion.commit()
        elif opcion == "0":
            salir = 0