from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declared_attr
from abc import abstractmethod
from typing import Optional, Any
import uuid
import sqlalchemy as sa

db = SQLAlchemy()
Base = declarative_base()

class Base:
    """
    Base Interface for all models
    """

    id = sa.Column(sa.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = sa.Column(sa.DateTime, default=datetime.now, nullable=False)
    updated_at = sa.Column(sa.DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)


    def __init__(
        self,
        id: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        **kwargs,
    ) -> None:
        """
        Base class constructor
        If kwargs are provided, set them as attributes
        """

        if kwargs:
            for key, value in kwargs.items():
                if hasattr(self, key):
                    continue
                setattr(self, key, value)

        self.id = str(id or uuid.uuid4())
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

    @classmethod
    def get(cls, id) -> "Any | None":
        """
        This is a common method to get an specific object
        of a class by its id

        If a class needs a different implementation,
        it should override this method
        """
        from src.persistence import repo

        return repo.get(cls.__name__.lower(), id)

    @classmethod
    def get_all(cls) -> list["Any"]:
        """
        This is a common method to get all objects of a class

        If a class needs a different implementation,
        it should override this method
        """
        from src.persistence import repo

        return repo.get_all(cls.__name__.lower())

    @classmethod
    def delete(cls, id) -> bool:
        """
        This is a common method to delete an specific
        object of a class by its id

        If a class needs a different implementation,
        it should override this method
        """
        from src.persistence import repo

        obj = cls.get(id)

        if not obj:
            return False

        return repo.delete(obj)

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
