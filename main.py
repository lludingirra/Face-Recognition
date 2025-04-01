import cv2
import os
import pickle
import face_recognition
import numpy as np
import cvzone
import sqlite3
from datetime import datetime

conn = sqlite3.connect('students.db')
cursor = conn.cursor()

cap = cv2.VideoCapture(0)
cap.set(3, 640)  # Width
cap.set(4, 480)  # Height

imgBackground = cv2.imread('Resources/background.png')

folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = [cv2.imread(os.path.join(folderModePath, path)) for path in modePathList]

file = open('EncodeFile.p', 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds

modeType = 0  
counter = 0
id = -1
imgStudent = None  

while True: 
    success, img = cap.read()
    if not success:
        break
    img = cv2.flip(img, 1)

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    imgBackground[162:162 + 480, 55:55+640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    if faceCurFrame:

        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
                id = studentIds[matchIndex]
                
                if counter == 0:
                    cvzone.putTextRect(imgBackground,"Loading", (275,400))
                    cv2.imshow('Background', imgBackground)
                    cv2.waitKey(1)
                    counter = 1
                    modeType = 1

        if counter != 0:
            
            if counter == 1:
                cursor.execute("SELECT * FROM students WHERE id = ?", (id,))
                studentInfo = cursor.fetchone()

            if studentInfo[8]:
                image_data = np.frombuffer(studentInfo[8], np.uint8)
                imgStudent = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
            else:
                imgStudent = np.zeros((216, 216, 3), np.uint8)

            datetimeObject = datetime.strptime(studentInfo[7], '%Y-%m-%d %H:%M:%S.%f')
            nowTime = datetime.now()  
            timeDiff = (nowTime - datetimeObject).total_seconds() / 60.0
            print(timeDiff)
            
            if timeDiff > 30:
                new_total_attendance = studentInfo[4] + 1
                cursor.execute("UPDATE students SET total_attendance = ?, last_attendance = ? WHERE id = ?", 
                                (new_total_attendance, nowTime, id))
                conn.commit()
            else:
                modeType = 3
                counter = 0 
                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

            if modeType != 3:
            
                if 10 < counter < 20 :
                    modeType = 2
                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                t_name = studentInfo[1]
                t_major = studentInfo[2]
                t_starting_year = studentInfo[3]
                t_total_attendance = new_total_attendance
                t_standing = studentInfo[5]
                t_year = studentInfo[6]

                if counter <= 10:

                    cv2.putText(imgBackground, str(t_total_attendance), (861, 125), 
                                cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                    
                    cv2.putText(imgBackground, str(t_major), (1006, 550), 
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (50, 50, 50), 1)
                    
                    cv2.putText(imgBackground, str(id), (1006, 493), 
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (100, 100, 100), 1)
                    
                    cv2.putText(imgBackground, str(t_standing), (910, 625), 
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    
                    cv2.putText(imgBackground, str(t_year), (1025, 625), 
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    
                    cv2.putText(imgBackground, str(t_starting_year), (1125, 625), 
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    
                    (w,h), _ = cv2.getTextSize(t_name, cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                    offset = (414 - w) // 2
                    cv2.putText(imgBackground, str(t_name), (808+offset, 445), 
                                cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

                    imgBackground[175:175+216, 909:909+216] = imgStudent

                counter += 1
                
                if counter >= 20:
                    counter = 0
                    modeType = 0
                    studentInfo = []
                    imgStudent = []
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
    else :
        modeType = 0
        counter = 0
        imgStudent = []
        imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    cv2.imshow('Background', imgBackground)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
conn.close()
