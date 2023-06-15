from sqlalchemy.orm import relationship

from .customers import Customer
from .appointments import Appointment
from .employees import Employee
from .invoices import Invoice
from .services import Service

from . import Base
from . import engine

Appointment.service = relationship("Service", back_populates="appointments")
Appointment.employee = relationship("Employee", back_populates="appointments")
Appointment.customer = relationship("Customer", back_populates="appointments")

Invoice.service = relationship("Service", back_populates="invoice")
Invoice.employee = relationship("Employee", back_populates="invoices")
Invoice.customer = relationship("Customer", back_populates="invoices")

Customer.invoices = relationship("Invoice", back_populates="customer")
Customer.appointments = relationship("Appointment", back_populates="customer")

Service.employee = relationship("Employee", back_populates="services")
Service.appointments = relationship("Appointment", back_populates="service")
Service.invoice = relationship("Invoice", back_populates="service")

Employee.appointments = relationship("Appointment", back_populates="employee")
Employee.invoices = relationship("Invoice", back_populates="employee")
Employee.services = relationship("Service", back_populates="employee")



Base.metadata.bind = engine
Base.metadata.create_all(bind=engine)