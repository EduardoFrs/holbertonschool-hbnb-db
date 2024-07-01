from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declared_attr
from abc import ABC, abstractmethod
from flask_sqlalchemy import SQLAlchemy
import uuid

db = SQLAlchemy()
Base = declarative_base()

class Base(db.Model, ABC):
    """
    Base Interface for all models
    """
    __abstract__ = True


    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)


    @classmethod
    def get(cls, id):
        return cls.query.get(id)

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def delete(cls, id):
        obj = cls.query.get(id)
        if not obj:
            return False
        db.session.delete(obj)
        db.session.commit()
        return True

    @abstractmethod
    def to_dict(self) -> dict:
        """Returns the dictionary representation of the object"""

    @staticmethod
    @abstractmethod
    def create(data: dict) -> Any:
        """Creates a new object of the class"""

    @staticmethod
    @abstractmethod
    def update(entity_id: str, data: dict) -> Any | None:
        """Updates an object of the class"""
