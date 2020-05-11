from flask import Flask, request, json
import aws_controller
from findface import face_rec
import requests

app = Flask(__name__)

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
            
            url = "https://ngpy61m0ak.execute-api.sa-east-1.amazonaws.com/dev/room/participant"

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

            # Chamando Aplicação de Reconhecimento Facial           
            name = face_rec(file, person)    
            if name == 'Unknown':
                resp_data = "not register"
            elif name == 'Not find':              
                resp_data = 'Not find any face'
            else:
                resp_data = "Register"
            return name