# pipenv shell (to enter Python)
# > from app import db
# >db.create_all()
# CRTL + C (to exit Python)
# python app.py (to start hosting the database)

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Month(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    start_day = db.Column(db.Integer, nullable=False)
    days_in_month = db.Column(db.Integer, nullable=False)
    days_in_previous_month = db.Column(db.Integer, nullable=False)
    reminders = db.Column(db.relationship('Reminder', backref='reminder', cascade='all, delete, delete-orphan'))


    def __init__(self, name, year, start_day, days_in_month, days_in_previous_month):
        self.name = name
        self.year = year
        self.start_day = start_day
        self.days_in_month = days_in_month
        self.days_in_previous_month = days_in_previous_month


class Reminder(db.Model):
    id =db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False)
    date = db.Column(db.Integer, nullable=False)
    month_id = db.Column(db.Integer, db.ForeignKey('month.id'), nullable=False)


    def __init__(self, text, date, month_id):
        self.text = text
        self.date = date
        self.month_id = month_id

class ReminderSchema(ma.Schema):
    class Meta:
        fields = ('id', 'text', 'date', 'month_id')

Reminder_schema = ReminderSchema()
multi_reminder_schema = ReminderSchema(many=True)

class MonthSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'year', 'start_day', 'days_in_month', 'days_in_previous_month')
    reminders = ma.Nested(multi_reminder_schema)


month_schema = MonthSchema()
multi_month_schema = MonthSchema(many=True)


# Endpoint to add a month
@app.route('/month/add', methods=['POST'])

def add_reminder():
    if request.content_type != 'application/json':
        return jsonify('Error: You are kind of a putz...the data MUST be sent as JSON!')

    post_data = request.get_json()
    name = post_data.get('name')
    year = post_data.get('year')
    start_day = post_data.get('start_day')
    days_in_month = post_data.get('days_in_month')
    days_in_previous_month = post_data.get('days_in_previous_month')

    if name == None:
        return jsonify('Error: What do you think this is? You must provide a Month!')
    if year == None:
        return jsonify('Error: What do you think this is? You must provide a value2!')

    new_record = Month(name, year, start_day, days_in_month, days_in_previous_month)
    db.session.add(new_record)
    db.session.commit()

    return jsonify(month_schema.dump(new_record))

# Endpoint to add multiple months

def add_multiple_months():
    if request.content_type != 'application/json':
        return jsonify('Error: You are kind of a putz...the data MUST be sent as JSON!')

    post_data = request.get_json()
    data = post_data.get("data")

    new_records = []

    for month in data:
        name = month.get("name")
        year = month.get("year")
        start_day = month.get("start_day")
        days_in_month = month.get("days_in_month")
        days_in_previous_month = month.get("previous_days_in_month")

        existing_month_check = db.session.query(Month).filter(Month.name == name).filter(Month.year == year).first()
        if existing_month_check is not None:
            return jsonify("Error: You're trying to manage the calendar wrong, NOODLE BRAIN!")
        else:
            new_record = Month(name, year, start_day, days_in_month, days_in_previous_month)
            db.session.add(new_record)
            db.commit()
            new_records.append(new_record)

    return jsonify(multi_month_schema.dump(new_record))

# Endpoint to query all months
@app.route('/month/get', methods=['GET'])

def get_all_months():
    all_records = db.session.query(Month).all()
    return jsonify(multi_name_schema.dump(all_records))

# Endpoint to query one month
@app.route('/month/get/<id>', methods=['GET'])

def get_month_id(id):
    one_month = db.session.query(Month).filter(Month.id == id).first()
    return jsonify(name_schema.dump(one_month))

# Endpoint to delete a month
@app.route('/month/delete/<id>', methods=['DELETE'])

def month_to_delete(id):
    delete_month = db.session.query(Month).filter(Month.id == id).first()
    db.session.delete(delete_month)
    db.session.commit()
    return jsonify("Well, that's just great...it's gone. YOU DELETED IT!")

# Endpoint to update/edit a month
@app.route('/month/update/<id>', methods=['PUT'])

def update_month_id(id):
    if request.content_type != 'application/json':
        return jsonify('Error: You are kind of a putz...the data must be sent as JSON!')

    put_data = request.get_json()
    name = put_data.get('name')
    year = put_data.get('year')

    month_to_update = db.session.query(Month).filter(Month.id == id).first()

    if name != None:
        month_to_update.name = name
    if year != None:
        month_to_update.year = year

    db.session.commit()

    return jsonify(month_schema.dump(month_to_update))


# Endpoint to add a reminder
@app.route('/reminder/add', methods=['POST'])

def add_reminder():
    if request.content_type != 'application/json':
        return jsonify('Error: You are kind of a putz...the data MUST be sent as JSON!')

    post_data = request.get_json()
    name = post_data.get('name')
    year = post_data.get('year')
    year = post_data.get('start_day')
    year = post_data.get('days_in_month')
    year = post_data.get('days_in_previous_month')

    if name == None:
        return jsonify('Error: What do you think this is? You must provide a Month!')
    if title == None:
        return jsonify('Error: What do you think this is? You must provide a value2!')

    new_record = Month(name, year)
    db.session.add(new_record)
    db.session.commit()

    return jsonify(name_schema.dump(new_record))


# Endpoint to query all months
@app.route('/reminder/get', methods=['GET'])

def get_all_months():
    all_records = db.session.query(Month).all()
    return jsonify(multi_reminder_schema.dump(all_records))

# Endpoint to query one reminder
@app.route('/reminder/get/<id>', methods=['GET'])

def get_reminder_id(id):
    one_reminder = db.session.query(Month).filter(Month.id == id).first()
    return jsonify(reminder_schema.dump(one_reminder))

# Endpoint to delete a reminder
@app.route('/reminder/delete/<id>', methods=['DELETE'])

def reminder_to_delete(id):
    delete_reminder = db.session.query(Reminder).filter(Reminder.id == id).first()
    db.session.delete(delete_reminder)
    db.session.commit()
    return jsonify("Well, that's just great...it's gone. YOU DELETED IT!")

# Endpoint to update/edit a reminder
@app.route('/reminder/update/<id>', methods=['PUT'])

def update_reminder_id(id):
    if request.content_type != 'application/json':
        return jsonify('Error: You are kind of a putz...the data must be sent as JSON!')

    put_data = request.get_json()
    name = put_data.get('name')
    year = put_data.get('year')

    month_to_update = db.session.query(Reminder).filter(Reminder.id == id).first()

    if name != None:
        reminder_to_update.name = name
    if year != None:
        reminder_to_update.year = year

    db.session.commit()

    return jsonify(month_schema.dump(month_to_update))



if __name__ == '__main__':
    app.run(debug=True)