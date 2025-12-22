from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse  # <--- NEW IMPORT FOR PDF
from pydantic import BaseModel
import os
import shutil
from dotenv import load_dotenv

# Import ALL services
from ocr_service import MedicalOCR
from db_service import DatabaseService
from agents import AgentOrchestrator
from gmail_service import GmailHealthIntegration
from emergency_service import EmergencyAccessService
from pdf_generator import HealthReportPDF  # <--- NEW SERVICE IMPORT

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- INITIALIZE SERVICES ---
db = DatabaseService(credentials_path=os.getenv("FIREBASE_CREDENTIALS_PATH"))
ocr = MedicalOCR(gemini_api_key=os.getenv("GOOGLE_API_KEY"))
orchestrator = AgentOrchestrator(api_key=os.getenv("GOOGLE_API_KEY"))

# Note: We added api_key here in the previous step for the Emergency AI features
emergency_service = EmergencyAccessService(db, api_key=os.getenv("GOOGLE_API_KEY"))

# --- ENDPOINTS ---

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/upload-document")
async def upload_document(file: UploadFile = File(...), user_id: str = "demo_user"):
    os.makedirs("temp", exist_ok=True)
    temp_path = f"temp/{file.filename}"
    
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        result = ocr.process_document(temp_path)
        record_id = db.save_health_record(user_id, result)
        return {"status": "success", "record_id": record_id, "data": result}
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

@app.get("/timeline/{user_id}")
async def get_timeline(user_id: str):
    events = db.get_user_timeline(user_id)
    return {"events": events}

class ChatRequest(BaseModel):
    user_id: str
    message: str

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    timeline = db.get_user_timeline(request.user_id)
    context = {"user_id": request.user_id, "recent_history": timeline[:5]}
    response_text = orchestrator.route_query(request.message, context)
    return {"response": response_text}

@app.post("/sync-gmail/{user_id}")
async def sync_gmail(user_id: str):
    gmail = GmailHealthIntegration(credentials_path="credentials.json")
    try:
        gmail.authenticate()
        messages = gmail.get_health_emails()
        processed_count = 0
        os.makedirs("temp", exist_ok=True)
        
        for msg in messages:
            email_content = gmail.extract_email_content(msg['id'])
            
            if email_content and email_content['attachments']:
                for attachment in email_content['attachments']:
                    temp_path = f"temp/{attachment['filename']}"
                    with open(temp_path, 'wb') as f:
                        f.write(attachment['data'])
                    
                    try:
                        result = ocr.process_document(temp_path)
                        db.save_health_record(user_id, result)
                        processed_count += 1
                    finally:
                        if os.path.exists(temp_path):
                            os.remove(temp_path)
                            
        return {"status": "success", "processed_count": processed_count}
        
    except Exception as e:
        return {"status": "error", "message": str(e)}

# --- EMERGENCY ENDPOINTS ---
@app.get("/emergency-profile/{user_id}")
async def get_emergency_profile(user_id: str):
    return emergency_service.generate_emergency_profile(user_id)

@app.get("/emergency-qr/{user_id}")
async def get_emergency_qr(user_id: str):
    qr_code = emergency_service.generate_qr_code(user_id)
    return {"qr_code": qr_code}

# --- NEW PDF REPORT ENDPOINT ---
@app.get("/generate-report/{user_id}")
async def generate_pdf_report(user_id: str):
    """Generate and download a PDF report"""
    # We initialize it here to ensure it uses the latest DB data
    pdf_generator = HealthReportPDF(db, api_key=os.getenv("GOOGLE_API_KEY"))
    pdf_buffer = pdf_generator.generate_complete_report(user_id)
    
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=health_report_{user_id}.pdf"}
    )