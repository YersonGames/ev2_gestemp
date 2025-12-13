from prompt_toolkit import prompt
import re
import datetime
# Servicio 
import servicios.LimpiarPantalla as screen

def registrardatospaquete(opcion,datos):
    nombre = datos[0]
    fechai = datetime.datetime.strftime(datos[1],"%Y-%m-%d")
    fechaf = datetime.datetime.strftime(datos[2],"%Y-%m-%d")
    disponibilidad = datos[3]
    step = opcion

    while step == "1":
        nombre = input("Nombre del Paquete: ").title()

        if not nombre:
            print("Error: El Campo esta vacio")
        else:
            step = 0

    while step == "2":
        fechai = input("Formato: (AAAA-MM-DD)\nIngrese la fecha de Inicio: ")
        patron = re.compile(r"^\d\d\d\d-\d\d-\d\d$", re.IGNORECASE)
        patron2 = patron.match(fechai)
        if not fechai:
            print("Error: El campo esta vacio")
        elif not patron2:
            print("Error: Fecha incorrecta")
        else:
            try:
                if datetime.datetime.strptime(fechai,"%Y-%m-%d") < datetime.datetime.strptime(fechaf,"%Y-%m-%d"):
                    step = 0
                else:
                    print("Error: Fecha incorrecta")
                    step = "2"
            except ValueError:
                print("Error: Fecha incorrecta")
                step = "2"

    while step == "3":
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
                    step = 0
                else:
                    print("Error: Fecha incorrecta")
                    step = "3"
            except ValueError:
                print("Error: Fecha incorrecta")
                step = "3"
    
    while step == "4":
        dispstr = input("Disponibilidad: ")
        try:
            disponibilidad = int(dispstr)
            step = 0
        except ValueError:
            print("Error: Valor Incorrecto")
    
    datos = [nombre,fechai,fechaf,disponibilidad]
    return datos