from flask import render_template
from landfill import app
from landfill.models import charges
@app.route('/')
def home():
    return render_template('home.html', charges=charges)


if __name__=="__main__":
    app.run('0.0.0.0', debug=True, ssl_context='adhoc')