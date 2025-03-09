from config import db
from models import TypeBuilding

BUILDINGS = [
     'Антенная мачта', 
     'Бетонная башня', 
     'Радиомачта', 
     'Гиперболоидная башня', 
     'Дымовая труба', 
     'Решётчатая мачта', 
     'Башня', 
     'Мост'
]

if __name__ == "__main__":
    for name in BUILDINGS:
        item = TypeBuilding(name)
        db.session.add(item)
    db.session.commit()