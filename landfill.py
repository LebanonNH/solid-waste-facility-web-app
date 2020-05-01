from flask import Flask, render_template

app = Flask(__name__)
charges = [{'name': "Household Bag", "Unit": "Bag", "Cost": "1"},
           {'name': "Contractor Bag", "Unit": "Bag", "Cost": "1"},
           {'name': "Microwave", "Unit": "Each", "Cost": "4"}
           ]

@app.route('/')
def home():
    return render_template('home.html', charges=charges)


if __name__=="__main__":
    app.run('0.0.0.0', debug=True, ssl_context='adhoc')
