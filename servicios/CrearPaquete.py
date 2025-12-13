from prompt_toolkit import prompt
import re
import datetime
# Servicio 
import servicios.LimpiarPantalla as screen

def registrardatosdestino():
    salir = 0
    step = 1
    while salir == 0:
        while step == 1:
            nombre = input("Nombre del Paquete: ").title()

            if not nombre:
                print("Error: El Campo esta vacio")
            else:
                step = 2

        while step == 2:
            fechai = input("Formato: (AAAA-MM-DD)\nIngrese la fecha de Inicio: ")
            patron = re.compile(r"^\d\d\d\d-\d\d-\d\d$", re.IGNORECASE)
            patron2 = patron.match(fechai)
            if not fechai:
                print("Error: El campo esta vacio")
            elif not patron2:
                print("Error: Fecha incorrecta")
            else:
                step = 3

        while step == 3:
            fechaf = input("Formato: (AAAA-MM-DD)\nIngrese la fecha de Fin: ")
            patron = re.compile(r"^\d\d\d\d-\d\d-\d\d$", re.IGNORECASE)
            patron2 = patron.match(fechaf)
            if not fechaf:
                print("Error: El campo esta vacio")
            elif not patron2:
                print("Error: Fecha incorrecta")
            else:
                try:
                    if datetime.datetime.strptime(fechai,"%Y-%m-%d") < datetime.datetime.strptime(fechaf,"%Y-%m-%d"):
                        step = 4
                    else:
                        print("Error: Fechas incorrectas")
                        step = 2
                except ValueError:
                    print("Error: Fechas incorrectas")
                    step = 2
        
        while step == 4:
            dispstr = input("Disponibilidad: ")
            try:
                disponibilidad = int(dispstr)
                step = 0
                salir = 1
                datos = [nombre,fechai,fechaf,disponibilidad]
                return datos
            except ValueError:
                print("Error: Valor Incorrecto")