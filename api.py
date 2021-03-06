from flask import Flask, request, json, jsonify
import aws_controller
from findface import face_rec,find_face
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Rota para realizar reconhecimento facial
@app.route('/face_rec', methods=['POST', 'GET'])
def face_recognition():
    if request.method == 'POST':
    
        if 'file' in request.files:

            # Recebendo Variaveis
            file = request.files.get('file')
            idPerson = request.form.get('idPerson')
            if idPerson == None :
                return 'Campo idPerson Obrigatório'
            roomId = request.form.get('roomId')
            if roomId == None :
                return 'Campo roomId Obrigatório'            
            
            url = "https://x29x40ex17.execute-api.sa-east-1.amazonaws.com/dev/room/participant"

            # Criando Objeto para requisição
            obj = {
                    "id" : idPerson,
                    "roomId" : roomId
            }
            headers = {
            'Content-Type': 'application/json'
            }
            
            # Realizando Requisição para Lambda
            response = requests.request("POST", url, headers=headers, json = obj)
            person = json.loads(response.text)
            print(person['name'])
            # Chamando Aplicação de Reconhecimento Facial
            if find_face(file) == 1: 
                name = face_rec(file, person)    
                if name == 'Unknown':
                    resp_data = "not register"
                elif name == 'Not find':              
                    resp_data = 'Not find any face'
                else:
                    resp_data = "Register"
                return name
app.run()