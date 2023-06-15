from . import Base
from sqlalchemy import *



class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(25))
    last_name = Column(String(25))
    email = Column(String(100))
    phone_number = Column(Integer)

   
    
