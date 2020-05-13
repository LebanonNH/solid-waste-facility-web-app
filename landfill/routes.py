from flask import render_template
from landfill import app, db
from landfill.models import Fees
@app.route('/')
def home():
    return render_template('home.html', charges=db.session.query(Fees).all())


if __name__=="__main__":
    app.run('0.0.0.0', debug=True, ssl_context='adhoc')