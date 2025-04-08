from sqlalchemy import func, desc
from models import Student, RaceEthnicity, ParentEducation, TestPreparation, Subject, StudentScore
from config import db

def to_dict_list(query_result, keys):
    return [dict(zip(keys, row)) for row in query_result]

def average_score_by_race():
    result = (
        db.session.query(
            RaceEthnicity.name,
            func.avg(StudentScore.score).label("avg_score")
        )
        .join(Student, RaceEthnicity.id == Student.race_ethnicity_id)
        .join(StudentScore, Student.id == StudentScore.student_id)
        .group_by(RaceEthnicity.name)
        .order_by(desc("avg_score"))
        .all()
    )
    return to_dict_list(result, ["race", "avg_score"])

def highest_scoring_subject():
    result = (
        db.session.query(
            Subject.name,
            func.avg(StudentScore.score).label("avg_score")
        )
        .join(StudentScore, Subject.id == StudentScore.subject_id)
        .group_by(Subject.name)
        .order_by(desc("avg_score"))
        .first()
    )
    if result:
        return {"subject": result[0], "avg_score": result[1]}
    return {}

def score_distribution_by_parent_education():
    result = (
        db.session.query(
            ParentEducation.name,
            func.avg(StudentScore.score).label("avg_score")
        )
        .join(Student, ParentEducation.id == Student.parent_education_id)
        .join(StudentScore, Student.id == StudentScore.student_id)
        .group_by(ParentEducation.name)
        .order_by(desc("avg_score"))
        .all()
    )
    return to_dict_list(result, ["education_level", "avg_score"])

def test_prep_effectiveness():
    result = (
        db.session.query(
            TestPreparation.name,
            func.avg(StudentScore.score).label("avg_score")
        )
        .join(Student, TestPreparation.id == Student.test_prep_id)
        .join(StudentScore, Student.id == StudentScore.student_id)
        .group_by(TestPreparation.name)
        .order_by(desc("avg_score"))
        .all()
    )
    return to_dict_list(result, ["prep_course", "avg_score"])

def gender_performance_difference():
    result = (
        db.session.query(
            Student.gender,
            func.avg(StudentScore.score).label("avg_score")
        )
        .join(StudentScore, Student.id == StudentScore.student_id)
        .group_by(Student.gender)
        .order_by(desc("avg_score"))
        .all()
    )
    return to_dict_list(result, ["gender", "avg_score"])
