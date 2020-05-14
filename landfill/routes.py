from flask import render_template, request, redirect, flash, url_for
from landfill import app, db
from landfill.models import Fees, User
from landfill.forms import TransactionForm

@app.route('/', methods=['GET', 'POST'])
def home():
    print("requesot made to home with method {}".format(request.method))
    form = TransactionForm() 
    charges = Fees.query.all()
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
                
        return render_template('confirmation.html', grand_total=grand_total, fees=fees, user=user)
    return render_template('home.html', charges=charges, form=form)

@app.route('/confirmation', methods=['POST'])
def confirmation():
    flash("Transaction added to the database")
    return redirect(url_for('home'))

if __name__=="__main__":
    app.run('0.0.0.0', debug=True, ssl_context='adhoc')