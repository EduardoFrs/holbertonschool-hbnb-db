from src import db
from src.models.base import Base
from src.models.country import Country

class City(Base):
    __tablename__ = 'city'

    name = db.Column(db.String, nullable=False)
    country_code = db.Column(db.String(10), db.ForeignKey('country.code'), nullable=False, unique=True)

    country = db.relationship('Country', backref=db.backref('cities', lazy=True))

    def __repr__(self):
        return f"<City {self.id} ({self.name})>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "country_code": self.country_code,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @staticmethod
    def create(city_data):
        """Create a new city"""
        country_code = city_data.get('country_code')
        country = Country.get(country_code)
        if not country:
            raise ValueError("Country not found")

        new_city = City(**city_data)
        db.session.add(new_city)
        db.session.commit()
        return new_city

    @staticmethod
    def update(city_id, data):
        """Update an existing city"""
        city = City.get(city_id)

        if not city:
            raise ValueError("City not found")

        for key, value in data.items():
            setattr(city, key, value)

        db.session.commit()
        return city
