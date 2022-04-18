from sqlalchemy import *
from sqlalchemy.orm import relationship

from app import db


class Token(db.Model):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True)

    send_token = Column(Text, nullable=false)

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

    businessName = Column(Text, nullable=True)
    contactName = Column(Text, nullable=True)
    electronicMail = Column(Text, nullable=True)

    supplierID = Column(Integer, nullable=True)
    street = Column(Text, nullable=True)
    city = Column(Text, nullable=True)
    postcode = Column(Text, nullable=True)
    country = Column(Text, nullable=True)
    currency = Column(Text, nullable=True)

    userId = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="accountdata")

class Customer(db.Model):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True)

    buyerReference = Column(Text)
    customerName = Column(Text)
    businessName = Column(Text)
    email = Column(Text)
    streetAddress = Column(Text)
    additionalStreetAddress = Column(Text)
    city = Column(Text)
    postcode = Column(Text)
    country = Column(Text)

    userId = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="customers")

class Payment(db.Model):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)


    dueDate = Column(Text)
    paymentType = Column(Text)
    paymentId = Column(Text)
    paymentTerms = Column(Text)

    userId = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="payments")

class Product(db.Model):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)

    invoiceId = Column(Integer)
    invoiceQuantity = Column(Integer)
    invoiceLineExtension = Column(Integer)
    invoiceName = Column(Text)
    invoicePriceAmount = Column(Integer)
    invoiceBaseQuantity = Column(Integer)    

    userId = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="products")

class User(db.Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    email = Column(Text, nullable=False, unique=True)
    password = Column(Text, nullable=False)

    accountdata = relationship(
        "Accountdata", order_by=Accountdata.id, back_populates="user")
    sessions = relationship(
        "Session", order_by=Session.id, back_populates="user")
    customers = relationship("Customer", order_by=Customer.id, back_populates="user")
    payments = relationship("Payment", order_by=Payment.id, back_populates = "user")
    products = relationship("Product", order_by=Product.id, back_populates = "user")