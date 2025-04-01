import cv2
import face_recognition
import pickle
import os
import sqlite3

conn = sqlite3.connect("students.db")
cursor = conn.cursor()

cursor.execute("SELECT id FROM students")
students = cursor.fetchall()
conn.close()

folderPath = 'Images'
PathList = os.listdir(folderPath)

imgList = []
studentIds = []

for path in PathList:
    student_id = os.path.splitext(path)[0]
    if (student_id,) in students:
        imgList.append(cv2.imread(os.path.join(folderPath, path)))
        studentIds.append(student_id)

def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

encodeListKnown = findEncodings(imgList)
encodeListKnownWithIds = [encodeListKnown, studentIds]

file = open('EncodeFile.p', 'wb')
pickle.dump(encodeListKnownWithIds, file)
file.close()

print('Encoding tamamlandı ve EncodeFile.p oluşturuldu.')

print(studentIds)