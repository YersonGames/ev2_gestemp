import re
import hashlib

#Servicio
import servicios.LimpiarPantalla as screen
from servicios.EncriptarDesencriptar import encriptar,desencriptar

def modificardatos(opcion,datos):
    step = opcion

    nombre = desencriptar(datos[0])
    direccion = desencriptar(datos[1])
    telefono = desencriptar(datos[2])
    email = desencriptar(datos[3])
    run = desencriptar(datos[4])
    contrasenahash2 = datos[8]
    permiso = datos[5]
    fechahoy = datos[6]
    salario = datos[7]

    #Ingresar nombre
    while step == "1":
        nombre = input("Nombre completo: ").strip()
        if not nombre:
            print("Error: El campo esta vacio")
        else:
            step = 0

    #Ingresar Direccion
    while step == "2":
        direccion = input("Direccion: ").strip()

        if not direccion:
            print("Error: El campo esta vacio")
        else:
            step = 0

    #Ingresar Telefono
    while step == "3":
        telefono = input("Numero de telefono: ").strip()
        if not telefono:
            print("Error: El campo esta vacio")
        else:
            step = 0
    
    #Ingresar Email
    while step == "4":
        email = input("Email: ").strip()
        patron = re.compile(r"^[-A-Za-z0-9!#$%&'*+/=?^_`{|}~]+(?:\.[-A-Za-z0-9!#$%&'*+/=?^_`{|}~]+)*@(?:[A-Za-z0-9](?:[-A-Za-z0-9]*[A-Za-z0-9])?\.)+[A-Za-z0-9](?:[-A-Za-z0-9]*[A-Za-z0-9])?$", re.IGNORECASE)
        patron2 = patron.match(email)
        if not email:
            print("Error: El campo esta vacio")
        elif not patron2:
            print("Error: Email invalido")
        else:
            step = 0
    
    #Ingresar Salario
    while step == "5":
        try:
            salario = float(input("Salario: ").strip())
            if not salario:
                print("Error: El campo esta vacio")
            else:
                step = 0
        except ValueError:
            print("Error: Salario incorrecto, ingrese un numero")
    
    #Ingresar Contrasena
    while step == "6":
        contrasena = input("Contraseña: ").strip()
        if not contrasena:
            print("Error: El campo esta vacio")
        else:
            data = contrasena.encode("utf-8")
            contrasenahash = hashlib.sha256()
            contrasenahash.update(data)
            contrasenahash2 = contrasenahash.hexdigest()
            step = 0

    #Ingresar RUN
    while step == "7":
        run = input("\nFormato: (11.111.111-1)\nSi es K reemplace por 0\nRUN: ").strip()
        patron = re.compile(r"^\d\d\.\d\d\d\.\d\d\d-\d$", re.IGNORECASE)
        patron2 = patron.match(run)
        if not run:
            print("Error: El campo esta vacio")
        elif not patron2:
            print("Error: Formato incorrecto (11.111.111-1)")
        else:
            step = 3
            
    data = [nombre,direccion,telefono,email,run,contrasenahash2,permiso,fechahoy,salario]
    return data