import datetime
import math
from flask import abort, render_template, request, redirect, flash, url_for
from flask_login import login_user, logout_user, login_required
from landfill import app, db, login_manager, bcrypt
from landfill.models import Employee, Fees, User, Transactions, Transactions_Fees
from landfill.forms import TransactionForm, LoginForm


@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(user_id)

@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    print("request made to home with method {}".format(request.method))
    form = TransactionForm() 
    charges = Fees.query.order_by('weight').all()
    if form.validate_on_submit():
        print("form validated")
        data = request.form
        print(data)
        fees = {}
        user = ""
        for key, value in data.items():
            if value:
                if key != "barcode":
                    fee_name = Fees.query.get(key)
                    if fee_name:
                        fees[key] = {"fee": fee_name, "qty": value, "total": fee_name.fees_per_unit * int(value)}
                if key == "barcode":
                    user = User.query.get(value)
        grand_total = 0
        for value in fees.values():
            grand_total += value['total']
        grand_total = math.ceil(float(grand_total) / 1.50)
        return render_template('confirmation.html', grand_total=grand_total, fees=fees, user=user)
    return render_template('home.html', charges=charges, form=form)

@app.route('/confirmation', methods=['POST'])
def confirmation():
    print(request)
    data = request.form
    print(data)
    barcode = data['barcode']
    new_trans = Transactions(barcode=barcode, transaction_timestamp=datetime.datetime.now())
    db.session.add(new_trans)
    db.session.commit()
    for key, value in data.items():
        if key != "barcode":
            t = Transactions_Fees(transactions_id=new_trans.id, fees_id=key, quantity=value)
            db.session.add(t)
    db.session.commit()
    flash("Transaction added to the database")
    return redirect(url_for('home'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print(f"looking for {form.username.data}")
        employee = Employee.query.filter_by(username=form.username.data).first()
        if employee and bcrypt.check_password_hash(employee.password, form.password.data):
            print(f"found employee {employee.username}")
            login_user(employee)

            flash('Logged in successfully.')

            return redirect(url_for('home'))
        else:
            flash("Please check your username and password", "alert-warn")
            return redirect(url_for('login'))
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__=="__main__":
    app.run('0.0.0.0', debug=True, ssl_context='adhoc')