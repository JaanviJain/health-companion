from dotenv import load_dotenv
import os
import firebase_admin
from firebase_admin import credentials, firestore

# 1. Load env
load_dotenv()

# 2. Check if the file path is correct
cred_path = os.getenv("FIREBASE_CREDENTIALS_PATH")
print(f"Looking for credentials at: {cred_path}")

if not os.path.exists(cred_path):
    print("❌ ERROR: File not found! Check the name in your .env file")
else:
    print("✅ File found!")
    
    # 3. Try to connect
    try:
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        
        # 4. Try to write
        doc_ref = db.collection('test_collection').document('test_doc')
        doc_ref.set({
            'message': 'Hello from Python!',
            'timestamp': firestore.SERVER_TIMESTAMP
        })
        print("✅ SUCCESS! Data written to Firebase.")
        print("Go check your Firebase Console now!")
        
    except Exception as e:
        print(f"❌ CONNECTION ERROR: {e}")