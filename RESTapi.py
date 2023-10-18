from flask import request, Flask, jsonify
import json

app = Flask(__name__)

students = [
    {'id': 1, 'name': 'Panchanand'},
    {'id': 2, 'name': 'Rahul'},
    {'id': 3, 'name': 'Viraj'}
]

nextStudentId = 4


@app.route('/students', methods=['GET'])
def get_students():
    return jsonify(students)


@app.route('/students/<int:id>', methods=['GET'])
def get_students_by_ID():
    student = get_student(id)
    if student is None:
        return jsonify({'error': 'Student does not exist'}, 404)
    return jsonify(student)


def get_student(id):
    return next((s for s in students if s['id'] == id), None)


def student_is_valid(student):
    for key in student.keys():
        if key != 'name':
            return False
        return True


@app.route('/students', methods=['POST'])
def create_students():
    global nextStudentId
    student = json.loads(request.data)
    if not student_is_valid(student):
        return jsonify({'error': 'Invalid employee properties.'}), 400

    student['id'] = nextStudentId
    nextStudentId += 1
    students.append(student)

    return '', 201, {'location': f'/students/{student["id"]}'}


@app.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id: int):
    global students
    student = get_student(id)
    if student is None:
        return jsonify({'error': 'Student does not exist'}), 404
    students = [s for s in students if s['id'] != id]
    return jsonify(student), 200


app.run()
