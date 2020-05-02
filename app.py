import os
from flask import Flask, redirect, render_template, request, session, url_for
from flask_pymongo import PyMongo
from datetime import datetime
from bson.objectid import ObjectId

app = Flask(__name__)

app.config["MONGO_DBNAME"] = "appointment_scheduler"
app.config[
    "MONGO_URI"] = "mongodb+srv://philiph80:delrod123@myfirstcluster-yuvii.mongodb.net/appointment_scheduler?retryWrites=true&w=majority"

mongo = PyMongo(app)

selected_doctor_id = ""

@app.route('/')
def entry_page():
    doctors = mongo.db.doctors.find()
    return render_template('entry_page.html', doctors=doctors)


@app.route('/calendar', methods=['POST', 'GET'])
@app.route('/calendar/', methods=['POST', 'GET'])
def calendar():
    today = datetime.now().strftime("%d/%m/%Y")
    doctors = mongo.db.doctors.find()
    doctor = selected_doctor_id
    calendar = build_calendar(today, doctor)
    patients = list(mongo.db.patients.find())
    slot_id = mongo.db.slots.find_one({"date": today})["_id"]
    return render_template("calendar.html", calendar=calendar, patients=patients, slot_id=slot_id, doctors=doctors, doctor=doctor)


@app.route('/set_doctor', methods=['POST', 'GET'])
def set_doctor():
    global selected_doctor_id
    selected_doctor_id = request.form.get('doctor_id')
    return redirect("/calendar")


@app.route('/insert_appointment', methods=["POST"])
def insert_appointment():
    start_time = request.form.get('start_time')
    end_time = request.form.get('end_time')
    times = []
    if start_time == end_time:
        times.append({"time": start_time, "start_time": True, "end_time": True})
    else:
        times = get_times(start_time, end_time)

    appointments = mongo.db.appointments
    appointment_id = appointments.insert_one({
        "doctor_id": selected_doctor_id,
        "patient_id": request.form.get('patient_id'),
        "times": times
    }).inserted_id

    print("Appointment id: ", id)
    slots = mongo.db.slots
    slots.update_one({'_id': ObjectId("5ea5c3c7d869174818f2c62a")},
                     {"$push": {"appointment_ids": str(appointment_id)}}
                     )

    return redirect(url_for('calendar'))


def get_times(start_time, end_time):
    times = ["09:00", "09:15", "09:30", "09:45", "10:00", "10:15", "10:30", "10:45",
             "11:00", "11:15", "11:30", "11:45", "12:00", "12:15", "12:30", "12:45",
             "13:00", "13:15", "13:30", "13:45", "14:00", "14:15", "14:30", "14:45"]

    filtered_times = times[times.index(start_time):times.index(end_time) + 1]
    times_list = []
    for i, time in enumerate(filtered_times):
        if time == filtered_times[0]:
            times_list.append({"time": time, "start_time": True, "end_time": False})
        elif time == filtered_times[-1]:
            times_list.append({"time": time, "start_time": False, "end_time": True})
        else:
            times_list.append({"time": time, "start_time": False, "end_time": False})

    return times_list


@app.route("/updateAppointment", methods=["POST"])
def update_appointment():
    appointments = mongo.db.appointments
    appointments.update({'_id': ObjectId(request.form.get('appointmentId'))},
                        {"$push": {"appointment_list": {"doctor_id": "5e8f51b51c9d440000598471",
                                                        "type": "patient",
                                                        "patient_id": request.form.get("patient_id")}}}
                        )

    return redirect(url_for('index'))


@app.route("/remove_appointment/<appointmentId>/<slotId>")
def remove_appointment(appointmentId, slotId):
    print("appId", appointmentId)
    mongo.db.appointments.delete_one({"_id": ObjectId(appointmentId)})
    mongo.db.slots.update_one({"_id": ObjectId(slotId)}, {"$pull": {"appointment_ids": appointmentId}})
    return redirect(url_for('index'))


@app.route('/addPatient')
def addPatient():
    doctors = mongo.db.doctors.find()
    return render_template('addPatient.html', doctors=doctors)


@app.route('/insert_patient', methods=["POST"])
def insert_patient():
    patients = mongo.db.patients
    patients.insert_one(request.form.to_dict())
    return redirect(url_for('index'))


def build_calendar(date, doctor_id="5ea578ecd869174818f2c620"):
    calendar = []
    hours = [{"hour": "09:00", "times": ["09:00", "09:15", "09:30", "09:45"]},
             {"hour": "10:00", "times": ["10:00", "10:15", "10:30", "10:45"]},
             {"hour": "11:00", "times": ["11:00", "11:15", "11:30", "11:45"]},
             {"hour": "12:00", "times": ["12:00", "12:15", "12:30", "12:45"]},
             {"hour": "13:00", "times": ["13:00", "13:15", "13:30", "13:45"]},
             {"hour": "14:00", "times": ["14:00", "14:15", "14:30", "14:45"]}]

    appointments = get_appointments(date, doctor_id)
    for hour in hours:
        appointment_times = []
        for i in range(4):
            time = hour["times"][i]
            appointment = search_appointments(appointments, time)
            if appointment is not None:
                time_obj = next((item for item in appointment["times"] if item["time"] == time), None)
                appointment_times.append({"time": time,
                                          "empty": False,
                                          "first_time": time_obj["start_time"],
                                          "last_time": time_obj["end"
                                                                "_time"],
                                          "appointment_id": appointment["_id"],
                                          "patient_id": appointment["patient_id"],
                                          "patient_name": appointment["patient_details"]["name"]})
            else:
                appointment_times.append({"time": time, "empty": True})

        calendar.append({"hour": hour["hour"], "times": appointment_times})

    return calendar


def search_appointments(appointments, time):
    for appointment in appointments:
        times = appointment["times"]
        test = next((item for item in times if item["time"] == time), None)
        if test is not None:
            return appointment

    return None


def get_appointments(date, doctor_id):
    filtered_appointments = []
    slot = mongo.db.slots.find_one({"date": date})
    appointment_ids = slot["appointment_ids"]
    for appointment_id in appointment_ids:
        appointment = mongo.db.appointments.find_one({
            '$and': [{"_id": ObjectId(appointment_id),
                      "doctor_id": doctor_id}]
        })
        if appointment is not None:
            patient = mongo.db.patients.find_one({"_id": ObjectId(appointment['patient_id'])})
            appointment.update({'patient_details': patient})
            filtered_appointments.append(appointment)
    return filtered_appointments


if __name__ == '__main__':
    app.run(debug=True)
