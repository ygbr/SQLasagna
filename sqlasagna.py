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

def connect(dsl, **kwargs):
    
    # Connection configuration
    engine = create_engine(dsl, **kwargs)
    
    Base = declarative_base()
    Base.metadata.bind = engine
    
    Session = scoped_session(sessionmaker(bind=engine, autoflush=True))
    se = Session()
    
    # Publish some session methods at module globals scope for quick calls
    globals()['commit'] = se.commit
    globals()['rollback'] = se.rollback
    globals()['execute'] = se.execute
    
    class DBD:
        """This is the magic Mixin, it adds some magic methods to the objects, allowing something like SqlSoup"""
        
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
        def count(cls):
            return se.query(cls).count()
        
        @classmethod
        def filter_by(cls, **kwargs):
            return se.query(cls).filter_by(**kwargs)
        
        @classmethod
        def filter(cls, *args):
            return se.query(cls).filter(*args)
        
        @classmethod
        def get(cls, id):
            return se.query(cls).get(id)
        
        @classmethod
        def query(cls):
            return se.query(cls)
        
        @classmethod
        def first(cls):
            return se.query(cls).first()
        
        @classmethod
        def insert(cls, **kwargs):
            try:
                x = cls(**kwargs)
                se.add(x)
                se.commit()
                return x
            except:
                print("[SQLasagna] Insert Error: " + str(sys.exc_info()))
                se.rollback()
                return False
        
        def save(self):
            try:
                se.add(self)
                se.commit()
                return True
            except:
                print("[SQLasagna] ORM Save Error: " + str(sys.exc_info()))
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
                print("[SQLasagna] Delete Error: " + str(sys.exc_info()))
                se.rollback()
                return False
        
    
    Base.metadata.reflect()
    
    tables = Base.metadata.tables
    
    for i in tables:
        # Here we create all mapper object using declarative base and my Mixin. If you know a better, faster, optimal way of doing this, fell free to change it.
        print("[SQLasagna] Mapping Table %s." % i)
        globals()[i] = type(i, (Base, DBD), {})
        
    for i in tables:
        # Now we map all relationships
        print("[SQLasagna] Mapping Relationships for %s." % i)
        for j in Base.metadata.tables.get(i).foreign_keys:
            t = j.target_fullname.split('.')[0]
            class_mapper(globals().get(i))._configure_property(t, relationship(globals().get(t), backref=i))
    
