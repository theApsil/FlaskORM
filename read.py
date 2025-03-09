import csv

from config import db
from models import Country, City, Building


def load_buildings_from_csv(file_path):
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            building = Building(
                title=row['name'],
                type_building_id=int(row['id1']),
                city_id=int(row['id2']),
                year=int(row['year']),
                height=float(row['height'])
            )
            db.session.add(building)
        db.session.commit()


def load_city_from_csv(file_path):
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            city = City(
                name=row['name'],
                country_id=int(row['id']),
            )
            db.session.add(city)
        db.session.commit()


def load_counry_from_csv(file_path):
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            country = Country(
                name=row['name'],
            )
            db.session.add(country)
        db.session.commit()



if __name__ == "__main__":
    load_buildings_from_csv('./data/building.csv')
    load_city_from_csv('./data/city.csv')
    load_counry_from_csv('./data/country.csv')
