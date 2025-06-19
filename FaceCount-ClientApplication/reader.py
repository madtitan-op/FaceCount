import csv
import numpy as np
from decryptcsv import decryptMethod

class reader:

    def csv_read ():
    #reading s_data.csv file
        decryptMethod()
        # csv_string = decrypted_data.decode('utf-8')
        with open('student_data.csv',mode='r',newline='') as file:
            csv_reader = csv.DictReader(file)
            #converting it into list
            
            #converting the csv file into list
            rows = list(csv_reader)
            

            for data in rows:
                data['face_encodings']=np.array( eval(data['face_encodings']))# converting the string into numpy array 
            
            return rows
        
    
    