from flask import render_template
from flask_restful import Api
from config import app, db
from models import Student
from query import (
    average_score_by_race,
    highest_scoring_subject,
    score_distribution_by_parent_education,
    test_prep_effectiveness,
    gender_performance_difference,
)
from resources import (
    RaceListResource, RaceResource,
    ParentEducationListResource, ParentEducationResource,
    TestPrepListResource, TestPrepResource,
    SubjectListResource, SubjectResource,
    StudentScoreListResource, StudentScoreResource,
    StudentListResource, StudentResource, 
    AnalyticsResource
)
from schemas import ma

api = Api(app)
ma.init_app(app)

api.add_resource(StudentListResource, "/api/students")
api.add_resource(StudentResource, "/api/students/<int:student_id>")

api.add_resource(RaceListResource, "/api/races")
api.add_resource(RaceResource, "/api/races/<int:id>")

api.add_resource(ParentEducationListResource, "/api/parent-education")
api.add_resource(ParentEducationResource, "/api/parent-education/<int:id>")

api.add_resource(TestPrepListResource, "/api/test-prep")
api.add_resource(TestPrepResource, "/api/test-prep/<int:id>")

api.add_resource(SubjectListResource, "/api/subjects")
api.add_resource(SubjectResource, "/api/subjects/<int:id>")

api.add_resource(StudentScoreListResource, "/api/scores")
api.add_resource(StudentScoreResource, "/api/scores/<int:student_id>/<int:subject_id>")

api.add_resource(AnalyticsResource, "/api/analytics/<string:type>")

def get_attr(obj, attr):
    try:
        for part in attr.split("."):
            obj = getattr(obj, part, "N/A") if obj else "N/A"
        return obj
    except AttributeError:
        return "N/A"


@app.route('/')
def index():
    students = Student.query.all()
    race_avg_scores = average_score_by_race()
    top_subject = highest_scoring_subject()
    parent_education_scores = score_distribution_by_parent_education()
    prep_effectiveness = test_prep_effectiveness()
    gender_performance = gender_performance_difference()
    
    return render_template(
        'index.html',
        students=students,
        race_avg_scores=race_avg_scores,
        top_subject=top_subject,
        parent_education_scores=parent_education_scores,
        prep_effectiveness=prep_effectiveness,
        gender_performance=gender_performance,
        get_attr=get_attr
    )


if __name__ == '__main__':
    app.run(debug=True)
