import csv
from models import db, app, RaceEthnicity, ParentEducation, TestPreparation, Student, Subject, StudentScore


CSV_FILE = "data/StudentsPerformance.csv"

SUBJECTS = ["math", "reading", "writing"]

def get_or_create(model, name):
    """Функция для получения или создания записи в БД."""
    instance = db.session.query(model).filter_by(name=name).first()
    if not instance:
        instance = model(name=name)
        db.session.add(instance)
        db.session.commit()
    return instance

def load_data():
    with app.app_context():
        subjects = {subj: get_or_create(Subject, subj) for subj in SUBJECTS}

        with open(CSV_FILE, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                race_ethnicity = get_or_create(RaceEthnicity, row["race/ethnicity"])
                parent_education = get_or_create(ParentEducation, row["parental level of education"])
                test_prep = get_or_create(TestPreparation, row["test preparation course"])

                student = Student(
                    gender=row["gender"],
                    race_ethnicity_id=race_ethnicity.id,
                    parent_education_id=parent_education.id,
                    lunch=row["lunch"],
                    test_prep_id=test_prep.id
                )
                db.session.add(student)
                db.session.commit()

                for subject_name in SUBJECTS:
                    score = int(row[f"{subject_name} score"])
                    student_score = StudentScore(
                        student_id=student.id,
                        subject_id=subjects[subject_name].id,
                        score=score
                    )
                    db.session.add(student_score)

            db.session.commit()
        print("✅ Данные успешно загружены!")

if __name__ == "__main__":
    load_data()
