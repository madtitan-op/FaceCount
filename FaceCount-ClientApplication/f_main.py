import face_recognition
import cv2
import csv
import ast
import numpy as np
import requests
from reader import reader
import json
from encryptcsv import encryptedMethod


def cam_read(token,system_id):
    rows = reader.csv_read()
    
        

    cv2.namedWindow("Video Feed", cv2.WINDOW_NORMAL)
        # Initialize webcam
    video_capture = cv2.VideoCapture(0)

    new_width = 1080
    new_height = 720

    present = set()

    while True:
        ret, frame = video_capture.read()
        
        if ret:
            cv2.resizeWindow("Video Feed", new_width, new_height)
            # Convert frame to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Find faces and their encodings in the current frame
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
            # print(face_locations)

            # Draw rectangles around the faces
            for (top, right, bottom, left) in face_locations:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            count = False
            # Ensure there is at least one face encoding from the known image and the current frame
            for j in range(len(rows)):
                row = rows[j]
                known_image_encode = row['face_encodings']
                # print(face_encodings)
                if len(known_image_encode) > 0 and len(face_encodings) > 0:
                    
                    
                    known_face_encode = known_image_encode  # direct geting numpy array 
                    unknown_face_encode = face_encodings[0]  # First face encoding from the current frame, here we list of np array that why we have to use 0 

                    # Compare the known face encoding with the unknown face encoding
                    result = face_recognition.compare_faces([known_face_encode], unknown_face_encode, tolerance=0.4)

                    # Display matching result
                    # print(result)
                    if result[0]:
                        
                        count = True
                        # token = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMDAwIiwiaWF0IjoxNzQ3NjQyNjEyLCJleHAiOjE3NDc2NjA2MTJ9.A1fSOfCswz1P__ZnQEu8o2fulO95jmkLD4t3EgLHrnU"
                        if(row['roll'] not in present):
                            cv2.putText(frame, f"{row['name']} your Attendance is successfully marked", (left-180, top-20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                            markdata = {"userId" : row['roll'],"status":'PRESENT',"role":'SYSTEM',"marker_id":system_id}
                            header = {
                                "Authorization": f"Bearer {token}",
                                "Content-Type": "application/json"
                            }
                            
                            response = requests.post('http://localhost:8080/api/attendance/admin/mark',data=json.dumps(markdata),headers=header)
                            print(response.status_code)
                            if (response.status_code == 200):
                                present.add(row['roll'])
                        else:
                            cv2.putText(frame, f"{row['name']} your Attendance is already marked", (left-180, top -20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        
            if not count and len(face_locations) > 0:
                cv2.putText(frame, "Not Matched", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)   

            
            # Show the frame with the face recognition result
            cv2.imshow("Video Feed", frame)
            
            # Break the loop if the 'q' key is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                encryptedMethod() 
                present.clear()
                break

    # Release the video capture object and close all OpenCV windows
    video_capture.release()
    cv2.destroyAllWindows()

    



# # for unknown image
# image_path = r'images/srk.png'
# u_image = face_recognition.load_image_file(image_path)
# u_image_location = face_recognition.face_locations(u_image)
# u_image_encode = face_recognition.face_encodings(u_image)



# if len(known_image_encode)>0 and len(u_image_encode)>0:

#     known_encode = known_image_encode[0]
#     unknown_encode = u_image_encode[0]

#     result = face_recognition.compare_faces([known_encode],unknown_encode,0.6)

#     if result[0]:
#         print("data matched")
    
#     else:
#         print("data not matched")

# else:
#     print("No face found in one or both face")