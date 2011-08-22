#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#   SQLasagna
#
# In order to play on a interactive shell and make some queries with SQLasagna, execute: # python3 -i sqlasagna.py
#

__version__ = '1.0'

from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.sql.expression import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declared_attr

# CONFIGURE YOUR CONNECTION HERE - Follow SQLAlchemy create_engine instructions.
# That's pretty much all you have to do!!!
engine = create_engine("mysql+oursql://user:password@yourserver.domain/dbname?charset=utf8&use_unicode=True&autoping=True", echo=True)

# Don't change the following code, unless you know what you're doing.

Base = declarative_base()
Base.metadata.bind = engine

Session = scoped_session(sessionmaker(bind=engine, autoflush=True))
se = Session()

class DBD:
    """This is my magic Mixin, it adds some magic methods to the objects, allowing something like SqlSoup"""
    
    __table_args__ = {'autoload': True}
    
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
    
    def __repr__(self):
        return str(self.__dict__)
        
    @classmethod
    def all(cls):
        return se.query(cls).all()
    
    @classmethod
    def find(cls, **kwargs):
        return se.query(cls).filter_by(**kwargs)
        
    @classmethod
    def get(cls, id):
        return se.query(cls).get(id)
        
    @classmethod
    def query(cls):
        return se.query(cls)
    
    def save(self):
        try:
            se.add(self)
            se.commit()
            return True
        except:
            se.rollback()
            return False
        
    def delete(self):
        try:
            if self.id:
                se.delete(self)
                se.commit()
            else:
                return False
                
            return True
        except:
            se.rollback()
            return False



Base.metadata.reflect()

tables = Base.metadata.tables

for i in tables:
    # Here we create all mapper object using declarative base and my Mixin. If you know a better, faster, optimal way of doing this, fell free to change it.
    print("[SQLasagna] Mapping %s" % i)
    globals()[i] = type(i, (Base, DBD), {})




