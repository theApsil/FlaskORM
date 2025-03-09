from flask import render_template
from config import app, db
from models import Student
from query import (
    average_score_by_race,
    highest_scoring_subject,
    score_distribution_by_parent_education,
    test_prep_effectiveness,
    gender_performance_difference,
)


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
        gender_performance=gender_performance
    )


if __name__ == '__main__':
    app.run(debug=True)
