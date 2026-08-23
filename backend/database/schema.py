"""SQLAlchemy models for academic database."""
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    department = Column(String)
    cgpa = Column(Float)
    attendance = Column(Float)
    semester = Column(Integer)

class Mark(Base):
    __tablename__ = "marks"
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    subject = Column(String)
    marks = Column(Float)
    semester = Column(Integer)

class Course(Base):
    __tablename__ = "courses"
    course_id = Column(Integer, primary_key=True)
    course_name = Column(String)
    faculty = Column(String)
    credits = Column(Integer)

DATABASE_URL = "sqlite:///./academic.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
