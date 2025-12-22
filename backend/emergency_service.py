import qrcode
from io import BytesIO
import base64
import google.generativeai as genai
import json
import os

class EmergencyAccessService:
    def __init__(self, db_service, api_key: str):
        self.db = db_service
        # Connect to AI
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-flash-latest')

    def generate_emergency_profile(self, user_id: str):
        """Generate emergency profile by reading user's history"""
        # 1. Get the user's real timeline from Firebase
        timeline = self.db.get_user_timeline(user_id)
        
        # If they have no records yet, return safe defaults
        if not timeline:
            return {
                'blood_type': "Unknown",
                'allergies': ["None recorded"],
                'chronic_conditions': ["None recorded"],
                'current_medications': ["None recorded"],
                'emergency_contact': "Not Set"
            }

        # 2. Prepare the data for the AI to read
        # We take the last 15 records to get the most recent info
        records_text = "Patient History:\n"
        for event in timeline[:15]: 
            records_text += f"- Date: {event.get('date', 'N/A')}, Title: {event.get('title', '')}, Details: {event.get('description', '')}\n"

        # 3. Ask Gemini to extract critical info
        prompt = f"""
        You are an emergency medical data extractor. 
        Analyze the following patient history and extract the most critical emergency information.
        
        Return ONLY a valid JSON object with these exact keys:
        - "blood_type" (String. If not found, use "Unknown")
        - "allergies" (List of strings. If none found, use ["None Known"])
        - "chronic_conditions" (List of strings. If none found, use ["None Known"])
        - "current_medications" (List of strings. If none found, use ["None Known"])
        - "emergency_contact" (String. If not found, use "Not Set")

        Patient History:
        {records_text}
        """

        try:
            # Generate the analysis
            response = self.model.generate_content(prompt)
            
            # Clean the text to ensure it's pure JSON (remove ```json markers)
            clean_text = response.text.replace("```json", "").replace("```", "").strip()
            
            return json.loads(clean_text)
            
        except Exception as e:
            print(f"❌ AI Extraction Error: {e}")
            # Fallback if AI fails
            return {
                'blood_type': "Unknown",
                'allergies': ["Error retrieving data"],
                'chronic_conditions': ["Check full timeline"],
                'current_medications': ["Check full timeline"],
                'emergency_contact': "Not Set"
            }

    def generate_qr_code(self, user_id: str):
        """Generate QR code for emergency access"""
        emergency_url = f"[https://health-companion-app.com/emergency/](https://health-companion-app.com/emergency/){user_id}"
        
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(emergency_url)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        return img_str