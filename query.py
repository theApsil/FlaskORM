from collections import defaultdict

from sqlalchemy import func, desc
from models import Student, RaceEthnicity, ParentEducation, TestPreparation, Subject, StudentScore
from config import db

def to_dict_list(query_result, keys):
    return [dict(zip(keys, row)) for row in query_result]


def get_analytics_from_database(join_class):
    raw_data = (
        db.session.query(
            join_class.name.label("name"),
            Subject.name.label("subject_name"),
            func.min(StudentScore.score).label("min_score"),
            func.max(StudentScore.score).label("max_score"),
            func.avg(StudentScore.score).label("avg_score")
        )
        .join(Student, Student.race_ethnicity_id == join_class.id)
        .join(StudentScore, StudentScore.student_id == Student.id)
        .join(Subject, StudentScore.subject_id == Subject.id)
        .group_by(join_class.name, Subject.name)
        .order_by(join_class.name, Subject.name)
        .all()
    )

    grouped = defaultdict(list)
    for row in raw_data:
        grouped[row.name].append({
            "subject_name": row.subject_name,
            "min_score": row.min_score,
            "max_score": row.max_score,
            "avg_score": float(f"{row.avg_score:.2f}")
        })

    # Преобразуем в список словарей
    result = [{"name": name, "subjects": subjects} for name, subjects in grouped.items()]
    return result



def analytics_score_by_race():
    return get_analytics_from_database(RaceEthnicity)

def analytics_score_by_parent():
    return get_analytics_from_database(ParentEducation)

def analytics_score_by_test_prep():
    return get_analytics_from_database(TestPreparation)

def analytics_score_by_gender():
    raw_data = (
        db.session.query(
            Student.gender.label("name"),
            Subject.name.label("subject_name"),
            func.min(StudentScore.score).label("min_score"),
            func.max(StudentScore.score).label("max_score"),
            func.avg(StudentScore.score).label("avg_score")
        )
        .join(StudentScore, StudentScore.student_id == Student.id)
        .join(Subject, StudentScore.subject_id == Subject.id)
        .group_by(Student.gender, Subject.name)
        .order_by(Student.gender, Subject.name)
        .all()
    )

    grouped = defaultdict(list)
    for row in raw_data:
        grouped[row.name].append({
            "subject_name": row.subject_name,
            "min_score": row.min_score,
            "max_score": row.max_score,
            "avg_score": float(f"{row.avg_score:.2f}")
        })

    # Преобразуем в список словарей
    result = [{"name": name, "subjects": subjects} for name, subjects in grouped.items()]
    return result

def analytics_score_by_lunch():
    raw_data = (
        db.session.query(
            Student.lunch.label("name"),
            Subject.name.label("subject_name"),
            func.min(StudentScore.score).label("min_score"),
            func.max(StudentScore.score).label("max_score"),
            func.avg(StudentScore.score).label("avg_score")
        )
        .join(StudentScore, StudentScore.student_id == Student.id)
        .join(Subject, StudentScore.subject_id == Subject.id)
        .group_by(Student.lunch, Subject.name)
        .order_by(Student.lunch, Subject.name)
        .all()
    )

    grouped = defaultdict(list)
    for row in raw_data:
        grouped[row.name].append({
            "subject_name": row.subject_name,
            "min_score": row.min_score,
            "max_score": row.max_score,
            "avg_score": float(f"{row.avg_score:.2f}")
        })

    # Преобразуем в список словарей
    result = [{"name": name, "subjects": subjects} for name, subjects in grouped.items()]
    return result

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
