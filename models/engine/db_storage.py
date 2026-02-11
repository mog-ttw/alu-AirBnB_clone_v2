#!/usr/bin/python3
"""Database storage engine for AirBnB clone"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from models.base_model import BaseModel, Base
from models.user import User  # import any models you have
# import other models here as needed

import os


class DBStorage:
    """Database storage engine"""
    __engine = None
    __session = None

    def __init__(self):
        """Initialize the database engine"""
        user = os.getenv('HBNB_MYSQL_USER')
        pwd = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        db = os.getenv('HBNB_MYSQL_DB')

        self.__engine = create_engine(
            f'mysql+mysqldb://{user}:{pwd}@{host}/{db}', 
            pool_pre_ping=True
        )

    def all(self, cls=None):
        """Query all objects, or all objects of a class"""
        from models import classes  # dictionary of all classes
        result = {}
        if cls:
            objects = self.__session.query(cls).all()
            for obj in objects:
                key = f"{obj.__class__.__name__}.{obj.id}"
                result[key] = obj
        else:
            for class_name in classes.values():
                objects = self.__session.query(class_name).all()
                for obj in objects:
                    key = f"{obj.__class__.__name__}.{obj.id}"
                    result[key] = obj
        return result

    def new(self, obj):
        """Add an object to the current DB session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current DB session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete obj from session if not None"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Reloads all tables and creates session"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_factory)()

    def close(self):
        """Close the current session"""
        self.__session.close()
