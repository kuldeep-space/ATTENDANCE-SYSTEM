import cv2
import face_recognition
from datetime import datetime
from image_encoder import encoder
from image_encoder import img_name
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate(
    r"D:\CODING STUFFS\PROJECTS\ATTENDANCE-SYSTEM\Code\serviceAccountKey.json"
)
firebase_admin.initialize_app(
    cred,
    {
        "databaseURL": "https://real-time-attendence-system-default-rtdb.asia-southeast1.firebasedatabase.app/"
    },
)


cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
cap.set(5, 30)

BACKGROUND = cv2.imread(r"PROJECTS/ATTENDANCE-SYSTEM/Resource/NOT MATCHED.png")
PANNEL=cv2.imread(r"D:\CODING STUFFS\PROJECTS\ATTENDANCE-SYSTEM\Resource\PANNEL.png")
Wrong = cv2.imread(r"PROJECTS/ATTENDANCE-SYSTEM/Resource/wrong.png")
Rigth = cv2.imread(r"PROJECTS/ATTENDANCE-SYSTEM/Resource/right.png")

st_encode = encoder()
student_id = img_name()

while True:
    success, frame = cap.read()
    IMG = BACKGROUND.copy()

    if not success:
        print("Webcam not Open")
        break

    frame_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    small_frame = cv2.resize(frame_img, (0, 0), fx=0.5, fy=0.5)

    frame_locations = face_recognition.face_locations(small_frame)
    frame_encodings = face_recognition.face_encodings(small_frame, frame_locations)

    if len(frame_encodings) == 0:
        IMG[471 : 471 + 94, 86 : 86 + 307] = Wrong
        cv2.putText(IMG,"FACE NOT FOUND ",(85, 400),cv2.FONT_HERSHEY_COMPLEX_SMALL,1.5,(0,0,255),4)
    for face_encoding, face_location in zip(frame_encodings, frame_locations):
        result = face_recognition.compare_faces(st_encode, face_encoding, tolerance=0.45)
        if True in result:
            IMG[471 : 471 + 94, 86 : 86 + 307] = Rigth
            IMG[342 : 342 + 82, 48 : 48 + 384] = PANNEL
            id = result.index(True)
            studentinfo = db.reference(f"students/{student_id[id]}").get()
            cv2.putText( IMG,f"REG NO. : {student_id[id]}",(60, 366),cv2.FONT_HERSHEY_COMPLEX_SMALL,0.7,(0,0,0),1)
            cv2.putText(IMG,f"Name : {studentinfo['name']}",(224, 366),cv2.FONT_HERSHEY_COMPLEX_SMALL,0.7,(0,0,0),1)
            cv2.putText(IMG,f"Total Attendance : {studentinfo['total attendance']}",(224, 405),cv2.FONT_HERSHEY_COMPLEX_SMALL,0.7,(0,0,0),1)
            cv2.putText(IMG,f"Year : {studentinfo['year']}",(65, 405),cv2.FONT_HERSHEY_COMPLEX_SMALL,0.7,(0,0,0),1)
            
            t1=studentinfo['last attendance time']
            dt1 = datetime.strptime(t1, "%Y-%m-%d %H:%M:%S")
            dt2 = datetime.now()
            
            diff = dt2 - dt1
            
            if diff.total_seconds() >= 5:
                ref=db.reference(f"students/{student_id[id]}")
                studentinfo['total attendance']+=1
                studentinfo['last attendance time']= dt2.strftime("%Y-%m-%d %H:%M:%S")
                ref.child("total attendance").set(studentinfo['total attendance'])
                ref.child('last attendance time').set(studentinfo['last attendance time'])
            
            else:
                cv2.putText(IMG,"Your attendance has been recorded.",(40, 440),cv2.FONT_HERSHEY_COMPLEX_SMALL,0.9,(0,255,0),1)
            
                
            

        if True not in result:
            IMG[471 : 471 + 94, 86 : 86 + 307] = Wrong

        top, right, bottom, left = face_location
        cv2.rectangle(
            frame, (left * 2, top * 2), (right * 2, bottom * 2), (255, 0, 0), 2
        )

    frame = cv2.resize(frame, (384, 270))

    IMG[50 : 50 + 270, 48 : 48 + 384] = frame

    cv2.imshow("window", IMG)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
