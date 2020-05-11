import sys
import urllib.request
import face_recognition as fr
from PIL import Image
import aws_controller

def compare_faces(file1, file2):
    # Carregando Imgans em um Numpy Array
    image1 = fr.load_image_file(file1)
    image2 = fr.load_image_file(file2)
    
    # Get the face encodings for 1st face in each image file
    image1_encoding = fr.face_encodings(image1)[0]
    image2_encoding = fr.face_encodings(image2)[0]
    
    # Comparando Imagens e retornando True / False
    results = fr.compare_faces([image1_encoding], image2_encoding)    
    return results[0] 

    
def face_rec(file, person):
    # Lista de Rosto conhecido recebendo o Nome e Imagem
    known_faces = [(person[0]['name'], aws_controller.get_item('pca-knowns-users', person[0]['userPicture']))]
    
    try:        
        for name, known_file in known_faces:
            if compare_faces(known_file,file):
                return name
        return 'Unknown'

    except:
        return 'Not find'