from __future__ import absolute_import
from datetime import date, datetime
from http import HTTPStatus
import json
import requests

from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///availability.db'
CORS(app)
db = SQLAlchemy(app)
db.create_all()
migrate = Migrate(app, db)


class ThinkfulApiClient:
    """
    A class to contain methods for interactiong with the Thinkful API
    (probably overkill for this exercise since it just needs one really simple function, but this assumes there
     are more endpoints we want to consume when the app is potentially expanded upon later, which would go here)
    """
    @staticmethod
    def get_schedule_data():
        response = requests.get("https://www.thinkful.com/api/advisors/availability")
        return json.loads(response.content)


class Appointment(db.Model):
    """
    A simple persistent model for storing booked appointments.
    """
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(64)) # Ideally this would instead be a FK to a Student or User model of some kind
    appointment_time = db.Column(db.DateTime)
    advisor_id = db.Column(db.Integer)  # And this would be a FK to an Advisor model

    __table_args__ = (
        # Don't let the same student book the same time more than once
        # This isn't ideal in case two students have the same name, would be more robust with a Student model as a FK
        # to enforce uniqueness independent of the students' names
        db.UniqueConstraint('student_name', 'appointment_time', name='_unique_student_and_time'),
    )

    def __repr__(self):
        return '{time} -- {student} with {advisor}'.format(time=self.appointment_time,
                                                           student=self.student_name,
                                                           advisor=self.advisor_id)


@app.route("/today", methods=["GET"])
def today():
    """Returns today's date, properly formatted"""
    return jsonify({"today": date.today().isoformat()})


@app.route("/booked-appointments", methods=["GET"])
def booked_appointments():
    """
    An endpoint to retrieve all booked appointments from the db
    """
    all_appointments = Appointment.query.all()
    data = []
    for appointment in all_appointments:
        data.append({
            'advisor_id': appointment.advisor_id,
            'student_name': appointment.student_name,
            'time': appointment.appointment_time,
        })
    return jsonify(data)


@app.route("/availability-schedule", methods=["GET"])
def availability_schedule():
    """
    An endpoint to retrieve the availability from the Thinkful API, then process that
    data into a usable form expected by the React front-end.
    """
    raw_schedule = ThinkfulApiClient.get_schedule_data()

    # First sort this so we have a nice dict of advisor => all time slots for that advisor
    schedule_dict = {}
    for day, slots in raw_schedule.items():
        for time, advisor_id in slots.items():
            if schedule_dict.get(advisor_id):
                schedule_dict[advisor_id].append(time)
            else:
                schedule_dict[advisor_id] = [time]

    # Now this needs to be broken back up into two parallel lists so we can use the indices later
    # when determining the row that was clicked to book the appointment
    advisor_ids = []
    advisor_times = []
    for advisor_id, slots in schedule_dict.items():
        advisor_ids.append(advisor_id)
        advisor_times.append(slots)

    data = {'advisor_ids': advisor_ids, 'advisor_times': advisor_times}

    return jsonify(data)


@app.route("/book-appointment", methods=["POST"])
def book_appointment():
    """
    An endpoint to book a new appointment
    """
    try:
        appointment_data = json.loads(request.data).get('appointment')
        datetime_string = appointment_data.get('advisorTime')[:-6].replace('T', ' ')
        tz_offset = appointment_data.get('advisorTime')[-6:]
        tz_offset = tz_offset.replace(':', '')
        formatted_datetime = datetime.strptime(datetime_string + ' ' + tz_offset, '%Y-%m-%d %H:%M:%S %z')

        appointment = Appointment(
            student_name=appointment_data.get('studentName'),
            appointment_time=formatted_datetime,
            advisor_id=appointment_data.get('advisorId'),
        )
        db.session.add(appointment)
        db.session.commit()
        return Response(status=HTTPStatus.OK)
    except exc.IntegrityError:
        db.session.rollback()
        return Response(status=HTTPStatus.BAD_REQUEST)
