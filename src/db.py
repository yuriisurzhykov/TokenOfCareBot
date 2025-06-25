import os

import firebase_admin
from firebase_admin import credentials, firestore

# Инициализация SDK
sa_path = "../" + os.getenv("FIREBASE_CREDENTIALS")
if not sa_path:
    raise RuntimeError("FIREBASE_CREDENTIALS not set")
cred = credentials.Certificate(sa_path)
firebase_admin.initialize_app(cred)

db = firestore.client()
COL = "user_settings"


def get_user_settings(chat_id: str) -> dict:
    doc = db.collection(COL).document(chat_id).get()
    return doc.to_dict() if doc.exists else None


def upsert_user_settings(chat_id: str, min_days: int, max_days: int) -> None:
    db.collection(COL).document(chat_id).set({
        "min_days": min_days,
        "max_days": max_days
    })


def list_all_user_settings() -> list[tuple[str, dict]]:
    return [(doc.id, doc.to_dict()) for doc in db.collection(COL).stream()]
