#!/usr/bin/python3
'''
    Engine for DBStorage
'''
from models.state import Base, State
import models
from models import BaseModel
import sqlalchemy
from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sys import argv
from os import getenv


class DBStorage:
    '''
        Database Storage class that connects to DB 
    '''
    __engine = None
    __session = None

    def __init__(self):
        '''
            Instantiation of DBStorage
        '''
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(getenv('HBNB_MYSQL_USER'),
                                              getenv('HBNB_MYSQL_PWD'),
                                              getenv('HBNB_MYSQL_HOST'),
                                              getenv('HBNB_MYSQL_DB'),
                                              pool_pre_ping=True))
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        '''
            Query the database and send results to user
        '''
        dicts = {}
        classes = []
        if cls in models.classes.values():
            classes.append(cls)
        if cls is None:
            for key, val in models.classes.items():
                classes.append(val)

        for obj in classes:
            try:
                results = self.__session.query(obj).all()
                for item in results:
                    key = str(item.__class__.__name__) + "." + str(item.id)
                    dicts[key] = item
            except:
                continue

        return dicts

    def new(self, obj):
        '''
            Create a new object and add it to current session
        '''
        self.__session.add(obj)

    def delete(self, obj=None):
        '''
             Delete an object from current session
        '''
        if obj is not None:
            self.__session.delete(obj)
            self.save()
        
    def save(self):
        '''
            Save session of database
        '''
        self.__session.commit()

    def reload(self):
        '''
            create all tables in db and current session
        '''
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        DB_Session = scoped_session(session_factory)
        self.__session = DB_Session()