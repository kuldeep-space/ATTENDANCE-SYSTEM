import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate(r"D:\CODING STUFFS\PROJECTS\KEYS\serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://real-time-attendence-system-default-rtdb.asia-southeast1.firebasedatabase.app/"
})

ref=db.reference('students')

data={
    "1":
        {
            "name":"Kuldeep",
            "year":"2nd",
            "total attendance":0,
            "last attendance time":"2022-12-01 09:54:34"
        },
        "2":
        {
            "name":"Kartik",
            "year":"2nd",
            "total attendance":0,
            "last attendance time":"2022-12-01 09:55:34"
        },
        "3":
        {
            "name":"Ashish",
            "year":"2nd",
            "total attendance":0,
            "last attendance time":"2022-12-01 09:56:34"
        },
        "4":
        {
            "name":"Navin",
            "year":"2nd",
            "total attendance":0,
            "last attendance time":"2022-12-01 09:57:34"
        },
        "5":
        {
            "name":"Shubham",
            "year":"2nd",
            "total attendance":0,
            "last attendance time":"2022-12-01 09:58:34"
        }
}
for key,value in data.items():
    ref.child(key).set(value)


