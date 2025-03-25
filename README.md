## [Описание датасета (ветка `dev-lab`)](https://github.com/theApsil/FlaskORM/blob/dev-lab/README.md)

## JSON структура API (hypermedia)
```json
{
  "students": [
    {
      "id": 1,
      "gender": "male",
      "race_ethnicity": "Group A",
      "parent_education": "Bachelor's degree",
      "lunch": "standard",
      "test_prep": "completed",
      "scores": [
        { "subject": "Math", "score": 78 },
        { "subject": "Reading", "score": 85 }
      ],
      "_links": {
        "self": { "href": "/students/1" },
        "scores": { "href": "/students/1/scores" }
      }
    }
  ],
  "_links": {
    "self": { "href": "/students" },
    "create": { "href": "/students", "method": "POST" }
  }
}
```
### `GET /students/{id}` (Описание студента по ID)
```json
{
  "id": 10,
  "gender": "female",
  "race_ethnicity": "Group C",
  "parent_education": "Master's degree",
  "lunch": "free or reduced",
  "test_prep": "none",
  "scores": [
    { "subject": "Math", "score": 90 },
    { "subject": "Reading", "score": 88 }
  ],
  "_links": {
    "self": { "href": "/students/10" },
    "update": { "href": "/students/10", "method": "PUT" },
    "delete": { "href": "/students/10", "method": "DELETE" }
  }
}
```