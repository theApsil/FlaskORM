from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///students.db"  # Можно заменить на PostgreSQL или MySQL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class RaceEthnicity(db.Model):
    __tablename__ = "race_ethnicity"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    students = db.relationship("Student", back_populates="race_ethnicity")


class ParentEducation(db.Model):
    __tablename__ = "parent_education"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    students = db.relationship("Student", back_populates="parent_education")


class TestPreparation(db.Model):
    __tablename__ = "test_prep"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    students = db.relationship("Student", back_populates="test_prep")


class Student(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.String(10), nullable=False)
    race_ethnicity_id = db.Column(db.Integer, db.ForeignKey("race_ethnicity.id"))
    parent_education_id = db.Column(db.Integer, db.ForeignKey("parent_education.id"))
    lunch = db.Column(db.String(20), nullable=False)
    test_prep_id = db.Column(db.Integer, db.ForeignKey("test_prep.id"))

    race_ethnicity = db.relationship("RaceEthnicity", back_populates="students")
    parent_education = db.relationship("ParentEducation", back_populates="students")
    test_prep = db.relationship("TestPreparation", back_populates="students")

    scores = db.relationship("StudentScore", back_populates="student")


class Subject(db.Model):
    __tablename__ = "subjects"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    scores = db.relationship("StudentScore", back_populates="subject")


class StudentScore(db.Model):
    __tablename__ = "student_scores"
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"), primary_key=True)
    score = db.Column(db.Integer, nullable=False)

    student = db.relationship("Student", back_populates="scores")
    subject = db.relationship("Subject", back_populates="scores")

# Создаем таблицы в базе данных
with app.app_context():
    db.create_all()
