#Librerias
import re
import datetime
import time

def registrar_horas(connect,id_usuario):
    conexion = connect
    step = 1
    salir = 1
    while salir == 1:
        #Registrar hora inicio
        while step == 1:
            hora1 = input("Formato (XX:XX) 24hrs\nIngresar Hora Inicio: ")
            patron = re.compile(r"^\d\d:\d\d$", re.IGNORECASE)
            patron2 = patron.match(hora1)
            verificar = hora1.split(":")
            
            if not hora1:
                print("El campo esta vacio")
            elif not patron2:
                print("Formato incorrecto: (XX:XX) 24hrs")
            elif int(verificar[0]) > 24 or int(verificar[1]) > 60:
                print("Hora incorrecta")
            else:
                step = 2

        #Registrar hora fin
        while step == 2:
            hora2 = input("Formato (XX:XX) 24hrs\nIngresar Hora Fin: ")
            patron = re.compile(r"^\d\d:\d\d$", re.IGNORECASE)
            patron2 = patron.match(hora1)
            verificar = hora2.split(":")
            
            if not hora2:
                print("El campo esta vacio")
            elif not patron2:
                print("Formato incorrecto: (XX:XX) 24hrs")
            elif int(verificar[0]) > 24 or int(verificar[1]) > 60:
                print("Hora incorrecta")
            else:
                step = 3
            
        while step == 3:
            dato1 = datetime.datetime.strptime(hora1,"%H:%M")
            dato2 = datetime.datetime.strptime(hora2,"%H:%M")

            if dato2 > dato1:
                data = (dato2-dato1).total_seconds()
                print(f"Horas trabajas: {datetime.timedelta(seconds=data)}")
                parametros = (id_usuario,data,-1)
                cursor = conexion.cursor()
                verificar = cursor.callproc("sp_empleado_registrar_horas",parametros)
                cursor.close()
                conexion.commit()
                time.sleep(2)
                step = 0
                salir = 0

            else:
                print("Horas invalidas")
                step = 1