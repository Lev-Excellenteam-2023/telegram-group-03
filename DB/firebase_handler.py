import datetime
from typing import List, Dict
import firebase_admin
from firebase_admin import credentials, db


def initialize_db():
    # Setting up the Firebase connection
    cred = credentials.Certificate('../private/telegrambot-7fe4d-firebase-adminsdk-vi108-333c66edaa.json')
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://telegrambot-7fe4d-default-rtdb.firebaseio.com/'
    })


def get_db_reference():
    """Get a reference to the 'users' node in the database."""
    return db.reference('users')



def add_record(name: str, phone: str, symptom: str, conversation_txt: str, severity: int):
    ref = get_db_reference()
    record = {
        "date": datetime.datetime.now().strftime('%Y-%m-%d'),
        "name": name,
        "phone": phone,
        "symptom": symptom,
        "conversation_txt": conversation_txt,
        "severity": severity
    }
    ref.push(record)


def delete_all_records():
    ref = get_db_reference()
    ref.delete()


def delete_by_name(name: str):
    ref = get_db_reference()
    snapshot = ref.order_by_child("name").equal_to(name).get()
    for key in snapshot.keys():
        ref.child(key).delete()


def delete_by_severity(severity: int):
    ref = get_db_reference()
    snapshot = ref.order_by_child("severity").equal_to(severity).get()
    for key in snapshot.keys():
        ref.child(key).delete()


def users_sorted_by_severity() -> List[Dict]:
    ref = get_db_reference()
    snapshot = ref.order_by_child("severity").get()
    return list(snapshot.values())


def all_records() -> List[Dict]:
    ref = get_db_reference()
    return list(ref.get().values())
