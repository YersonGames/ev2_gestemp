import datetime

if datetime.datetime.strptime("2025-08-30","%Y-%m-%d") > datetime.datetime.strptime("2025-08-29","%Y-%m-%d"):
    print("a")