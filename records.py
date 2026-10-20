"""Where the patient health records come from.

`InMemoryRecordStore` is the default, so the app and its tests run without any account. `FirestoreRecordStore`
reads the same records from a Firebase Firestore collection called `HealthRecord`.
"""
import os

SAMPLE_RECORDS = [
    {"id": 1, "name": "John", "age": 20, "address": "Highway 37", "Phone": "01304050", "height": 170,
     "weight": 60, "MedicalHistory": "diabetic , Hypertension", "Date": "2020-12-25", "Doctor_Name": "magdy",
     "Diagnose": "Immune Deficiency Syndrome", "Accident": "Car Accident"},
    {"id": 2, "name": "ahmed", "age": 30, "address": "imbaba", "Phone": "01305603", "height": 160,
     "weight": 80, "MedicalHistory": "diabetic", "Date": "2011-11-25", "Doctor_Name": "Wassif",
     "Diagnose": "cancer", "Accident": "Bus Accident"},
    {"id": 1, "name": "John", "age": 20, "address": "Highway 37", "Phone": "01304050", "height": 170,
     "weight": 60, "MedicalHistory": "diabetic , Hypertension", "Date": "2010-11-25", "Doctor_Name": "Hanan",
     "Diagnose": "Preumonin", "Accident": "Train Accident"},
]


class InMemoryRecordStore:
    def __init__(self, records=None):
        self._records = list(SAMPLE_RECORDS if records is None else records)

    def find(self, **criteria):
        """Records whose fields equal every given value, e.g. find(id=1, Date="2020-12-25")."""
        return [dict(r) for r in self._records if all(r.get(k) == v for k, v in criteria.items())]


class FirestoreRecordStore:
    def __init__(self, credentials_path):
        import firebase_admin  # only needed when Firestore is used
        from firebase_admin import credentials, firestore

        firebase_admin.initialize_app(credentials.Certificate(credentials_path))
        self._collection = firestore.client().collection("HealthRecord")

    def find(self, **criteria):
        query = self._collection
        for field, value in criteria.items():
            query = query.where(field, "==", value)
        return [doc.to_dict() for doc in query.stream()]


def default_store():
    """Firestore when FIREBASE_CREDENTIALS points to a service account file, otherwise the sample records."""
    credentials_path = os.environ.get("FIREBASE_CREDENTIALS")
    return FirestoreRecordStore(credentials_path) if credentials_path else InMemoryRecordStore()