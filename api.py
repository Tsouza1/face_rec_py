from flask import Flask, request, json
import aws_controller
from werkzeug.utils import secure_filename
from findface import face_rec
import urllib.request
# import urllib.request


app = Flask(__name__)
# Chamada para Criaçao de User
@app.route('/createU', methods=['POST'])
def create_user():
    file = request.files['file']
    form = request.form
    filename = secure_filename(file.filename)

    new_user = aws_controller.create_item(form, file, filename)

    # bucket = "bucketknowface"
    # region_name='sa-east-1'
    # url = "https://%s.s3-%s.amazonaws.com/%s" % (bucket, region_name, filename)
    
    

# @app.route('/createS', methods=['POST'])
# def create_sala():


# Chamada do Script de Face recognition
@app.route('/face_rec', methods=['POST', 'GET'])
def face_recognition():
    person =  json.loads(aws_controller.get_item())

    # image = urllib.request.urlopen(person['url'])
    
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files.get('file')
            # name_id = request.form.get('name_id')            
            
            name = face_rec(file, person)    
            if name == 'Unknown':
                resp_data = "not register"
            elif name == 'bugou':              
                resp_data = 'krl'
            else:
                resp_data = "register"
            return name

app.run()