from model import *
from model.relations import *
from model.cache import region
from flask import Flask, request, render_template
from flask import jsonify
import json
from kafka import KafkaProducer, KafkaConsumer
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import threading


app = Flask (__name__)
"""
@app.route("/")
def index():
   employees = session.query(Employee).all()
   items = []
   for item in employees:
        items.append(
            {      
                "id": item.id,
                "first_name": item.first_name,
                "last_name": item.last_name,
                "email": item.email,
                "phone_number": item.phone_number
            }
        )
   return json.dumps(items)

   @app.route("/employees/add")
   def add_employee ():
        first_name = request.args.get("first_name")
        last_name = request.args.get("last_name")
        email = request.args.get("email")
        phone_number = request.args.get("phone_number")
        employee = Employee(first_name=first_name, last_name=last_name,email=email, phone_number=phone_number)
        session.add(employee)
        session.commit()
        return "{'message': 'Dodan novi radnik u bazu.'}"

"""

socketio = SocketIO(app, cors_allowed_origins="*")
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def json_serializer(data):
    return json.dumps(data).encode('utf-8')

def json_deserializer(data):
    return json.loads(data)

producer = KafkaProducer(
    bootstrap_servers=['kafka:9092'],
    value_serializer=json_serializer
)

consumer = KafkaConsumer(
    'employee',
    bootstrap_servers=['kafka:9092'],
    value_deserializer=json_deserializer,
    group_id='test-group',
    auto_offset_reset='earliest'
)

kafka_thread = None


@app.route("/")
def index ():
    employees = session.query(Employee).all()
    return render_template('employees.html', employees=employees)

@app.route("/employees/delete/<int:id>", methods=["DELETE"])
def delete_employee(id):
    # ID se sada prenosi putem URL-a
    # Dohvati objekt Razred sa navedenim ID-om
    employee = session.query(Employee).get(id)

    if employee:  # ako Razred s ovim ID-om postoji
        session.delete(employee)
        session.commit()
        # Uspješno izbrisano
        return jsonify({'message': f'Zaposlenik sa ID {id} je izbrisan.'}), 200
    else:
        # Nema Razreda s ovim ID-om
        return jsonify({'message': f'Nema zaposlenika s ID {id}.'}), 404

@app.route("/employees/<int:id>", methods=["GET"])
def get_employee(id):
    employee = region.get_or_create(
        f'Employee:{id}', 
        creator=lambda: session.query(Employee).get(id),
        expiration_time=60  
    )
    if employee:
        return jsonify([{"id": employee.id, "first_name": employee.first_name, "last_name": employee.last_name, "email": employee.email, "phone_number": employee.phone_number}]), 200
    else:
        return jsonify({'message': f'Nema zaspolenika s ID {id}.'}), 404

@app.route("/employees/edit", methods=["PUT"])
def edit_employee():
    id = request.form.get("id")
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    phone_number = request.form.get("phone_number")

    if id:  
        employee = session.query(Employee).get(id)
        if employee:  
            if first_name: 
                employee.first_name = first_name
            if last_name: 
                employee.last_name = last_name
            if email: 
                employee.email = email
            if phone_number: 
                employee.phone_number = phone_number
            
            session.commit()

            producer.send("employee", [{"id": employee.id, "first_name": employee.first_name, "last_name": employee.last_name, "email": employee.email, "phone_number": employee.phone_number}])
            producer.flush()

            # Uspješno ažurirano
            return jsonify({'message': f'Zaposlenik sa ID {id} je ažuriran.'}), 200
        else:
            # Nema zasposlenika s ovim ID-om
            return jsonify({'message': f'Nema zaposlenika s ID {id}.'}), 404
    else:
        # Nije pružen ID
        return jsonify({'message': 'ID nije pružen.'}), 400

@app.route("/employees/add", methods=["POST"])
def add_employee():
    # Dohvati ime,prezime,email,broj
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    phone_number = request.form.get("phone_number")
    
    # Dodaj novog zaposlenika
    employee = Employee(first_name=first_name, last_name=last_name, email=email, phone_number=phone_number)
    session.add(employee)
    session.commit()

    producer.send("employee", [{"id": employee.id, "first_name": employee.first_name, "last_name": employee.last_name, "email": employee.email, "phone_number": employee.phone_number}])
    producer.flush()

    # Dobra je praksa vratiti ispravan JSON zahtjev
    return jsonify({'message': 'Dodan novi zaspolenik u bazu.'})

@socketio.on('connect', namespace='/kafka')
def connect():
    global kafka_thread
    if kafka_thread is None or not kafka_thread.is_alive():
        kafka_thread = threading.Thread(target=kafka_consumer)
        kafka_thread.start()

def kafka_consumer():
    for poruka in consumer:
        employee = poruka.value
        socketio.emit('data', {'employee': employee}, namespace='/kafka')

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5000, allow_unsafe_werkzeug=True)