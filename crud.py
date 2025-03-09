from config import db
from models import TypeBuilding

item = TypeBuilding('Небоскрёб')
db.session.add(item)
db.session.commit()