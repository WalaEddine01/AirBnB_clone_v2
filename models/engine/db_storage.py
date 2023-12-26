#!/usr/bin/python3
"""
This module defines a class to manage file storage for hbnb clone
"""

from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from os import getenv
from models.base_model import Base


class DBStorage:
    """
    This class manages DB storage for hbnb clone
    """
    __engine = None
    __session = None
    classes = [State, City, User, Place, Review, Amenity]

    def __init__(self):
        """
        Creates the engine self.__engine
        """
        from sqlalchemy import create_engine

        user = getenv("HBNB_MYSQL_USER")
        password = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        database = getenv("HBNB_MYSQL_DB")
        env = getenv("HBNB_ENV")
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(user, password, host, database),
                                      pool_pre_ping=True)
        if env == "test":
            from models.base_model import Base
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Queries all objects depending of the class name
        """
        results = []
        if cls is None:
            for c in self.classes:
                for result in self.__session.query(c):
                    results.append(result)
        else:
            result = self.__session.query(eval(cls))
            results = result.all()

        return {"{}.{}".format(result.__class__.__name__, result.id): result
                for result in results}

    def new(self, obj):
        """
        Adds a new object to the current database session
        """
        if obj:
            self.__session.add(obj)

    def save(self):
        """
        Commits all changes of the current database session
        """
        if self.__session:
            self.__session.commit()

    def delete(self, obj=None):
        """
        Deletes from the current database session obj if not None
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """
        Creates all tables in the database and the
        current database session
        """
        from sqlalchemy.orm import sessionmaker, scoped_session

        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """
        Closes the current database session
        """
        self.__session.close()
