from flask_marshmallow import Marshmallow
from marshmallow import Schema, fields, post_dump
from models import Student, RaceEthnicity, ParentEducation, TestPreparation, Subject, StudentScore

ma = Marshmallow()

class RaceEthnicitySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RaceEthnicity
        include_relationships = True
        load_instance = True
        exclude = ["students"]

class ParentEducationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ParentEducation
        include_relationships = True
        load_instance = True
        exclude = ["students"]

class TestPreparationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TestPreparation
        include_relationships = True
        load_instance = True
        exclude = ["students"]

class SubjectSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Subject
        include_relationships = True
        load_instance = True
        exclude = ["scores"]

class StudentScoreSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = StudentScore
        include_relationships = True
        load_instance = True

    student_id = ma.auto_field()
    subject_id = ma.auto_field()
    score = ma.auto_field()

class ScoreNestedSchema(Schema):
    subject = fields.String(attribute="subject.name")
    score = fields.Float()

class StudentSchema(Schema):
    id = fields.Int()
    gender = fields.Str()
    race_ethnicity = fields.Method("get_race_ethnicity")
    parent_education = fields.Method("get_parent_education")
    lunch = fields.Str()
    test_prep = fields.Method("get_test_prep")
    scores = fields.Nested(ScoreNestedSchema, many=True)
    _links = fields.Method("get_links")

    def get_race_ethnicity(self, obj):
        return obj.race_ethnicity.name if obj.race_ethnicity else None

    def get_parent_education(self, obj):
        return obj.parent_education.name if obj.parent_education else None

    def get_test_prep(self, obj):
        return obj.test_prep.name if obj.test_prep else None

    def get_links(self, obj):
        return {
            "self": {"href": f"/students/{obj.id}"},
            "scores": {"href": f"/students/{obj.id}/scores"},
            "update": {"href": f"/students/{obj.id}", "method": "PUT"},
            "delete": {"href": f"/students/{obj.id}", "method": "DELETE"},
        }

    @post_dump(pass_many=True)
    def wrap_with_links(self, data, many, **kwargs):
        if many:
            return {
                "students": data,
                "_links": {
                    "self": {"href": "/students"},
                    "create": {"href": "/students", "method": "POST"}
                }
            }
        return data

student_schema = StudentSchema()
students_schema = StudentSchema(many=True)
