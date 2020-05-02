from flask import Flask, request, json
import aws_controller
from werkzeug.utils import secure_filename
from findface import face_rec
import urllib.request
import requests
# import urllib.request


app = Flask(__name__)

@app.route('/face_rec', methods=['POST', 'GET'])
def face_recognition():
    if request.method == 'POST':
    
        if 'file' in request.files:

            file = request.files.get('file')
            idPerson = request.form.get('idPerson')
            roomId = request.form.get('roomId')
            
            url = "https://84x8skef0k.execute-api.sa-east-1.amazonaws.com/dev/room/participant"

            obj = {
                    "id" : idPerson,
                    "roomId" : roomId
            }
            headers = {
            'Content-Type': 'application/json'
            }
            # print (json.dumps(obj))
            response = requests.request("POST", url, headers=headers, json = obj)
            person = json.loads(response.text)

            # person = aws_controller.get_item(idPerson, roomId)
             
            name = face_rec(file, person)    
            if name == 'Unknown':
                resp_data = "not register"
            elif name == 'Not find':              
                resp_data = 'Not find any face'
            else:
                resp_data = "Register"
            return name