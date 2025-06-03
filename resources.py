from flask_restful import Resource
from flask import request
from models import db, RaceEthnicity, ParentEducation, TestPreparation, Subject, StudentScore
from schemas import (
    RaceEthnicitySchema, ParentEducationSchema, TestPreparationSchema,
    SubjectSchema, StudentScoreSchema, StudentSchema, StudentScoreHyperSchema
)
from query import *

race_schema = RaceEthnicitySchema()
races_schema = RaceEthnicitySchema(many=True)

parent_schema = ParentEducationSchema()
parents_schema = ParentEducationSchema(many=True)

prep_schema = TestPreparationSchema()
preps_schema = TestPreparationSchema(many=True)

subject_schema = SubjectSchema()
subjects_schema = SubjectSchema(many=True)

score_schema = StudentScoreSchema()
scores_schema = StudentScoreSchema(many=True)

student_schema = StudentSchema()
students_schema = StudentSchema(many=True)

student_score_schema = StudentScoreHyperSchema()
student_scores_schema = StudentScoreHyperSchema(many=True)
# Race
class RaceListResource(Resource):
    def post(self):
        data = request.get_json()
        race = RaceEthnicity(name=data["name"])
        db.session.add(race)
        db.session.commit()
        return race_schema.dump(race), 201

    def get(self):
        return races_schema.dump(RaceEthnicity.query.all()), 200

class RaceResource(Resource):
    def get(self, id):
        race = RaceEthnicity.query.get_or_404(id)
        return race_schema.dump(race), 200


# Parent Education
class ParentEducationListResource(Resource):
    def post(self):
        data = request.get_json()
        edu = ParentEducation(name=data["name"])
        db.session.add(edu)
        db.session.commit()
        return parent_schema.dump(edu), 201

    def get(self):
        return parents_schema.dump(ParentEducation.query.all()), 200

class ParentEducationResource(Resource):
    def get(self, id):
        edu = ParentEducation.query.get_or_404(id)
        return parent_schema.dump(edu), 200


# Test Preparation
class TestPrepListResource(Resource):
    def post(self):
        data = request.get_json()
        prep = TestPreparation(name=data["name"])
        db.session.add(prep)
        db.session.commit()
        return prep_schema.dump(prep), 201

    def get(self):
        return preps_schema.dump(TestPreparation.query.all()), 200

class TestPrepResource(Resource):
    def get(self, id):
        prep = TestPreparation.query.get_or_404(id)
        return prep_schema.dump(prep), 200


# Subject
class SubjectListResource(Resource):
    def post(self):
        data = request.get_json()
        subject = Subject(name=data["name"])
        db.session.add(subject)
        db.session.commit()
        return subject_schema.dump(subject), 201

    def get(self):
        return subjects_schema.dump(Subject.query.all()), 200

class SubjectResource(Resource):
    def get(self, id):
        subject = Subject.query.get_or_404(id)
        return subject_schema.dump(subject), 200
    
    def put(self, id):
        subject = db.session.get(Subject, id)
        if not subject:
            return {"error": "Score not found"}, 404

        data = request.get_json()
        subject.name = data.get("name", subject.name)
        db.session.commit()
        return subject_schema.dump(subject), 200
    

    def delete(self, id):
        subject = Subject.query.get_or_404(id)
        db.session.delete(subject)
        db.session.commit()
        return {}, 204


# Student Scores
class StudentScoreListResource(Resource):
    def get(self):
        scores = StudentScore.query.all()
        return {
            "scores": student_scores_schema.dump(scores),
            "_links": {
                "self": {"href": "/scores"},
                "create": {"href": "/scores", "method": "POST"}
            }
        }, 200

    def post(self):
        data = request.get_json()
        score = StudentScore(
            student_id=data["student_id"],
            subject_id=data["subject_id"],
            score=data["score"]
        )
        db.session.add(score)
        db.session.commit()
        return student_score_schema.dump(score), 201


class StudentScoreResource(Resource):
    def get(self, student_id, subject_id):
        score = StudentScore.query.get_or_404((student_id, subject_id))
        return student_score_schema.dump(score), 200

    def put(self, student_id, subject_id):
        score = StudentScore.query.get_or_404((student_id, subject_id))
        data = request.get_json()
        score.score = data.get("score", score.score)
        db.session.commit()
        return student_score_schema.dump(score), 200

    def delete(self, student_id, subject_id):
        score = StudentScore.query.get_or_404((student_id, subject_id))
        db.session.delete(score)
        db.session.commit()
        return {}, 204

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
        return {}, 204


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
    

class AnalyticsResource(Resource):
    def get(self, type):
        if type == "average-score-by-race":
            return analytics_score_by_race()
        elif type == "highest-scoring-subject":
            return highest_scoring_subject()
        elif type == "score-by-parent-education":
            return score_distribution_by_parent_education()
        elif type == "test-prep-effectiveness":
            return test_prep_effectiveness()
        elif type == "gender-performance":
            return gender_performance_difference()
        return {"error": "Unknown analytics type"}, 400
