from flask_restful import Resource
from flask import request
from models import db, Student
from schemas import student_schema, students_schema


class StudentResource(Resource):
    def get(self, student_id):
        student = Student.query.get_or_404(student_id)
        return student_schema.dump(student), 200

    def put(self, student_id):
        student = Student.query.get_or_404(student_id)
        data = request.get_json()

        student.gender = data.get("gender", student.gender)
        student.race_ethnicity_id = data.get("race_ethnicity_id", student.race_ethnicity_id)
        student.parent_education_id = data.get("parent_education_id", student.parent_education_id)
        student.lunch = data.get("lunch", student.lunch)
        student.test_prep_id = data.get("test_prep_id", student.test_prep_id)   

        db.session.commit()
        return student_schema.dump(student), 200

    def delete(self, student_id):
        student = Student.query.get_or_404(student_id)
        db.session.delete(student)
        db.session.commit()
        return 204


class StudentListResource(Resource):
    def get(self):
        students = Student.query.all()
        return students_schema.dump(students), 200

    def post(self):
        data = request.get_json()
        new_student = Student(
            gender=data["gender"],
            race_ethnicity_id=data["race_ethnicity_id"],
            parent_education_id=data["parent_education_id"],
            lunch=data["lunch"],
            test_prep_id=data["test_prep_id"]
        )

        db.session.add(new_student)
        db.session.commit()
        return student_schema.dump(new_student), 201