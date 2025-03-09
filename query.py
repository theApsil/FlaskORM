from sqlalchemy import func, desc
from config import db
from models import Student, RaceEthnicity, ParentEducation, TestPreparation, Subject, StudentScore

def average_score_by_race():
    """
    Вычисляет средний балл студентов по расовой/этнической принадлежности.
    """
    return (
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

def highest_scoring_subject():
    """
    Определяет предмет с наивысшим средним баллом среди всех студентов.
    """
    return (
        db.session.query(
            Subject.name,
            func.avg(StudentScore.score).label("avg_score")
        )
        .join(StudentScore, Subject.id == StudentScore.subject_id)
        .group_by(Subject.name)
        .order_by(desc("avg_score"))
        .first()
    )

def score_distribution_by_parent_education():
    """
    Группирует студентов по уровню образования родителей и вычисляет средний балл.
    """
    return (
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

def test_prep_effectiveness():
    """
    Анализирует влияние подготовки к тестам на средний балл студентов.
    """
    return (
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

def gender_performance_difference():
    """
    Сравнивает средний балл между мужчинами и женщинами.
    """
    return (
        db.session.query(
            Student.gender,
            func.avg(StudentScore.score).label("avg_score")
        )
        .join(StudentScore, Student.id == StudentScore.student_id)
        .group_by(Student.gender)
        .order_by(desc("avg_score"))
        .all()
    )