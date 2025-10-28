import re
import hashlib
import datetime
from prompt_toolkit import prompt

#Servicio
import servicios.LimpiarPantalla as screen

def registrardatosdepartamento():
    step = 1

    #Ingresar nombre
    while step == 1:
        nombre = input("Nombre completo: ").strip()
        if not nombre:
            print("Error: El campo esta vacio")
        else:
            step = 2

    #Ingresar Descripcion
    while step == 2:
        #descripcion = input("Descripción: ").strip()
        print("Presiona [ESC]+[ENTER] para enviar.\nDescripcion:")
        descripcion = prompt(">> ", multiline=True).strip()
        if not descripcion:
            print("Error: El campo esta vacio")
        else:
            step = 0

    screen.clear()
    datos = [nombre,descripcion]
    return datos