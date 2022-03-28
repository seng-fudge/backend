from app import db

from sqlalchemy import *
from sqlalchemy.orm import relationship


class Token(db.Model):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True)

    send_token = Column(Text, nullable=False)
    create_token = Column(Text, nullable=False)

    sessionId = Column(Integer, ForeignKey("sessions.id"))
    session = relationship("Session", back_populates="tokens")


class Session(db.Model):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True)

    time = Column(Integer, nullable=False)

    tokens = relationship("Token", order_by=Token.id, back_populates="session")

    userId = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="sessions")


class Accountdata(db.Model):
    __tablename__ = "accountdatas"

    id = Column(Integer, primary_key=True)

    businessName = Column(Text, nullable=False)
    contactName = Column(Text, nullable=False)
    electronicMail = Column(Text, nullable=False)

    supplierID = Column(Integer, nullable=False)
    street = Column(Text, nullable=False)
    city = Column(Text, nullable=False)
    postcode = Column(Integer, nullable=False)
    country = Column(Text, nullable=False)
    currency = Column(Text, nullable=False)

    userId = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="accountdata")


class User(db.Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    email = Column(Text, nullable=False, unique=True)
    password = Column(Text, nullable=False)

    accountdata = relationship(
        "Accountdata", order_by=Accountdata.id, back_populates="user")
    sessions = relationship("Session", order_by=Session.id, back_populates="user")
