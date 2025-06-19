import face_recognition
import os
from s_data import csv_data

from decryptcsv import decryptMethod

# data = [{'name':"priyanshu",'roll':'15800122073'},
#         {'name': "animesh",'roll':"15800121016"},
#         {'name': "skd",'roll':"15800121020"}
#         ]
data = []
class encodings():
    


    # print(data[0]['name'])
    def face_encoding(img_name,name,roll):
        decryptMethod()
        # img_name = f"{img_name}.jpg"
        img_path = os.path.join("user_photos/",img_name)
        known_image = face_recognition.load_image_file(img_path)
        known_image_location = face_recognition.face_locations(known_image)
        known_image_encode = face_recognition.face_encodings(known_image)
        data_dict = {'name':name , 'roll':roll , 'face_encodings':known_image_encode}
        global data
        data.append(data_dict)
        csv_data(data)
        data.clear()

# i=0 
# def encode(img_name):
#     img_name =f"{img_name}.jpg"
#     image_path = os.path.join("images/", img_name)
#     known_image = face_recognition.load_image_file(image_path)
#     known_image_location = face_recognition.face_locations(known_image)
#     known_image_encode = face_recognition.face_encodings(known_image)
#     global i
#     data[i]['encodings']= known_image_encode
    
#     i = i+1
    # print(known_image_encode)
   
# path = ['pks','ani',"skd"]
# for img in path:
#     encode(img)
# face_encode(input('enter img name only : '),input("enter name : "),input("enter roll : "))

