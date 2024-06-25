from src import db

class Review(db.Model):
    __tablename__ = 'review'

    id = db.Column(db.String(36), primary_key=True)
    place_id = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(db.String(36), primary_key=True)
    comment = db.Column(db.String, nullable=True)
    rating = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f"<Review {self.id} - '{self.comment[:25]}...'>"

    def to_dict(self):
        return {
            "id": self.id,
            "place_id": self.place_id,
            "user_id": self.user_id,
            "comment": self.comment,
            "rating": self.rating,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @staticmethod
    def create(review_data):
        """Create a new review"""
        new_review = Review(**review_data)
        db.session.add(new_review)
        db.session.commit()
        return new_review

    @staticmethod
    def update(review_id, data):
        """Update an existing review"""
        review = Review.query.get(review_id)

        if not review:
            raise ValueError("Review not found")

        for key, value in data.items():
            setattr(review, key, value)

        db.session.commit()
        return review
