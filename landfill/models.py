from landfill import db, root_user, root_password
from landfill.conf import fees, cities
from flask_login import UserMixin

class City(db.Model):
    __tablename__ = "city"

    id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(40), nullable=False)
    users = db.relationship("User", backref="city")


    def __repr__(self):
        return '<City {}>'.format(self.city_name)


class User(db.Model):
    __tablename__ = "user"

    barcode = db.Column(db.BigInteger, primary_key=True)
    expiration_date = db.Column(db.Date, nullable=False)
    first_name = db.Column(db.String(40), nullable=False)
    last_name = db.Column(db.String(40), nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    transactions = db.relationship("Transactions")

    def __repr__(self):
        return '<User {} {}>'.format(self.first_name, self.last_name)
    

class Fees(db.Model):

    __tablename__ = "fees"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    weight = db.Column(db.Integer, default = 100, nullable=False)
    unit_of_measure = db.Column(db.String(40))
    fees_per_unit = db.Column(db.Numeric, nullable=False)
    fees = db.relationship("Transactions_Fees")


    def __repr__(self):
        return '<Fee {}-{} per {}>'.format(self.name, self.fees_per_unit, self.unit_of_measure)

class Transactions(db.Model):

    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    barcode = db.Column(db.BigInteger, db.ForeignKey('user.barcode'), nullable=False)
    transaction_timestamp = db.Column(db.DateTime, nullable=False)
    fees = db.relationship("Transactions_Fees")

    def __repr__(self):
        return '<Transaction {}-{}>'.format(self.id, self.transaction_timestamp)


class Transactions_Fees(db.Model):

    __tablename__ = "transactions_fees"

    id = db.Column(db.Integer, primary_key=True)
    transactions_id = db.Column(db.Integer, db.ForeignKey('transactions.id'), nullable=False)
    fees_id = db.Column(db.Integer, db.ForeignKey('fees.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Transaction_Fees {}-{}>'.format(self.transactions_id, self.fees_id)


class Employee(db.Model, UserMixin):

    __tablename__ = "employees"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return '<Employee {}>'.format(self.username)


def populate_data():

    for key, value in fees.items():
        new_fee = Fees(name=key, weight=value['weight'], unit_of_measure=value['unit'], fees_per_unit=value['fee'])  
        db.session.add(new_fee)
    db.session.commit()

    for city in cities:
        new_city = City(city_name=city)
        db.session.add(new_city)
    db.session.commit()

    new_employee = Employee(root_user, root_password)
    session.add(new_employee)
    session.commit()