import csv
import os
import numpy as np
from encryptcsv import encryptedMethod

file_name = "student_data.csv"
file_exists = os.path.isfile(file_name) 

def csv_data(data):
    
    with open(file_name,mode="a",newline='') as file :
        fieldname =["name","roll",'face_encodings']
        csv_writer = csv.DictWriter(file,fieldnames = fieldname)
        
        if not file_exists:
            csv_writer.writeheader()

        # for row in data:
        #     row['face_encodings'] = row['face_encodings'][0].tolist() # converting numpy array into list to store in csv file  
        #     csv_writer.writerow(row)

        for row in data:
            face_encoding = row['face_encodings']
            
            # If it's already a NumPy array, just convert it
            if isinstance(face_encoding, np.ndarray):
                row['face_encodings'] = face_encoding.tolist()
            
            # If it's a list with one NumPy array inside
            elif isinstance(face_encoding, list) and isinstance(face_encoding[0], np.ndarray):
                row['face_encodings'] = face_encoding[0].tolist()
            
            # If it's already a list of floats, leave it as-is or convert just to be safe
            elif isinstance(face_encoding, list):
                row['face_encodings'] = list(face_encoding)
            
            # Fallback: convert single float to list (edge case)
            elif isinstance(face_encoding, float):
                row['face_encodings'] = [face_encoding]

            csv_writer.writerow(row)
    encryptedMethod()   