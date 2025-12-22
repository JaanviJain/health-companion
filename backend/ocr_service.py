import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import google.generativeai as genai
import re
import os
from typing import Dict, List

# WINDOWS CONFIGURATION: point to where you installed Tesseract
# If you didn't change the path during install, this is the default:
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class MedicalOCR:
    def __init__(self, gemini_api_key: str):
        genai.configure(api_key=gemini_api_key)
        self.model = genai.GenerativeModel('gemini-flash-latest')

    def extract_text_from_image(self, image_path: str) -> str:
        """Extract text using Tesseract"""
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Convert PDF to images and extract text"""
        # Note: On Windows, this requires Poppler to be installed and in PATH.
        # For now, we will wrap this in a try-catch or assume image uploads.
        try:
            images = convert_from_path(pdf_path)
            full_text = ""
            for image in images:
                text = pytesseract.image_to_string(image)
                full_text += text + "\n"
            return full_text
        except Exception as e:
            return f"Error reading PDF (Do you have Poppler installed?): {str(e)}"

    def structure_medical_data(self, raw_text: str) -> Dict:
        """Use Gemini to structure the extracted text"""
        prompt = f"""
        You are a medical data extraction expert. Extract structured information from this medical report.
        
        Raw text:
        {raw_text}
        
        Extract and return JSON with:
        - patient_name
        - date (ISO format)
        - report_type (lab_report, prescription, imaging, consultation_note)
        - tests (list of: name, value, unit, reference_range, status)
        - medications (list of: name, dosage, frequency, duration)
        - diagnoses (list)
        - doctor_name
        - hospital_name
        
        Return ONLY valid JSON, no explanation.
        """
        
        response = self.model.generate_content(prompt)
        # Clean up code blocks if Gemini returns markdown
        text = response.text.replace('```json', '').replace('```', '')
        return text

    def process_document(self, file_path: str) -> Dict:
        """Main processing pipeline"""
        # Extract text
        if file_path.endswith('.pdf'):
            raw_text = self.extract_text_from_pdf(file_path)
        else:
            raw_text = self.extract_text_from_image(file_path)
        
        # Structure with Gemini
        structured_data = self.structure_medical_data(raw_text)
        
        return {
            "raw_text": raw_text,
            "structured_data": structured_data
        }