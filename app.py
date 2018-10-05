from flask import Flask
from flask import jsonify
from flask import request
from flask import abort

app = Flask(__name__)

medicine = [
    {
        'name': u'tylenol'
    },
    {
        'name': u'asprin'
    }
]

patients = [
    {
        'name': u'Anthony',
        'medicine': []
    },
    {
        'name': u'John',
        'medicine': []
    }
]


@app.route('/medicine')
def get_medicine():
    return jsonify({'medicine': medicine})


@app.route('/patients')
def get_patients():
    return jsonify({'patients': patients})


@app.route('/addPatient', methods=['POST'])
def add_patient():
    if not request.json or 'name' not in request.json:
        abort(400)
    patient = {
        'name': request.json['name'],
        'medicine': []
    }
    patients.append(patient)
    return jsonify({'patients': patients}), 201


@app.route('/addMedicine', methods=['POST'])
def add_medicine():
    if not request.json or not 'name' in request.json:
        abort(400)
    med = {
        'name': request.json['name']
    }
    medicine.append(med)
    return jsonify({'medicine': med}), 201


@app.route('/assignMedicine/<string:patient_name>', methods=['PUT'])
def assign_medicine(patient_name):
    if not request.json or not 'name' in request.json:
        abort(400)
    addedMed = {}
    for med in medicine:
        if med['name'] == request.json['name']:
            addedMed = med
    if not addedMed or addedMed == {}:
        abort(400)

    for patient in patients:
        if patient['name'] == patient_name:
            originalMeds = patient['medicine']
            originalMeds.append(addedMed)
            patient['medicine'] = originalMeds
            return jsonify({'patients': patients}), 201

    abort(400)


@app.route('/removeMedicine/<string:patient_name>', methods=['PUT'])
def remove_medicine(patient_name):
    if not request.json or not 'name' in request.json:
        abort(400)
    removedMed = {}
    for med in medicine:
        if med['name'] == request.json['name']:
            removedMed = med
    if not removedMed or removedMed == {}:
        abort(400)

    for patient in patients:
        if patient['name'] == patient_name:
            originalMeds = patient['medicine']
            originalMeds.remove(removedMed)
            patient['medicine'] = originalMeds
            return jsonify({'patients': patients}), 201

    abort(400)


if __name__ == '__main__':
    app.run()
