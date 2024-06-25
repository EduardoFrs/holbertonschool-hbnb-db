from src import db

class Country(db.Model):
    __tablename__ = 'country'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    code = db.Column(db.String(10), nullable=False, unique=True)

    cities = db.relationship('City', backref='country', lazy=True)

    def __repr__(self):
        return f"<Country {self.code} ({self.name})>"

    def to_dict(self):
        return {
            "name": self.name,
            "code": self.code,
            "cities": [city.name for city in self.cities]
        }

    @staticmethod
    def get_all():
        """Get all countries"""
        return Country.query.all()

    @staticmethod
    def get(code):
        """Get a country by its code"""
        return Country.query.filter_by(code=code).first()

    @staticmethod
    def create(name, code):
        """Create a new country"""
        new_country = Country(name=name, code=code)
        db.session.add(new_country)
        db.session.commit()
        return new_country
