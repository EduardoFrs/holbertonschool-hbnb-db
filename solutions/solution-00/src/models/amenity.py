from src import db

class Amenity(Base):
    __tablename__ = 'amenity'

    name = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"<Amenity {self.id} ({self.name})>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @staticmethod
    def create(amenity_data):
        """Create a new amenity"""
        new_amenity = Amenity(**amenity_data)
        db.session.add(new_amenity)
        db.session.commit()
        return new_amenity

    @staticmethod
    def update(amenity_id, data):
        """Update an existing amenity"""
        amenity = Amenity.query.get(amenity_id)

        if not amenity:
            return None

        if "name" in data:
            amenity.name = data["name"]

        db.session.commit()
        return amenity


class PlaceAmenity(Base):
    """PlaceAmenity representation"""

    id = db.Column(db.String(36), primary_key=True)
    place_id = db.Column(db.String(36),  db.ForeignKey('place.id'), nullable=False)
    amenity_id = db.Column(db.String(36), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, onupdate=db.func.current_timestamp())

    def __repr__(self) -> str:
        return f"<PlaceAmenity ({self.place_id} - {self.amenity_id})>"

    def to_dict(self) -> dict:
        """Dictionary representation of the object"""
        return {
            "id": self.id,
            "place_id": self.place_id,
            "amenity_id": self.amenity_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @staticmethod
    def get(place_id, amenity_id):
        """Get a PlaceAmenity object by place_id and amenity_id"""
        return PlaceAmenity.query.filter_by(place_id=place_id, amenity_id=amenity_id).first()


    @staticmethod
    def create(data):
        """Create a new PlaceAmenity object"""
        new_place_amenity = PlaceAmenity(**data)
        db.session.add(new_place_amenity)
        db.session.commit()
        return new_place_amenity

    @staticmethod
    def delete(place_id, amenity_id):
        """Delete a PlaceAmenity object by place_id and amenity_id"""
        place_amenity = PlaceAmenity.get(place_id, amenity_id)
        if not place_amenity:
            return False
        db.session.delete(place_amenity)
        db.session.commit()
        return True

    @staticmethod
    def update(entity_id, data):
        """Not implemented, isn't needed"""
        raise NotImplementedError(
            "This method is defined only because of the Base class"
        )
