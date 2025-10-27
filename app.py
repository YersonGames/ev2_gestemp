import prettytable
import mysql.connector
import hashlib
from getpass import getpass

#Clases
from clases.empleado import Empleado
from clases.usuario import Usuario

#Servicios
import MenuGestionEmpleado
import MenuGestionDepartamento
import MenuGestionProyecto
import servicios.LimpiarPantalla as screen
from servicios.EncriptarDesencriptar import encriptar,desencriptar
import servicios.RegistrarHora as RegistrarHora

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

def mostrar_menu(nombre,permiso):
    screen.clear()
    print(f"Sesion: {desencriptar(nombre)}")
    if permiso == 3:
        cargo = "Administrador"
    elif permiso == 2:
        cargo = "Gerente"
    elif permiso == 1:
        cargo = "Empleado"
    print(f"Cargo: {cargo}")
    menu = prettytable.PrettyTable()
    menu.field_names = ["","Opciones"]
    if permiso == 3:
        menu.add_rows([
                        [1,"Gestionar Empleados"],
                        [2,"Gestionar Departamentos"],
                        [3,"Gestionar Proyectos"],
                        [0,"Salir"]
                    ])
    elif permiso == 1 or permiso == 2:
        menu.add_rows([
                    [1,"Ingresar Horas"],
                    [0,"Salir"]
                  ])
    print(menu)

def main():
    conexion = conexionsql()

    salir = 1
    login = 1
    program = 1

    while program == 1:
        while login == 1:
            screen.clear()
            print("Iniciar Sesion")
            print("\nEscriba 'salir' para salir del programa")
            step = 1
            while step == 1:
                run = input("RUN: ").strip()
                if not run and run.lower() != "salir":
                    print("El campo esta vacio")
                elif run.lower() == "salir":
                    step = 0
                    login = 0
                    salir = 0
                    program = 0
                else:
                    step = 2
            
            while step == 2:
                contrasena = getpass("Contraseña: ").strip()
                if not contrasena and contrasena.lower() != "salir":
                    print("El campo esta vacio")
                elif contrasena.lower() == "salir":
                    step = 0
                    login = 0
                    salir = 0
                    program = 0
                else:
                    step = 3
            
            while step == 3:
                data = contrasena.encode("utf-8")
                contrasenahash = hashlib.sha256()
                contrasenahash.update(data)

                parametros = (encriptar(run),contrasenahash.hexdigest(),-1,-1,"Nombre")

                cursor = conexion.cursor()
                verificar_login = cursor.callproc("sp_usuario_login",parametros)
                cursor.close()
                if verificar_login[2] > 0 and verificar_login[3] > 0:
                    input(f"Haz iniciado sesion como {desencriptar(verificar_login[4])}, \nPresione [ENTER] para continuar")
                    permiso = verificar_login[3]
                    nombre_usuario = verificar_login[4]
                    login = 0
                    step = 0
                    salir = 1
                else:
                    input("Error al iniciar sesion, presione [ENTER] para reintentar")
                    step = 0

        while salir == 1:
            if permiso == 3:
                mostrar_menu(nombre_usuario,permiso)
                opcion = input("Opcion: ").strip()

                #Gestionar empleados
                if opcion == "1":
                    MenuGestionEmpleado.menu_gestion_empleado(conexion)
                elif opcion == "2":
                    MenuGestionDepartamento.menu_gestion_departamento(conexion)
                elif opcion == "3":
                    MenuGestionProyecto.menu_gestion_proyecto(conexion)
                elif opcion == "0":
                    salir = 0
                    login = 1
            elif permiso == 1 or permiso == 2:
                mostrar_menu(nombre_usuario,permiso)
                opcion = input("Opcion: ").strip()
                if opcion == "1":
                    RegistrarHora.registrar_horas(conexion,verificar_login[2])
                elif opcion == "0":
                    salir = 0
                    login = 1


    
main()