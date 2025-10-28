import datetime

date = datetime.date(1899, 12, 30)
date2 = date + datetime.timedelta(days=45991)
print(date2)