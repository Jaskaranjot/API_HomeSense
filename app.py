import firebase_admin
from firebase_admin import credentials, db
from flask import Flask, request, jsonify
from datetime import datetime
import sqlite3 

connection = sqlite3.connect("homeSenData.db") 
cursor = connection.cursor()

#def create_homeData_table():
 #   cursor.execute("create table HomeData (dateTime DATETIME DEFAULT CURRENT_TIMESTAMP, motionDetected, garageDoorStatus, activityCount)")
  #  connection.commit()


cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred,{'databaseURL':"https://assignment3-c159a-default-rtdb.europe-west1.firebasedatabase.app/"})
ref = db.reference("/HomeData")

app = Flask(__name__)

@app.route('/api/data', methods=['POST'])
def add_data():
    connection = sqlite3.connect("homeSenData.db") 
    cursor = connection.cursor()
    data = request.get_json()

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    motion_Detected = data.get('motionDetected')
    garage_Door_Status = data.get('garageDoorStatus')
    activity_Count = data.get('activityCount')
    new_data = {
        'dateTime': current_time,
        'motionDetected': motion_Detected,
        'garageDoorStatus': garage_Door_Status,
        'activityCount': activity_Count,
    }
    ref.push(new_data)
    cursor.execute(f"insert into HomeData (motionDetected, garageDoorStatus, activityCount) values ('{new_data['motionDetected']}', '{new_data['garageDoorStatus']}','{new_data['activityCount']}')")
    connection.commit()
    return jsonify({"message": "Data added successfully"}), 201

@app.route('/api/lastDoorOpen', methods=['GET'])
def last_door_open():
    data = ref.get()
    Home_data = [entry for entry in data.values() if entry.get('garageDoorStatus') == "open"]

    return jsonify({"sensor_data": Home_data}), 200


@app.route('/api/motionBaseline',methods=['GET'])
def motionDetect():
    numMotion = 0
    sumMotion = 0
    data = ref.get()

    for entry in data.values():
        if entry.get('motionDetected') == 'True' or entry.get('motionDetected') == 'False':
            numMotion +=1
        if entry.get('motionDetected') == 'True':
            sumMotion += entry.get('activityCount')
    avg = sumMotion/numMotion
    return jsonify({"Average_Activity_count": avg}), 200
    

if __name__ == "__main__":
    app.run(debug=True)
#create_homeData_table()