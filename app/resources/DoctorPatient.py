from flask_restful import Resource, reqparse
from flask import abort, request
from app.models.doctor import Doctor
from app.models import Patient


class DoctorPatientResource(Resource):
    # @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('patient_username', type=str, required=True)
        parser.add_argument('doctor_username', type=str, required=True)
        args = request.get_json()

        try:
            doctor = Doctor.get_doctor_by_username(args["doctor_username"])
            patient = Patient.get_patient_by_username(args["patient_username"])
            if doctor is not None and patient is not None:
                # Add the patient to the list of patients
                patients = doctor.get('patients', [])
                patients.append(args['patient_username'])

                # Update the doctor record with the new list of patients
                doctor_response = Doctor.update_doctor(args["doctor_username"], patients=patients)
                doctors = patient.get('doctors', [])
                doctors.append(args['doctor_username'])
                #
                # # Update the patient record with the new list of doctors
                patient_response = Patient.update_patient(args["patient_username"], doctors=doctors)
                return {'message': 'Doctor and Patient are linked successfully', 'data': {'patient': patient_response, 'doctor': doctor_response}}
            else:
                abort(404, message="Doctor or Patient not found")
        except Exception as e:
            abort(500, message=str(e))

    # @jwt_required()
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('patient_username', type=str, required=True)
        parser.add_argument('doctor_username', type=str, required=True)
        args = request.get_json()
        try:
            doctor = Doctor.get_doctor_by_username(args["doctor_username"])
            patient = Patient.get_patient_by_username(args['patient_username'])
            if doctor is not None and patient is not None:
                # Remove the patient from the list of patients
                patients = doctor.get('patients', [])
                patient_username = args['patient_username']
                if patient_username in patients:
                    patients.remove(patient_username)
                    # Update the doctor record with the updated list of patients
                    doctor_response = Doctor.update_doctor(args["doctor_username"], patients=patients)
                # Remove the doctor from the list of doctor
                doctors = patient.get('doctors', [])
                doctor_username = args['doctor_username']
                if doctor_username in doctors:
                    doctors.remove(doctor_username)
                    # Update the patient record with the updated list of doctors
                    patient_response = Patient.update_patient(args['patient_username'], doctors=doctors)
                return {'message': 'Patient and Doctor are unlinked successfully!'}
            else:
                abort(404)  # Just abort with the status code
        except Exception as e:
            abort(500)  # Just abort with the status code