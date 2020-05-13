from landfill import db
from landfill.conf import fees, cities

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(40))
    users = db.relationship("User", backref="city")

    def __repr__(self):
        return '<City {}>'.format(self.city_name)


class User(db.Model):
    barcode = db.Column(db.BigInteger, primary_key=True)
    expiration_date = db.Column(db.Date)
    first_name = db.Column(db.String(40))
    last_name = db.Column(db.String(40))
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'))
    transactions = db.relationship("Transactions")

    def __repr__(self):
        return '<User {} {}>'.format(self.first_name, self.last_name)
    

class Fees(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    unit_of_measure = db.Column(db.String(40))
    fees_per_unit = db.Column(db.Numeric)
    fees = db.relationship("Transactions_Fees")

    def __repr__(self):
        return '<Fee {}-{} per {}>'.format(self.name, self.fees_per_unit, self.unit_of_measure)

class Transactions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    barcode = db.Column(db.BigInteger, db.ForeignKey('user.barcode'))
    transaction_timestamp = db.Column(db.DateTime)
    fees = db.relationship("Transactions_Fees")

    def __repr__(self):
        return '<Transaction {}-{}>'.format(self.id, self.transaction_timestamp)


class Transactions_Fees(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transactions_id = db.Column(db.Integer, db.ForeignKey('transactions.id'))
    fees_id = db.Column(db.Integer, db.ForeignKey('fees.id'))
    qty = db.Column(db.Integer)

    def __repr__(self):
        return '<Transaction_Fees {}-{}>'.format(self.transactions_id, self.fees_id)


def populate_data():

    for key, value in fees.items():
        new_fee = Fees(name=key, unit_of_measure=value['unit'], fees_per_unit=value['fee'])  
        db.session.add(new_fee)
    db.session.commit()

    for city in cities:
        new_city = City(city_name=city)
        db.session.add(new_city)
    db.session.commit()