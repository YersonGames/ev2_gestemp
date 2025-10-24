import re
import hashlib
import datetime

# Servicio 
import servicios.LimpiarPantalla as screen

def registrardatosproyectos():
    step = 1

    # Ingresar nombre
    while step == 1:
        nombre = input("Nombre del proyecto: ").strip()
        if not nombre:
            print("Error: El Campo esta vacio")
        else:
            step = 2

    # Ingresar descripción
    while step == 2:
        descripcion = input("Descripción del proyecto: ").strip()
        if not descripcion:
            print("Error: El campo esta vacio")
        else:
            step = 0


    fecha = datetime.datetime.now()
    fecha_inicio = f"{fecha.year}-{fecha.month}-{fecha.day}"
    screen.clear()
    datos = [nombre,descripcion,fecha_inicio]
    return datos
