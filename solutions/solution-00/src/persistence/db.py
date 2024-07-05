"""
  Now is easy to implement the database repository. The DBRepository
  should implement the Repository (Storage) interface and the methods defined
  in the abstract class Storage.

  The methods to implement are:
    - get_all
    - get
    - save
    - update
    - delete
    - reload (which can be empty)
"""

from src.models.base import Base
from src.persistence.repository import Repository
from src import db
from sqlalchemy.orm.exc import NoResultFound
from src.models import User


class DBRepository(Repository):
    """Dummy DB repository"""

    def __init__(self) -> None:
        """Not implemented"""
        from src.models.user import User


        self.models = {
            "users": User
        }

    def get_all(self, model_name: str) -> list:
        """Get all objects of a model"""
        model_class = Base._decl_class_registry.get(model_name.capitalize())
        if model_class:
            return model_class.query.all()
        return []

    def get(self, model_name: str, obj_id: str) -> Base | None:
        """Get an object by id"""
        model_class = Base._decl_class_registry.get(model_name.capitalize())
        if model_class:
            return model_class.query.get(obj_id)
        return None

    def reload(self) -> None:
        """Not implemented"""

    def save(self, obj: Base) -> None:
        """Save an object"""
        db.session.add(obj)
        db.session.commit()

    def update(self, obj: Base) -> None:
        """Update an object"""
        db.session.commit()

    def delete(self, obj: Base) -> bool:
        """Delete an object"""
        db.session.delete(obj)
        db.session.commit()
        return True
