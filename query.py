from sqlalchemy import func, desc
from config import db
from models import Building, City, Country, TypeBuilding

def get_building_info():
    return (
        db.session.query(
            Building.title, TypeBuilding.name, Country.name, City.name, Building.year, Building.height
        )
        .join(City, Building.city_id == City.id)
        .join(Country, City.country_id == Country.id)
        .join(TypeBuilding, Building.type_building_id == TypeBuilding.id)
        .order_by(desc(Building.height))
        .all()
    )

def get_height_stats_by_country():
    return (
        db.session.query(
            Country.name,
            func.max(Building.height).label("max_height"),
            func.min(Building.height).label("min_height"),
            func.avg(Building.height).label("avg_height")
        )
        .join(City, Building.city_id == City.id)
        .join(Country, City.country_id == Country.id)
        .group_by(Country.name)
        .order_by(Country.name)
        .all()
    )

def get_height_stats_by_year():
    return (
        db.session.query(
            Building.year,
            func.max(Building.height).label("max_height"),
            func.min(Building.height).label("min_height"),
            func.avg(Building.height).label("avg_height")
        )
        .group_by(Building.year)
        .order_by(Building.year)
        .all()
    )

def get_mast_type_height_stats():
    return (
        db.session.query(
            TypeBuilding.name,
            func.max(Building.height).label("max_height"),
            func.min(Building.height).label("min_height"),
            func.avg(Building.height).label("avg_height")
        )
        .join(TypeBuilding, Building.type_building_id == TypeBuilding.id)
        .filter(TypeBuilding.name.ilike('%мачта%'))
        .group_by(TypeBuilding.name)
        .order_by(desc("avg_height"))
        .all()
    )

def get_height_stats_for_countries_with_multiple_buildings():
    subquery = (
        db.session.query(Building.city_id, func.count(Building.id).label("building_count"))
        .group_by(Building.city_id)
        .having(func.count(Building.id) > 1)
        .subquery()
    )
    
    return (
        db.session.query(
            Country.name,
            func.max(Building.height).label("max_height"),
            func.min(Building.height).label("min_height"),
            func.avg(Building.height).label("avg_height")
        )
        .join(City, Building.city_id == City.id)
        .join(Country, City.country_id == Country.id)
        .join(subquery, subquery.c.city_id == Building.city_id)
        .group_by(Country.name)
        .all()
    )


if __name__ == "__main__":
    print(get_building_info())
    print(get_height_stats_by_country())
    print(get_height_stats_by_year())
    print(get_mast_type_height_stats())
    print(get_height_stats_for_countries_with_multiple_buildings())
