from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String, DateTime, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker
from conf import fees, cities

engine = create_engine('sqlite:///landfill.db', echo=True)
Base = declarative_base()
 
########################################################################
class City(Base):
    """"""
    __tablename__ = "city"
 
    id = Column(Integer, primary_key=True)
    city_name = Column(String)

    #----------------------------------------------------------------------
    def __init__(self, city_name):
        """"""
        self.city_name = city_name

class User(Base):
    """"""
    __tablename__ = "user"
 
    barcode = Column(Integer, primary_key=True)
    expiration_date = Column(Date)
    first_name = Column(String)
    last_name = Column(String)
    city_id = Column(String, ForeignKey("city.id"))

    #----------------------------------------------------------------------
    def __init__(self, barcode, expiration_date, first_name, last_name, city_id):
        """"""
        self.barcode = barcode
        self.expiration_date = expiration_date
        self.first_name = first_name
        self.last_name = last_name
        self.city_id = city_id


class Fees(Base):
    """"""
    __tablename__ = "fees"
 
    id = Column(Integer, primary_key=True)
    name = Column(String)
    unit_of_measure = Column(String)
    fees_per_unit = Column(Numeric)

    #----------------------------------------------------------------------
    def __init__(self, name, unit_of_measure, fees_per_unit):
        """"""
        self.name = name
        self.unit_of_measure = unit_of_measure
        self.fees_per_unit = fees_per_unit


class Transactions(Base):
    """"""
    __tablename__ = "transactions"
 
    id = Column(Integer, primary_key=True)
    barcode = Column(Integer, ForeignKey("user.barcode"))
    transaction_timestamp = Column(DateTime)

    #----------------------------------------------------------------------
    def __init__(self, barcode, transaction_timestamp):
        """"""
        self.transaction_timestamp = transaction_timestamp
        self.barcode = barcode

class Transactions_Fees(Base):
    """"""
    __tablename__ = "transactions_fees"
 
    id = Column(Integer, primary_key=True)
    transactions_id = Column(Integer, ForeignKey("transactions.id"))
    fees_id = Column(Integer, ForeignKey("fees.id"))
    quantity = Column(Integer)
    
    #----------------------------------------------------------------------
    def __init__(self, transactions_id, fees_id, quantity):
        """"""
        self.transactions_id = transactions_id
        self.fees_id = fees_id
        self.quantity = quantity


# create tables
Base.metadata.create_all(engine)


DBSession = sessionmaker(bind=engine)
session = DBSession()

for key, value in fees.items():
    new_fee = Fees(key, value['unit'], value['fee'])  
    session.add(new_fee)
session.commit()

for city in cities:
    new_city = City(city)
    session.add(new_city)
session.commit()