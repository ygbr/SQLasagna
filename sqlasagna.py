#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#   SQLasagna
#
#   @author     Ygor Lemos < ygbr@mac.com >
#               github.com/ygbr/SQLasagna
#

__version__ = '1.0'

import sys
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.sql.expression import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declared_attr


def connect(dsl, **kwargs):
    
    # Connection and session configuration
    engine = create_engine(dsl, **kwargs)
    
    Base = declarative_base()
    Base.metadata.bind = engine
    
    Session = scoped_session(sessionmaker(bind=engine, autoflush=True))
    se = Session()
    
    class Bolognesa:
        """This bogus object holds the returned object"""
        pass
    
    # Publish some session methods at module globals scope for quick calls
    Bolognesa.commit = se.commit
    Bolognesa.rollback = se.rollback
    Bolognesa.execute = se.execute
    
    class Pasta:
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
        def add_column(cls, *args, **kwargs):
            return se.query(cls).add_column(*args, **kwargs)
        
        @classmethod
        def count(cls):
            return se.query(cls).count()
        
        @classmethod
        def order_by(cls, *args, **kwargs):
            return se.query(cls).order_by(*args, **kwargs)
        
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
                instemp = cls(**kwargs)
                se.add(instemp)
                se.commit()
                return instemp
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
    
    for table in tables:
        # Here we create all mapper objects using declarative base and my Mixin
        print("[SQLasagna] Mapping Table %s." % table)
        setattr(Bolognesa, table, type(str(table), (Base, Pasta), {}))
    
    for table in tables:
        # Now we map all relationships
        print("[SQLasagna] Mapping Relationships for %s." % table)
        
        for fk in Base.metadata.tables.get(table).foreign_keys:
            fkn = fk.target_fullname.split('.')[0]
            if fkn != table:
                try:
                    class_mapper(getattr(Bolognesa,table))._configure_property(fkn, relationship(getattr(Bolognesa, fkn), backref=table))
                except:
                    print("[SQLasagna] Problem mapping relationships for %s." % table)
                    print(sys.exc_info())
                    print("[SQLasagna] Re-Mapping Table %s." % table)
                    setattr(Bolognesa, table, type(table, (Base, Pasta), {}))
            else:
                print("[SQLasagna] Not mapping relationship %s into table %s because it is already mapped." %(fkn, table))
    
    return Bolognesa
