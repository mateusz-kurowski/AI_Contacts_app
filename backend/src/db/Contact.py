from sqlalchemy import Column, DateTime, Integer, String, func

from .db import Base


# SQLAlchemy model
class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(128), nullable=False)
    phone = Column(String(32), nullable=False, unique=True)
    createdAt = Column(DateTime, nullable=False, default=func.now())

    def __repr__(self):
        return f"<Contact(id={self.id}, name='{self.name}', phone='{self.phone}')>"
