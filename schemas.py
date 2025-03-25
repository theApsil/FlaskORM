from flask_marshmallow import Marshmallow
from models import Student, RaceEthnicity, ParentEducation, TestPreparation, Subject, StudentScore

ma = Marshmallow()

class RaceEthnicitySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RaceEthnicity
        include_relationships = True
        load_instance = True

class ParentEducationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ParentEducation
        include_relationships = True
        load_instance = True

class TestPreparationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TestPreparation
        include_relationships = True
        load_instance = True

class SubjectSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Subject
        include_relationships = True
        load_instance = True

class StudentScoreSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = StudentScore
        include_relationships = True
        load_instance = True

class StudentSchema(ma.SQLAlchemyAutoSchema):
    scores = ma.Nested(StudentScoreSchema, many=True)

    class Meta:
        model = Student
        include_relationships = True
        load_instance = True
        exclude = ("race_ethnicity", "parent_education", "test_prep")

student_schema = StudentSchema()
students_schema = StudentSchema(many=True)
