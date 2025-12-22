import google.generativeai as genai
import os
from typing import List, Dict, Any

class BaseAgent:
    def __init__(self, api_key: str, system_prompt: str):
        genai.configure(api_key=api_key)
        # FIXED: Using the model we know works for your account
        self.model = genai.GenerativeModel('gemini-flash-latest')
        self.system_prompt = system_prompt

    def process(self, query: str, context: dict) -> str:
        prompt = f"{self.system_prompt}\n\nContext: {context}\n\nQuery: {query}"
        response = self.model.generate_content(prompt)
        return response.text

class LabAnalysisAgent(BaseAgent):
    def __init__(self, api_key: str):
        system_prompt = """
        You are a lab analysis expert. Analyze lab results and explain them clearly.
        - Identify abnormal values
        - Explain what tests mean
        - Suggest follow-up if needed
        - Use simple language
        """
        super().__init__(api_key, system_prompt)

class TriageAgent(BaseAgent):
    def __init__(self, api_key: str):
        system_prompt = """
        You are a medical triage expert. Assess urgency of symptoms.
        
        Classify as:
        - EMERGENCY: Life-threatening, go to ER now
        - URGENT: See doctor within 24 hours
        - ROUTINE: Schedule regular appointment
        - SELF-CARE: Can manage at home
        
        Ask clarifying questions if needed.
        """
        super().__init__(api_key, system_prompt)

    def assess_urgency(self, symptoms: List[str], context: dict) -> Dict:
        query = f"Symptoms: {', '.join(symptoms)}"
        response = self.process(query, context)
        
        # Parse urgency level based on keywords in the AI response
        response_upper = response.upper()
        if "EMERGENCY" in response_upper:
            urgency = "emergency"
            score = 10
        elif "URGENT" in response_upper:
            urgency = "urgent"
            score = 7
        elif "ROUTINE" in response_upper:
            urgency = "routine"
            score = 4
        else:
            urgency = "self-care"
            score = 2
            
        return {
            "urgency": urgency,
            "score": score,
            "explanation": response,
            "recommended_action": self._get_recommended_action(urgency)
        }

    def _get_recommended_action(self, urgency: str) -> str:
        actions = {
            "emergency": "Visit emergency room immediately",
            "urgent": "Schedule doctor appointment within 24 hours",
            "routine": "Schedule regular appointment",
            "self-care": "Monitor symptoms and self-care"
        }
        return actions.get(urgency, "Consult healthcare provider")

class InsuranceAgent(BaseAgent):
    def __init__(self, api_key: str):
        system_prompt = """
        You are an insurance guidance expert. Help users understand:
        - Coverage details
        - In-network providers
        - Expected costs
        - Claims process
        
        Be clear about what is/isn't covered.
        """
        super().__init__(api_key, system_prompt)

class DoctorCoordinationAgent(BaseAgent):
    def __init__(self, api_key: str):
        system_prompt = """
        You are a healthcare coordination expert. Help with:
        - Finding appropriate specialists
        - Scheduling appointments
        - Preparing for visits
        - Managing referrals
        """
        super().__init__(api_key, system_prompt)

class AgentOrchestrator:
    def __init__(self, api_key: str):
        self.lab_agent = LabAnalysisAgent(api_key)
        self.triage_agent = TriageAgent(api_key)
        self.insurance_agent = InsuranceAgent(api_key)
        self.doctor_agent = DoctorCoordinationAgent(api_key)
        # Fallback to general lab agent for generic queries
        self.general_agent = LabAnalysisAgent(api_key) 

    def route_query(self, query: str, context: dict) -> str:
        """Determine which agent should handle the query"""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['lab', 'test', 'result', 'blood work', 'report']):
            print("🤖 Routing to: Lab Agent")
            return self.lab_agent.process(query, context)
            
        elif any(word in query_lower for word in ['pain', 'symptom', 'feeling', 'hurts', 'sick', 'emergency']):
            print("🤖 Routing to: Triage Agent")
            symptoms = [query] 
            triage_result = self.triage_agent.assess_urgency(symptoms, context)
            return f"{triage_result['explanation']}\n\nReccomendation: {triage_result['recommended_action']}"
            
        elif any(word in query_lower for word in ['insurance', 'coverage', 'cost', 'claim', 'pay']):
            print("🤖 Routing to: Insurance Agent")
            return self.insurance_agent.process(query, context)
            
        elif any(word in query_lower for word in ['doctor', 'appointment', 'specialist', 'schedule']):
            print("🤖 Routing to: Doctor Agent")
            return self.doctor_agent.process(query, context)
            
        else:
            print("🤖 Routing to: General/Lab Agent (Default)")
            return self.general_agent.process(query, context)