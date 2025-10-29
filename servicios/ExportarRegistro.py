#Librerias
import xlsxwriter
import datetime
import time
import datetime

#Servicios
from servicios.EncriptarDesencriptar import encriptar,desencriptar

def exportar_registro(connect):
    conexion = connect
    #Crear
    file = xlsxwriter.Workbook('Registro.xlsx')
    hoja = file.add_worksheet()

    #filas
    hoja.write(0,0,"Empleados")
    hoja.write(0,1,"Registro Tiempo Empleado")
    hoja.write(0,4,"Departamentos")
    hoja.write(0,7,"Proyectos")

    #Empleados/Horas
    cursor = conexion.cursor()
    cursor.callproc("sp_empleado_listar_registro")
    columna = 1
    for result in cursor.stored_results():
        lista = result.fetchall()
        for l in lista:
            if l[1] != None:
                hoja.write(columna,0,desencriptar(l[1]))
            if l[2] != None:
                hoja.write(columna,1,str(datetime.timedelta(seconds=l[2])))
            if l[3] != None:
                date = datetime.datetime.strftime(l[3],"%Y-%m")
                hoja.write(columna,2,date)
            columna += 1
    hoja.add_table(0,0,columna,2,{'columns': [{'header': 'Empleados'},{'header': 'Horas Trabajadas Empleados'},{'header': 'Fecha'}]})

    #Departamentos
    cursor = conexion.cursor()
    cursor.callproc("sp_departamento_listar")
    columna = 1
    for result in cursor.stored_results():
        lista = result.fetchall()
        for l in lista:
            hoja.write(columna,4,l[1])
            hoja.write(columna,5,l[2])
            columna += 1
    cursor.close()
    hoja.add_table(0,4,columna,5,{'columns': [{'header': 'Departamentos'},{'header': 'Descripcion Dep'}]})
    #Proyectos
    cursor = conexion.cursor()
    cursor.callproc("sp_proyectos_listar")
    columna = 1
    for result in cursor.stored_results():
        lista = result.fetchall()
        for l in lista:
            hoja.write(columna,7,l[1])
            hoja.write(columna,8,l[2])
            columna += 1
    cursor.close()
    hoja.add_table(0,7,columna,8,{'columns': [{'header': 'Proyectos'},{'header': 'Descripcion Pro'}]})

    hoja.autofit()
    file.close()

    print("El registro 'Registro.xlsx' exportado correctamente!")
    time.sleep(2)