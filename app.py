import os
from flask import Flask, redirect, render_template, request, session, url_for
from flask_pymongo import PyMongo
from datetime import datetime
from bson.objectid import ObjectId
import json

app = Flask(__name__)

app.config["MONGO_DBNAME"] = "appointment_scheduler"
app.config[
    "MONGO_URI"] = "mongodb+srv://philiph80:delrod123@myfirstcluster-yuvii.mongodb.net/appointment_scheduler?retryWrites=true&w=majority"

mongo = PyMongo(app)


@app.route('/')
def entry_page():
    doctors = mongo.db.doctors.find()
    return render_template('entry_page.html', doctors=doctors)


@app.route('/calendar/<selected_doctor_id>')
@app.route('/calendar/<selected_doctor_id>/<selected_date>')
def calendar(selected_doctor_id, selected_date):
    if selected_date:
        timestamp = int(selected_date)
        selected_date = datetime.fromtimestamp(timestamp).strftime('%d/%m/%Y')
    else:
        selected_date = datetime.now().strftime("%d/%m/%Y")

    if selected_doctor_id:
        selected_doctor = mongo.db.doctors.find_one({"_id": ObjectId(selected_doctor_id)})
        calendar = build_calendar(selected_doctor, selected_date)
        doctors = mongo.db.doctors.find()
        patients = list(mongo.db.patients.find())
        day_id = mongo.db.days.find_one({"date": selected_date})["_id"]
        if selected_date == datetime.now().strftime("%d/%m/%Y"):
            date = "Today"
        else:
            date = selected_date
        return render_template("calendar.html", calendar=calendar, patients=patients, day_id=day_id, doctors=doctors,
                               selected_doctor=selected_doctor, date=date)
    else:
        return redirect('/')


def build_calendar(selected_doctor, selected_date):
    calendar = []
    with open('hours.json') as json_hours:
        hours = json.load(json_hours)

    appointments = get_appointments(selected_doctor, selected_date)
    for hour in hours:
        appointment_times = []
        for i in range(4):
            time = hour["times"][i]
            appointment = search_appointments(appointments, time)
            if appointment is not None:
                time_obj = next((item for item in appointment["appointment_slots"] if item["time"] == time), None)
                appointment_times.append({"time": time,
                                          "empty": False,
                                          "first_time": time_obj["first_slot"],
                                          "last_time": time_obj["last_slot"],
                                          "appointment_id": appointment["_id"],
                                          "patient_id": appointment["patient_id"],
                                          "patient_name": appointment["patient_details"]["name"],
                                          "start_time": appointment["first_slot"],
                                          "end_time": appointment["last_slot"]
                                          })
            else:
                appointment_times.append({"time": time, "empty": True})

        calendar.append({"hour": hour["hour"], "times": appointment_times})

    return calendar


def get_appointments(selected_doctor, selected_date):
    filtered_appointments = []
    slot = mongo.db.days.find_one({"date": selected_date})
    if slot is None:
        mongo.db.days.insert_one({"date": selected_date, "appointment_ids": []})
        slot = mongo.db.days.find_one({"date": selected_date})
    appointment_ids = slot["appointment_ids"]
    for appointment_id in appointment_ids:
        appointment = mongo.db.appointments.find_one({
            '$and': [{"_id": ObjectId(appointment_id),
                      "doctor_id": selected_doctor }]
        })
        if appointment is not None:

            appointment_slots = get_times(appointment['first_slot'], appointment['last_slot'])
            patient = mongo.db.patients.find_one({"_id": ObjectId(appointment['patient_id'])})
            appointment.update({'patient_details': patient, "appointment_slots": appointment_slots})
            print("Appointment: ", appointment)
            filtered_appointments.append(appointment)
    return filtered_appointments


def get_times(first_slot, last_slot):
    with open('times.json') as json_times:
        times = json.load(json_times)
    if first_slot == last_slot:
        return [{"time": first_slot, "first_slot": True, "last_slot": True}]
    else:
        filtered_times = times[times.index(first_slot):times.index(last_slot) + 1]
        times_list = []
        for i, time in enumerate(filtered_times):
            if time == filtered_times[0]:
                times_list.append({"time": time, "first_slot": True, "last_slot": False})
            elif time == filtered_times[-1]:
                times_list.append({"time": time, "first_slot": False, "last_slot": True})
            else:
                times_list.append({"time": time, "first_slot": False, "last_slot": False})
            print("times list: ", times_list)
        return times_list


def search_appointments(appointments, time):
    for appointment in appointments:
        times = appointment["appointment_slots"]
        test = next((item for item in times if item["time"] == time), None)
        if test is not None:
            return appointment

    return None


@app.route('/insert_appointment', methods=["POST"])
def insert_appointment():
    start_time = request.form.get('start_time')
    end_time = request.form.get('end_time')
    appointments = mongo.db.appointments
    appointment_id = appointments.insert_one({
        "doctor_id": selected_doctor["_id"],
        "patient_id": request.form.get('patient_id'),
        "first_slot": start_time,
        "last_slot": end_time
    }).inserted_id

    mongo.db.days.update_one({'date': selected_date},
                     {"$push": {"appointment_ids": str(appointment_id)}}
                     )

    return redirect(url_for('calendar'))


@app.route("/updateAppointment", methods=["POST"])
def update_appointment():
    appointments = mongo.db.appointments
    appointments.update({'_id': ObjectId(request.form.get('appointmentId'))},
                        {"$push": {"appointment_list": {"doctor_id": selected_doctor["_id"],
                                                        "type": "patient",
                                                        "patient_id": request.form.get("patient_id")}}}
                        )
    return redirect(url_for('index'))


@app.route("/remove_appointment/<appointmentId>/<dayId>")
def remove_appointment(appointmentId, dayId):
    print("appId", appointmentId)
    mongo.db.appointments.delete_one({"_id": ObjectId(appointmentId)})
    print("dayId", dayId)
    mongo.db.days.update_one({"_id": ObjectId(dayId)}, {"$pull": {"appointment_ids": appointmentId}})
    return redirect(url_for('calendar'))


@app.route('/addPatient')
def addPatient():
    doctors = mongo.db.doctors.find()
    return render_template('addPatient.html', doctors=doctors)


@app.route('/insert_patient', methods=["POST"])
def insert_patient():
    patients = mongo.db.patients
    patients.insert_one(request.form.to_dict())
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
