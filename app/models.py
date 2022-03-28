import datetime
from enum import unique
from sqlalchemy import Column, Integer
from app import db

from sqlalchemy import *
from sqlalchemy.orm import relationship
class Token(db.Model):
    __tablename__   = "tokens"
    
    id              = Column(Integer, primary_key = True)
    
    send_token      = Column(Text, nullable = False)
    create_token    = Column(Text, nullable = False)
    
    userId          = Column(Integer, ForeignKey("users.id"))
    user            = relationship("User", back_populates="token")
class Session(db.Model):
    __tablename__ = "sessions"
    
    id = Column(Integer, primary_key = True)
    
    time = Column(Integer, nullable = False)
    
    userId = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="sessions")
class Accountdata(db.model):
    __tablename__   = "accountdatas"

    id              = Column(Integer, primary_key=True)

    businessName    = Column(Text, nullable = False)
    contactName     = Column(Text, nullable = False)
    electronicMail  = Column(Text, nullable = False)

    supplierID      = Column(Integer, nullable = False)
    street          = Column(Text, nullable = False)
    city            = Column(Text, nullable = False)
    postcode        = Column(Integer, nullable = False)
    country         = Column(Text, nullable = False)
    currency        = Column(Text, nullable = False)

    userId          = Column(Integer, ForeignKey("users.id"))
    user            = relationship("User", back_populates="accountdata")
class User(db.Model):
    __tablename__   = "users"
    
    id              = Column(Integer, primary_key=True)
    
    email           = Column(Text, nullable = False, unique = True)
    password        = Column(Text, nullable = False)
    
    token           = relationship("Token", order_by=Token.id, back_populates="user")
    accountdata     = relationship("Accountdata", order_by=Accountdata.id, back_populates="user")