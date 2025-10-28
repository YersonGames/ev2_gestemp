import re
import hashlib
from prompt_toolkit import prompt

#Servicio
import servicios.LimpiarPantalla as screen

def modificardatosdepartamento(opcion,datos):
    step = opcion

    nombre = datos[0]
    descripcion = datos[1]

    #Ingresar nombre
    while step == "1":
        nombre = input("Nombre del Departamento: ").strip()
        if not nombre:
            print("Error: El campo esta vacio")
        else:
            step = 0
    
    #Ingresar Descripcion
    while step == "2":
        print("Presiona [ESC]+[ENTER] para enviar.\nDescripcion:")
        descripcion = prompt(">> ", multiline=True).strip()

        if not descripcion:
            print("Error: El campo esta vacio")
        else:
            step = 0

    data = [nombre,descripcion]
    return data