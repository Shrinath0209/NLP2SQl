"""Populate the academic SQLite database with sample data."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from backend.database.schema import init_db, SessionLocal, Student, Mark, Course

def seed():
    init_db()
    db = SessionLocal()

    # Clear existing
    db.query(Mark).delete()
    db.query(Student).delete()
    db.query(Course).delete()

    students = [
        Student(name="Ipsita S", department="CSE", cgpa=8.7, attendance=82.0, semester=6),
        Student(name="Priya K", department="CSE", cgpa=9.1, attendance=91.0, semester=6),
        Student(name="Rahul M", department="ECE", cgpa=7.4, attendance=68.0, semester=4),
        Student(name="Sneha R", department="CSE", cgpa=6.8, attendance=72.0, semester=6),
        Student(name="Karthik P", department="ME", cgpa=7.9, attendance=88.0, semester=4),
        Student(name="Divya L", department="ECE", cgpa=8.2, attendance=79.0, semester=6),
        Student(name="Arun T", department="CSE", cgpa=5.9, attendance=61.0, semester=2),
        Student(name="Meena J", department="IT", cgpa=8.5, attendance=85.0, semester=4),
        Student(name="Vijay S", department="CSE", cgpa=7.1, attendance=74.0, semester=6),
        Student(name="Anita C", department="ME", cgpa=9.3, attendance=95.0, semester=6),
    ]
    db.add_all(students)
    db.flush()

    subjects = ["Deep Learning", "DBMS", "OS", "Networks", "Math"]
    for s in students:
        for sub in subjects:
            db.add(Mark(student_id=s.id, subject=sub, marks=round(50 + (s.cgpa * 5), 1), semester=s.semester))

    courses = [
        Course(course_name="Deep Learning for NLP", faculty="Dr. Kumar", credits=4),
        Course(course_name="Database Management", faculty="Dr. Sharma", credits=3),
        Course(course_name="Operating Systems", faculty="Dr. Patel", credits=3),
        Course(course_name="Computer Networks", faculty="Dr. Rao", credits=3),
        Course(course_name="Unsupervised Learning", faculty="Dr. Singh", credits=4),
    ]
    db.add_all(courses)
    db.commit()
    db.close()
    print("Database seeded with", len(students), "students!")

if __name__ == "__main__":
    seed()
