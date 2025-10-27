import datetime

hora1 = "20:00"
hora2 = "21:00"

verificar = hora1.split(":")
if int(verificar[0]) > 24:
    print("Error hora1")

verificar = hora2.split(":")
if int(verificar[0]) > 24:
    print("Error hora2")

date = datetime.datetime.strptime(hora2,"%H:%M")
date2 = datetime.datetime.strptime(hora1,"%H:%M")

if date > date2:
    date3 = date-date2
    date4 = date3.total_seconds()
    date5 = datetime.timedelta(seconds=86400)
    print(date5)
else:
    print("Error")