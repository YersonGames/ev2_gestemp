import re
import hashlib
import datetime

#Servicio
import servicios.LimpiarPantalla as screen

def modificardatosproyecto(opcion,datos):
    step = opcion

    nombre = datos[0]
    descripcion = datos[1]

    #Ingresar nombre
    while step == "1":
        nombre = input("Nombre del Proyecto: ").strip()
        if not nombre:
            print("Error: El campo esta vacio")
        else:
            step = 0
    
    #Ingresar Descripcion
    while step == "2":
        descripcion = input("Descripcion: ").strip()

        if not descripcion:
            print("Error: El campo esta vacio")
        else:
            step = 0

    fecha = datetime.datetime.now()
    fecha_inicio = f"{fecha.year}-{fecha.month}-{fecha.day}"
    data = [nombre,descripcion,fecha_inicio]
    return data