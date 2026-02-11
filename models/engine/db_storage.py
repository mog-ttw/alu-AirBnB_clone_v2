#!/usr/bin/python3
"""DB Storage Engine for AirBnB_clone"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base

class DBStorage:
    """Database storage class for MySQL using SQLAlchemy"""
    __engine = None
    __session = None

    def __init__(self):
        """Initialize the engine"""
        from os import getenv

        HBNB_MYSQL_USER = getenv("HBNB_MYSQL_USER")
        HBNB_MYSQL_PWD = getenv("HBNB_MYSQL_PWD")
        HBNB_MYSQL_HOST = getenv("HBNB_MYSQL_HOST")
        HBNB_MYSQL_DB = getenv("HBNB_MYSQL_DB")

        self.__engine = create_engine(
            f"mysql+mysqldb://{HBNB_MYSQL_USER}:{HBNB_MYSQL_PWD}@{HBNB_MYSQL_HOST}/{HBNB_MYSQL_DB}",
            pool_pre_ping=True
        )

        if getenv("HBNB_ENV") == "test":
            # drop all tables in test DB
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query all objects"""
        pass

    def new(self, obj):
        """Add object to session"""
        pass

    def save(self):
        """Commit session"""
        pass

    def delete(self, obj=None):
        """Delete object from session"""
        pass

    def reload(self):
        """Create tables and session"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_factory)()
