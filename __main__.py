from model import *
from model.relations import *
from model.cache import region, api

k = Employee(first_name="Ana", last_name="Anic", email="ana@gmail.com", phone_number="12345")
session.add(k)
session.commit()

ID = 1
KEY = f'employee_{ID}'
k = region.get(KEY)
print(k)
if k is api.NO_VALUE:
    k = session.query(Employee).filter(Employee.id==ID).one()
    region.set(KEY, k)
print(k.first_name + " " + k.last_name)


