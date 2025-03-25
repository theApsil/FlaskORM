# Семантический профиль API
## 1. Основные сущности  
Представлены в **[Описание датасета (ветка `dev-lab`)](https://github.com/theApsil/FlaskORM/blob/dev-lab/README.md)**
---

## 2. Взаимосвязи сущностей

- **Student** связан с **RaceEthnicity**, **ParentEducation** и **TestPreparation** (многие к одному).
- **StudentScore** связывает **Student** и **Subject** (многие ко многим).
- **Subject** является независимой сущностью.

---
## 3. API Routes
### Студенты

- `POST /students` — Создать нового студента.
- `GET /students` — Получить список всех студентов.
- `GET /students/{id}` — Получить информацию о студенте.
- `PUT /students/{id}` — Обновить данные студента.
- `DELETE /students/{id}` — Удалить студента.

### Этническая принадлежность

- `POST /races` — Создать новую этническую группу.
- `GET /races` — Получить список всех этнических групп.
- `GET /races/{id}` — Получить информацию о конкретной этнической группе.

### Образование родителей

- `POST /parent-education` — Создать новый уровень образования.
- `GET /parent-education` — Получить список всех уровней образования родителей.
- `GET /parent-education/{id}` — Получить информацию о конкретном уровне образования.

### Подготовка к тесту

- `POST /test-prep` — Создать новый вариант подготовки к тесту.
- `GET /test-prep` — Получить список всех вариантов подготовки к тесту.
- `GET /test-prep/{id}` — Получить информацию о конкретной подготовке.

### Предметы

- `POST /subjects` — Создать новый предмет.
- `GET /subjects` — Получить список всех предметов.
- `GET /subjects/{id}` — Получить информацию о предмете.

### Оценки

- `POST /scores` — Добавить оценку студенту.
- `GET /scores` — Получить все оценки.
- `GET /scores/{id}` — Получить информацию об оценке.
- `PUT /scores/{id}` — Обновить оценку.
- `DELETE /scores/{id}` — Удалить оценку.

### Аналитика

- `GET /analytics/average-score-by-race` — Средний балл по расовой принадлежности.
- `GET /analytics/highest-scoring-subject` — Предмет с наивысшим средним баллом.
- `GET /analytics/score-by-parent-education` — Средний балл по уровню образования родителей.
- `GET /analytics/test-prep-effectiveness` — Влияние подготовки на оценки.
- `GET /analytics/gender-performance` — Разница в оценках между полами.

---
## JSON структура API (hypermedia)
### `API Endpoints`
```json
{
  "students": {
    "create": { "href": "/students", "method": "POST" },
    "list": { "href": "/students", "method": "GET" },
    "self": { "href": "/students/{id}", "method": "GET" },
    "update": { "href": "/students/{id}", "method": "PUT" },
    "delete": { "href": "/students/{id}", "method": "DELETE" }
  },
  "races": {
    "create": { "href": "/races", "method": "POST" },
    "list": { "href": "/races", "method": "GET" },
    "self": { "href": "/races/{id}", "method": "GET" }
  },
  "parentEducation": {
    "create": { "href": "/parent-education", "method": "POST" },
    "list": { "href": "/parent-education", "method": "GET" },
    "self": { "href": "/parent-education/{id}", "method": "GET" }
  },
  "testPrep": {
    "create": { "href": "/test-prep", "method": "POST" },
    "list": { "href": "/test-prep", "method": "GET" },
    "self": { "href": "/test-prep/{id}", "method": "GET" }
  }
  "analytics": {
    "averageScoreByRace": { "href": "/analytics/average-score-by-race", "method": "GET" },
    "highestScoringSubject": { "href": "/analytics/highest-scoring-subject", "method": "GET" },
    "scoreByParentEducation": { "href": "/analytics/score-by-parent-education", "method": "GET" },
    "testPrepEffectiveness": { "href": "/analytics/test-prep-effectiveness", "method": "GET" },
    "genderPerformance": { "href": "/analytics/gender-performance", "method": "GET" }
  }
}
```

### `/students` получение списка всех студентов
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