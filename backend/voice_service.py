import google.generativeai as genai
from typing import List, Dict

class VoiceHealthAssistant:
    def __init__(self, api_key: str, db_service):
        genai.configure(api_key=api_key)
        # FIXED: Using the standard stable model name
        self.model = genai.GenerativeModel('gemini-flash-latest')
        self.db = db_service
        self.conversation_history = []
        
    def create_health_context(self, user_id: str) -> str:
        """Build context from user's health records"""
        # Get timeline events from Firestore
        timeline = self.db.get_user_timeline(user_id)
        
        # Take the 5 most recent events to keep context concise
        recent_records = timeline[:5]
        
        if not recent_records:
            return "Patient has no medical records on file yet."
            
        context = "Patient Health Summary (Recent Records):\n"
        for event in recent_records:
            # Handle cases where date might be a string or object
            date_str = str(event.get('date', 'Unknown Date'))
            context += f"- {date_str}: {event.get('title', 'Record')} - {event.get('description', '')}\n"
            
        return context

    def process_voice_query(self, user_id: str, user_message: str) -> str:
        """Process user voice query with health context"""
        
        # 1. Get user's health context from DB
        health_context = self.create_health_context(user_id)
        
        # 2. Build system prompt
        system_prompt = f"""
        You are a helpful and empathetic health assistant. 
        You have access to the patient's following medical history:
        
        {health_context}
        
        Guidelines:
        - Answer the user's question based on their history if relevant.
        - Be empathetic and clear.
        - Explain medical terms in simple language.
        - If asked about specific test results, reference the actual values from the history.
        - IMPORTANT: Never provide definitive diagnoses. Always advise seeing a doctor for medical advice.
        """
        
        # 3. Generate response using the Chat Session
        # We start a fresh chat each time to ensure context is injected correctly
        chat = self.model.start_chat(history=[])
        response = chat.send_message(system_prompt + "\n\nUser Question: " + user_message)
        
        return response.text