from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, Boolean, Date, Enum

Base = declarative_base()


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True, unique=True)
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
    reset_token = Column(Text, nullable=True)

    # candidate = relationship("Candidate", back_populates="user")
    user_role = relationship("UserRole", back_populates="users")
    applicant = relationship("Applicant", back_populates="user")


class Applicant(Base):
    __tablename__ = "applicants"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    first_name = Column(String(255), nullable=False)
    other_names = Column(String(255),index=True, nullable=False)
    phone_number = Column(String(255), nullable=False)
    address = Column(Text, nullable=True)

    user = relationship("User", back_populates="applicant")
    qualifications = relationship("Qualification", back_populates="applicant")
    skills = relationship("Skill", back_populates="applicant")


class Qualification(Base):
    __tablename__ = "qualifications"
    id = Column(Integer, primary_key=True, index=True)
    applicant_id = Column(Integer, ForeignKey("applicants.id"))
    qualification_type = Column(String(255), nullable=False)
    qualification_name = Column(String(255), nullable=False)
    institution = Column(String(255), nullable=False)
    completion_date = Column(Date, nullable=False)

    applicant = relationship("Applicant", back_populates="qualifications")


class Skill(Base):
    __tablename__ = "skills"
    id = Column(Integer, primary_key=True, index=True)
    applicant_id = Column(Integer, ForeignKey("applicants.id"))
    skill_name = Column(String(255), nullable=False)
    experience_years = Column(Integer, nullable=False)
    proficiency_level = Column(Enum('Beginner', 'Intermediate', 'Advanced', name='proficiency_level_enum'), nullable=False)

    applicant = relationship("Applicant", back_populates="skills")


class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True, unique=True)
    description = Column(Text, nullable=True)
    qualification = Column(String(255), nullable=True)
    skills = Column(String(255), nullable=True)
    salary = Column(Float, default=0.00)
    validity = Column(Date)
    is_active = Column(Boolean, default=True, nullable=False)


class Applicant(Base):
    __tablename__ = "applicants"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    first_name = Column(String(255), nullable=False)
    other_names = Column(String(255),index=True, nullable=False)
    phone_number = Column(String(255), nullable=False)
    address = Column(Text, nullable=True)

    user = relationship("User", back_populates="applicants")
    qualifications = relationship("Qualification", back_populates="applicants")
    skills = relationship("Skill", back_populates="applicants")


class Qualification(Base):
    __tablename__ = "qualifications"
    id = Column(Integer, primary_key=True, index=True)
    applicant_id = Column(Integer, ForeignKey("applicants.id"))
    qualification_type = Column(String(255), nullable=False)
    qualification_name = Column(String(255), nullable=False)
    institution = Column(String(255), nullable=False)
    completion_date = Column(Date, nullable=False)


class Skill(Base):
    __tablename__ = "skills"
    id = Column(Integer, primary_key=True, index=True)
    applicant_id = Column(Integer, ForeignKey("applicants.id"))
    skill_name = Column(String(255), nullable=False)
    experience_years = Column(Integer, nullable=False)
    proficiency_level = Column(Enum('Beginner', 'Intermediate', 'Advanced', name='proficiency_level_enum'), nullable=False)


class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True, unique=True)
    description = Column(Text, nullable=True)
    qualification = Column(String(255), nullable=True)
    skills = Column(String(255), nullable=True)
    salary = Column(Float, default=0.00)
    validity = Column(Date)
    is_active = Column(Boolean, default=True, nullable=False)
