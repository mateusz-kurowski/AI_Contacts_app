from sqlalchemy import Column, String, Integer
from .db import Base


# SQLAlchemy model
class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(128), nullable=False)
    phone = Column(String(32), nullable=False, unique=True)
