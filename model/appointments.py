from . import Base
from sqlalchemy import *



class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True)
    appointment_date = Column(Date)
    appointment_time = Column(Time)
    service_id = Column(Integer, ForeignKey("services.id"))
    employee_id = Column(Integer, ForeignKey("employees.id"))
    customer_id = Column(Integer, ForeignKey("customers.id"))
    
