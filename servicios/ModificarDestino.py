from prompt_toolkit import prompt

# Servicio 
import servicios.LimpiarPantalla as screen

def modificardatosdestino(opcion,datos):

    nombre = datos[0]
    descripcion = datos[1]
    actividades = datos[2]
    costo = datos[3]

    step = opcion
    while step == "1":
        nombre = input("Nombre del Destino: ").title()

        if not nombre:
            print("Error: El Campo esta vacio")
        else:
            step = 0

    while step == "2":
        print("Presiona [ESC]+[ENTER] para enviar.\nDescripcion:")
        descripcion = prompt(">> ", multiline=True).strip()
        
        if not descripcion:
            print("Error: El campo esta vacio")
        else:
            step = 0

    while step == "3":
        print("Presiona [ESC]+[ENTER] para enviar.\nActividades:")
        actividades = prompt(">> ", multiline=True).strip()
        
        if not actividades:
            print("Error: El campo esta vacio")
        else:
            step = 0
    
    while step == "4":
        costostr = input("Costo: ")
        try:
            costo = float(costostr)
            step = 0
        except ValueError:
            print("Error: Valor Incorrecto")

    datos = [nombre,descripcion,actividades,costo]
    return datos