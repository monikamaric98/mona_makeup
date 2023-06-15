from . import Base
from sqlalchemy import *



class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True)
    invoice_time = Column(Time)
    invoice_date = Column(Date)
    service_id= Column(Integer, ForeignKey("services.id"))
    customer_id = Column(Integer,ForeignKey("customers.id"))
    employee_id = Column(Integer,ForeignKey("employees.id"))


    
