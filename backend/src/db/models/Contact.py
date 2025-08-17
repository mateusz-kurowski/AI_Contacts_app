from sqlalchemy import Column, DateTime, Integer, String, func
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass

# SQLAlchemy model
class ContactModel(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(128), nullable=False)
    phone = Column(String(32), nullable=False, unique=True)
    createdAt = Column(DateTime, nullable=False, default=func.now())

    def __repr__(self):
        return f"<ContactModel(id={self.id}, name='{self.name}', phone='{self.phone}')>"

    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "createdAt": self.createdAt,
        }