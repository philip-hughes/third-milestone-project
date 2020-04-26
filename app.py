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
            print("timeobj ", time_obj)
            if len(time_obj["appointments"]) != 0:
                print("time_obj apps", time_obj["appointments"])
                test = next((item for item in time_obj["appointments"] if item["doctor_id"] == doctor), None)
                if test != None:
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


def get_appointments(date, doctor_id):
    filtered_appointments = []
    slot = mongo.db.slots.find_one({"date": date})
    print('slot ', slot)
    appointment_ids = slot["appointment_ids"]
    print("appointment_ids ", appointment_ids)
    for appointment_id in appointment_ids:
        appointment = mongo.db.appointments.find_one({
            '$and': [{"_id": ObjectId(appointment_id),
                      "doctor_id": doctor_id}]
        })
        print("appointment ", appointment)
        if appointment is not None:
            filtered_appointments.append(appointment)

    return filtered_appointments


if __name__ == '__main__':
    app.run(debug=True)
