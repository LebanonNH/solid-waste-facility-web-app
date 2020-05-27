from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError

from landfill import db
from landfill.models import User, Fees

fees = Fees.query.all()

def barcode_validator(form, field):
    message = "Barcode does not exist in Database"
    user = User.query.get(field.data)
    if not user:
        raise ValidationError(message)

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class TransactionForm(FlaskForm):
    barcode = IntegerField('barcode', validators=[DataRequired(), barcode_validator])
    submit = SubmitField('Submit')
    

for fee in fees:
    setattr(TransactionForm, "charge-" + str(fee.id), IntegerField(fee.name))