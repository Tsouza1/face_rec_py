import sys
import urllib.request
import face_recognition as fr
from PIL import Image

def compare_faces(file1, file2):
    # Load the jpg files into numpy arrays
    image1 = fr.load_image_file(file1)
    image2 = fr.load_image_file(file2)
    
    # Get the face encodings for 1st face in each image file
    image1_encoding = fr.face_encodings(image1)[0]
    image2_encoding = fr.face_encodings(image2)[0]
    
    # Compare faces and return True / False
    results = fr.compare_faces([image1_encoding], image2_encoding)    
    return results[0] 

    
def face_rec(file, person):
   
    known_faces = [(person['name'], urllib.request.urlopen(person['url']))]

    try:        
        for name, known_file in known_faces:
            if compare_faces(known_file,file):
                return name
        return 'Unknown'

    except:
        return 'bugou'