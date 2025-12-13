import prettytable
import mysql.connector
import time

#Clases
from clases.empleado import Empleado
from clases.usuario import Usuario

#Servicios
import servicios.RegistroEmpleado as RegistroEmpleado
import servicios.LimpiarPantalla as screen
import servicios.ModificarEmpleado as ModificarEmpleado
from servicios.EncriptarDesencriptar import encriptar,desencriptar

def mostrar_menu_gestion():
    screen.clear()
    print("")
    menu = prettytable.PrettyTable()
    menu.field_names = ["","Opciones"]
    menu.add_rows([
                    [1,"Registrar Empleado"],
                    [2,"Modificar Empleado"],
                    [3,"Eliminar Empleado"],
                    [4,"Listar Emplaados"],
                    [5,"Buscar Empleado"],
                    [0,"Volver"]
                  ])
    print(menu)

def mostrar_menu_modificar(datos):
    screen.clear()
    print("")
    menu = prettytable.PrettyTable()
    menu.field_names = ["","Opciones","Datos"]
    menu.add_rows([
                    [1,"Modificar Nombre",desencriptar(datos[0])],
                    [2,"Modificar Direccion",desencriptar(datos[1])],
                    [3,"Modificar Telefono",desencriptar(datos[2])],
                    [4,"Modificar Email",desencriptar(datos[3])],
                    [5,"Modificar Salario",datos[7]],
                    [6,"Modificar Contraseña",""],
                    [7,"Modificar RUN",desencriptar(datos[4])],
                    [0,"Volver",""]
                  ])
    print(menu)

def menu_gestion_empleado(connect):
    conexion = connect
    salir = 1
    while salir == 1:
        mostrar_menu_gestion()
        opcion = input("Opcion: ").strip()

        #Registrar empleado
        if opcion == "1":
            try:
                tabla = prettytable.PrettyTable()
                tabla.field_names = ["Nombre","Direccion","Telefono","Email","RUN","Permiso","Fecha de Inicio","Salario"]

                datos = RegistroEmpleado.registrardatos()

                empleado = Empleado(datos[0],datos[1],datos[2],datos[3],datos[4],datos[5],datos[6],datos[7],datos[8])
                tabla.add_row([empleado.get_nombre(),empleado.get_direccion(),empleado.get_telefono(),empleado.get_email(),empleado.get_run(),empleado.get_permiso(),empleado.get_fecha_inicio(),empleado.get_salario()])

                parametros = (encriptar(empleado.get_nombre()),encriptar(empleado.get_direccion()),encriptar(empleado.get_telefono()),encriptar(empleado.get_email()),encriptar(empleado.get_run()),empleado.get_contrasenahash(),empleado.get_permiso(),empleado.get_fecha_inicio(),empleado.get_salario(),datos[9],datos[10])
                cursor = conexion.cursor()
                cursor.callproc("sp_empleado_registrar",parametros)
                cursor.close()
                conexion.commit()
                print(tabla)
                print("Empleado registrado correctamente!")
                time.sleep(2)
            except mysql.connector.errors.Error as error:
                print("Error: ",error)
                time.sleep(2)

        #Modificar empleado
        elif opcion == "2":
            run = input("Ingrese el RUN del empleado: ").strip()
            parametros = (encriptar(run),-1)
            cursor = conexion.cursor()

            verificar = cursor.callproc("sp_empleado_verificar_run",parametros)
            cursor.close()
            if verificar[-1] != -1:
                salir2 = 1
                while salir2 == 1:
                    parametros_id = (verificar[-1],-1)
                    cursor = conexion.cursor()
                    cursor.callproc("sp_empleado_get_id",parametros_id)

                    for result in cursor.stored_results():
                        lista = result.fetchall()
                        for l in lista:
                            datos = l

                    cursor.close()
                    mostrar_menu_modificar(datos)
                    opcion = input("Opcion: ").strip()
                    if opcion != "0":
                        data = ModificarEmpleado.modificardatos(opcion,datos)
                        empleado = Empleado(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8])
                        parametrosempleado = (encriptar(empleado.get_nombre()),encriptar(empleado.get_direccion()),encriptar(empleado.get_telefono()),encriptar(empleado.get_email()),encriptar(empleado.get_run()),empleado.get_contrasenahash(),empleado.get_permiso(),empleado.get_fecha_inicio(),empleado.get_salario(),verificar[-1],data[9],data[10])
                        cursor = conexion.cursor()
                        cursor.callproc("sp_empleado_modificar_id",parametrosempleado)
                        cursor.close()
                        conexion.commit()
                        print("Datos modificados correctamente")
                        time.sleep(2)
                    else:
                        salir2 = 0
                    
            else:
                print("El RUN no coincide con ningun empleado")
                conexion.commit()
                time.sleep(2)
        
        #Eliminar empleado
        elif opcion == "3":
            run = input("Ingrese el RUN del empleado: ").strip()
            parametros = (encriptar(run),-1)

            cursor = conexion.cursor()
            verificar = cursor.callproc("sp_empleado_eliminar_run",parametros)

            for result in cursor.stored_results():
                lista = result.fetchall()
                for l in lista:
                    nombre = desencriptar(l[0])

            if verificar[-1] != -1:
                print(f"El empleado {nombre} ha sido eliminado")
            else:
                print("El RUN no coincide con ningun empleado")

            time.sleep(2)



        #Listar empleados
        elif opcion == "4":
            tabla = prettytable.PrettyTable()
            tabla.field_names = ["ID","Nombre","Direccion","Telefono","Email","RUN","Permiso","Fecha de Inicio","Salario"]

            cursor = conexion.cursor()
            cursor.callproc("sp_empleado_listar")

            for result in cursor.stored_results():
                lista = result.fetchall()
                for l in lista:
                    tabla.add_row([l[0],desencriptar(l[1]),desencriptar(l[2]),desencriptar(l[3]),desencriptar(l[4]),desencriptar(l[5]),l[6],l[7],l[8]])

            cursor.close()
            conexion.commit()
            screen.clear()
            if len(tabla._rows) > 0:
                screen.clear()
                print(tabla)
                input("\nPresione [ENTER] para volver")
            else:
                print("\nNo hay empleados registrados")
                time.sleep(2)
        
        #Buscar empleado por nombre
        elif opcion == "5":

            tabla = prettytable.PrettyTable()
            tabla.field_names = ["ID","Nombre","Direccion","Telefono","Email","RUN","Permiso","Fecha de Inicio","Salario"]

            nombre = input("Ingrese el nombre: ").strip()
            parametros = (encriptar(nombre),-1)

            cursor = conexion.cursor()
            verificar = cursor.callproc("sp_empleado_buscar",parametros)
            if verificar[-1] != -1:
                for result in cursor.stored_results():
                    lista = result.fetchall()
                    for l in lista:
                        tabla.add_row([l[0],desencriptar(l[1]),desencriptar(l[2]),desencriptar(l[3]),desencriptar(l[4]),desencriptar(l[5]),l[6],l[7],l[8]])
                screen.clear()
                print(tabla)
                input("\nPresione [ENTER] para volver")
            else:
                print("\nEmpleado no encontrado")
                time.sleep(2)
                

            cursor.close()
            conexion.commit()
        elif opcion == "0":
            salir = 0