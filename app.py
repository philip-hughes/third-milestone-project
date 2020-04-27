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


@app.route('/')
def index():
    today = datetime.now().strftime("%d/%m/%Y")
    doctor = "5e8f51b51c9d440000598471"
    hours = mongo.db.appointments.find({"date": today})
    filtered_hours = []
    for hour in hours:
        slots = []
        for time_obj in hour["appointment_list"]:

            if len(time_obj["appointments"]) != 0:

                test = next((item for item in time_obj["appointments"] if item["doctor_id"] == doctor), None)
                if test is not None:
                    patient = mongo.db.patients.find_one({"_id": ObjectId(test["patient_id"])})
                    slots.append(
                        {"time": time_obj["time"], "patient": patient, "empty": False})
                else:
                    slots.append({"time": time_obj["time"], "empty": True})
            else:
                slots.append({"time": time_obj["time"], "empty": True})

        filtered_hours.append({"id": hour["_id"], "hour": hour["hour"], "slots": slots})
        print("hours", filtered_hours)
    return render_template("index.html", hours=filtered_hours)


@app.route('/addAppointment/<appointmentId>/<time>', methods=["POST", "GET"])
def addAppointment(time, appointmentId):
    doctor = "5e8f51b51c9d440000598471"
    patients = mongo.db.patients.find({"doctor_id": doctor})
    return render_template("addAppointment.html", time=time, appointmentId=appointmentId, patients=patients)


@app.route("/updateAppointment", methods=["POST"])
def update_appointment():
    appointments = mongo.db.appointments
    appointments.update({'_id': ObjectId(request.form.get('appointmentId'))},
                        {"$push": {"appointment_list": {"doctor_id": "5e8f51b51c9d440000598471",
                                                        "type": "patient",
                                                        "patient_id": request.form.get("patient_id")}}}
                        )

    return redirect(url_for('index'))


@app.route("/remove_appointment/<appointmentId>")
def remove_appointment(appointmentId):
    print("appId", appointmentId)
    doctor = "5e8f51b51c9d440000598471"
    appointments = mongo.db.appointments
    appointments.update({'_id': ObjectId(appointmentId)},
                        {"$pull": {"appointment_list": {"doctor_id": doctor}}}
                        )
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


def build_calendar(date, doctor_id):
    calendar = []
    hours = [{"hour": "09:00", "times": ["09:00", "09:15", "09:30", "09:45"]},
             {"hour": "10:00", "times": ["10:00", "10:15", "10:30", "10:45"]},
             {"hour": "11:00", "times": ["11:00", "11:15", "11:30", "11:45"]},
             {"hour": "12:00", "times": ["12:00", "12:15", "12:30", "12:45"]},
             {"hour": "13:00", "times": ["13:00", "13:15", "13:30", "13:45"]},
             {"hour": "14:00", "times": ["14:00", "14:15", "14:30", "14:45"]}]

    appointments = get_appointments(date, doctor_id)
    print("Returned from getAppointments:", appointments )
    for hour in hours:
        appointment_times = []
        for i in range(4):
            time = hour["times"][i]
            appointment = search_appointments(appointments, time)
            print('Returned from searchAppointments: ', appointment)
            if appointment is not None:
                appointment_times.append({time: [{"empty": False,
                                                  "appointment_id": appointment["_id"],
                                                  "patient_id": appointment["patient_id"],
                                                  "patient_name": appointment["patient_details"]["name"]}]})
            else:
                appointment_times.append({time: [{"empty": True}]})

        calendar.append({"hour": hour["hour"], "times": appointment_times})

    return calendar


def search_appointments(appointments, time):
    for appointment in appointments:
        print("Search appointments recieved appointment:", appointment)
        times = appointment["times"]
        test = next((item for item in times if item["time"] == time), None)
        if test is not None:
            return appointment

    return None


def get_appointments(date, doctor_id):
    filtered_appointments = []
    slot = mongo.db.slots.find_one({"date": date})
    appointment_ids = slot["appointment_ids"]
    print("appointment_ids ", appointment_ids)
    for appointment_id in appointment_ids:
        appointment = mongo.db.appointments.find_one({
            '$and': [{"_id": ObjectId(appointment_id),
                      "doctor_id": doctor_id}]
        })
        print("appointment ", appointment)
        if appointment is not None:
            patient = mongo.db.patients.find_one({"_id": ObjectId(appointment['patient_id'])})
            appointment.update({'patient_details': patient})
            filtered_appointments.append(appointment)
    return filtered_appointments


calendar = build_calendar("27/04/2020", '5ea578ecd869174818f2c620')
print("Calendar: ", calendar)

if __name__ == '__main__':
    app.run(debug=True)
