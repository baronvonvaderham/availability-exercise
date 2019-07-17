from __future__ import absolute_import
from datetime import date

from flask import jsonify
import pytest
import requests

from python.app import app, db, ThinkfulApiClient, Appointment


@pytest.fixture()
def test_client():
    testing_client = app.test_client()
    ctx = app.app_context()
    ctx.push()
    yield testing_client
    ctx.pop()


@pytest.fixture
def init_database():
    db.create_all()
    yield db
    db.drop_all()


def tomorrow():
    from datetime import datetime, timedelta
    return datetime.now() + timedelta(days=1)


def test_api_client__get_schedule_data():
    schedule_data = ThinkfulApiClient.get_schedule_data()
    assert type(schedule_data) == dict


def test_today(test_client):
    response = test_client.get('/today')
    assert response.status_code == 200
    assert response.json == {"today": "{}".format(date.today())}


def test_booked_appointments(test_client, init_database):
    # If we make this request before doing anything else, the response should have no data in it
    response = test_client.get('/booked-appointments')
    assert response.status_code == 200
    assert response.json == []

    # Now let's create some appoinments and try it again
    appointment_1 = Appointment(student_name="John Doe",
                                appointment_time=tomorrow(),
                                advisor_id=12345)
    appointment_2 = Appointment(student_name="Jane Doe",
                                appointment_time=tomorrow(),
                                advisor_id=12345)
    db.session.add(appointment_1)
    db.session.add(appointment_2)
    db.session.commit()
    response = test_client.get('/booked-appointments')
    # Response data should now contain the two appointments we created above
    assert response.status_code == 200
    assert len(response.json) == 2
    assert response.json[0].get('student_name') == "John Doe"
    assert response.json[1].get('student_name') == "Jane Doe"


def test_availability_schedule(test_client):
    response = test_client.get('/availability-schedule')
    assert response.status_code == 200
    # Our two lists of the split up data should both exist in the response data
    assert response.json.get('advisor_ids')
    assert response.json.get('advisor_times')
    # And both should have the same length
    assert len(response.json.get('advisor_ids')) == len(response.json.get('advisor_times'))


def test_book_appointment(test_client, init_database, mocker):
    date = '2019-07-16T23:00:00-04:00'
    appointment = {
        'advisorId': 12345,
        'advisorTime': date,
        'studentName': "Jane Doe",
    }
    data = {'appointment': appointment}
    response = test_client.post('http://localhost:4433/book-appointment', json=data)
    assert response.status_code == 200
    fetch_appointment = Appointment.query.all()
    assert len(fetch_appointment) == 1
    # Now try to book that same appointment again, which should error
    response = test_client.post('http://localhost:4433/book-appointment', json=data)
    assert response.status_code == 400
