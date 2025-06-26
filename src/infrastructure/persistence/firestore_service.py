import firebase_admin
from firebase_admin import credentials, firestore


class FirestoreService:
    """Generic wrapper вокруг Firestore CRUD операций."""

    def __init__(self, credentials_path: str, project_id: str):
        cred = credentials.Certificate(credentials_path)
        firebase_admin.initialize_app(cred, {"projectId": project_id})
        self.client = firestore.client()

    def get_document(self, collection: str, doc_id: str) -> dict:
        doc = self.client.collection(collection).document(doc_id).get()
        return doc.to_dict() if doc.exists else None

    def set_document(self, collection: str, doc_id: str, data: dict) -> None:
        self.client.collection(collection).document(doc_id).set(data, merge=True)

    def list_documents(self, collection: str) -> list:
        return [doc.to_dict() for doc in self.client.collection(collection).stream()]
