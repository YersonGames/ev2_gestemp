import re
import hashlib
import datetime
import os


def registrardatos():
    step = 1

    while step == 1:
        nombre = input("Nombre completo: ").strip()
        if not nombre:
            print("Error: El campo esta vacio")
        else:
            step = 2

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

    while step == 4:
        telefono = input("Numero de telefono: ").strip()
        if not telefono:
            print("Error: El campo esta vacio")
        else:
            step = 5
    
    while step == 5:
        direccion = input("Direccion: ").strip()

        if not direccion:
            print("Error: El campo esta vacio")
        else:
            step = 6
    
    while step == 6:
        try:
            salario = float(input("Salario: ").strip())
            if not salario:
                print("Error: El campo esta vacio")
            else:
                step = 7
        except ValueError:
            print("Error: Salario incorrecte, ingrese un numero")
    
    while step == 7:
        contrasena = input("Contraseña: ").strip()
        if not contrasena:
            print("Error: El campo esta vacio")
        else:
            data = contrasena.encode("utf-8")
            contrasenahash = hashlib.sha256()
            contrasenahash.update(data)
            step = 0

    fecha = datetime.datetime.now()
    fechahoy = f"{fecha.year}-{fecha.month}-{fecha.day}"

    datos = [nombre,direccion,telefono,email,run,contrasenahash.hexdigest(),1,fechahoy,salario]
    os.system("clear||cls")
    return datos