from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, Boolean

Base = declarative_base()


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    description = Column(Text, nullable=True)
    price = Column(Float, default=0.00)
    tax = Column(Float, default=0.00)
    tags = Column(Text, nullable=True)
    image = Column(String(255), nullable=True)


class UserRole(Base):
    __tablename__ = "user_roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)

    users = relationship("User", back_populates="user_role")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    user_role_id = Column(Integer, ForeignKey("user_roles.id"))
    is_active = Column(Boolean, default=True, nullable=False)

    # candidate = relationship("Candidate", back_populates="user")
    user_role = relationship("UserRole", back_populates="users")
