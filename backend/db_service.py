import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import json

class DatabaseService:
    def __init__(self, credentials_path: str):
        # Prevent double-initialization error during reloads
        if not firebase_admin._apps:
            cred = credentials.Certificate(credentials_path)
            firebase_admin.initialize_app(cred)
        self.db = firestore.client()

    def save_health_record(self, user_id: str, record_data: dict):
        """Save a processed health record"""
        doc_ref = self.db.collection('health_records').document()
        
        # Handle the structured data (it comes as a string from Gemini, needs to be JSON)
        try:
            structured_json = json.loads(record_data.get('structured_data', '{}'))
        except:
            structured_json = {"error": "Could not parse JSON", "raw": record_data.get('structured_data')}

        record = {
            'record_id': doc_ref.id,
            'user_id': user_id,
            'record_type': structured_json.get('report_type', 'unknown'),
            'date': datetime.now(), # Default to now, can update from extracted date later
            'raw_text': record_data.get('raw_text'),
            'structured_data': structured_json,
            'created_at': datetime.now()
        }
        
        doc_ref.set(record)
        
        # Also create timeline event
        self.create_timeline_event(user_id, record)
        
        return doc_ref.id

    def create_timeline_event(self, user_id: str, record: dict):
        """Create a timeline event from a health record"""
        event_ref = self.db.collection('timeline_events').document()
        
        event = {
            'event_id': event_ref.id,
            'user_id': user_id,
            'event_type': record['record_type'],
            'date': record['date'],
            'title': self._generate_event_title(record),
            'description': "Medical Record Uploaded",
            'related_records': [record['record_id']],
            'created_at': datetime.now()
        }
        
        event_ref.set(event)

    def get_user_timeline(self, user_id: str):
        """Get all timeline events for a user, sorted by date"""
        events = self.db.collection('timeline_events')\
            .where('user_id', '==', user_id)\
            .order_by('date', direction=firestore.Query.DESCENDING)\
            .stream()
        
        return [event.to_dict() for event in events]

    def _generate_event_title(self, record: dict):
        """Generate a readable title for timeline"""
        type_map = {
            'lab_report': 'Lab Test Results',
            'prescription': 'New Prescription',
            'imaging': 'Imaging Study',
            'consultation': 'Doctor Visit'
        }
        return type_map.get(record['record_type'], 'Health Record')