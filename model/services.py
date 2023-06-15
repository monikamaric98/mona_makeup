from . import Base
from sqlalchemy import *



class Service(Base):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True)
    name = Column(String(25))
    price = Column(Integer())
    description = Column(String(100))
    employee_id = Column(Integer,ForeignKey("employees.id"))


    
