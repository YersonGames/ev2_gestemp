import re
import hashlib
import datetime
from getpass import getpass

#Servicio
import servicios.LimpiarPantalla as screen

def registrardatos():
    step = 1

    #Ingresar nombre
    while step == 1:
        nombre = input("Nombre completo: ").strip()
        if not nombre:
            print("Error: El campo esta vacio")
        else:
            step = 2

    #Ingresar RUN
    while step == 2:
        run = input("\nFormato: (11.111.111-1)\nSi es K reemplace por 0\nRUN: ").strip()
        patron = re.compile(r"^\d\d\.\d\d\d\.\d\d\d-\d$", re.IGNORECASE)
        patron2 = patron.match(run)
        if not run:
            print("Error: El campo esta vacio")
        elif not patron2:
            print("Error: Formato incorrecto (11.111.111-1)")
        else:
            step = 3
    
    #Ingresar Email
    while step == 3:
        email = input("Email: ").strip()
        patron = re.compile(r"^[-A-Za-z0-9!#$%&'*+/=?^_`{|}~]+(?:\.[-A-Za-z0-9!#$%&'*+/=?^_`{|}~]+)*@(?:[A-Za-z0-9](?:[-A-Za-z0-9]*[A-Za-z0-9])?\.)+[A-Za-z0-9](?:[-A-Za-z0-9]*[A-Za-z0-9])?$", re.IGNORECASE)
        patron2 = patron.match(email)
        if not email:
            print("Error: El campo esta vacio")
        elif not patron2:
            print("Error: Email invalido")
        else:
            step = 4

    #Ingresar Telefono
    while step == 4:
        telefono = input("Numero de telefono: ").strip()
        if not telefono:
            print("Error: El campo esta vacio")
        else:
            step = 5
    
    #Ingresar Direccion
    while step == 5:
        direccion = input("Direccion: ").strip()

        if not direccion:
            print("Error: El campo esta vacio")
        else:
            step = 6
    
    #Ingresar Salario
    while step == 6:
        try:
            salario = float(input("Salario: ").strip())
            if not salario:
                print("Error: El campo esta vacio")
            else:
                step = 7
        except ValueError:
            print("Error: Salario incorrecto, ingrese un numero")
    
    #Ingresar Contrasena
    while step == 7:
        contrasena = getpass("Contraseña: ").strip()
        if not contrasena:
            print("Error: El campo esta vacio")
        else:
            repeat_pass = getpass("Repita la contraseña")

            if repeat_pass == contrasena:
                data = contrasena.encode("utf-8")
                contrasenahash = hashlib.sha256()
                contrasenahash.update(data)
                step = 0
            else:
                print("Contraseña incorrecta!\n")

    fecha = datetime.datetime.now()
    fechahoy = f"{fecha.year}-{fecha.month}-{fecha.day}"
    screen.clear()
    datos = [nombre,direccion,telefono,email,run,contrasenahash.hexdigest(),1,fechahoy,salario]
    return datos