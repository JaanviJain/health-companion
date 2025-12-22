from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import inch
from datetime import datetime
import io
import google.generativeai as genai

class HealthReportPDF:
    def __init__(self, db_service, api_key):
        self.db = db_service
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-flash-latest')

    def generate_complete_report(self, user_id: str):
        """Generate comprehensive health report PDF"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        # 1. Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2563eb'),
            spaceAfter=30,
            alignment=1 # Center
        )
        story.append(Paragraph("Patient Health Summary", title_style))
        story.append(Paragraph(f"Generated on: {datetime.now().strftime('%B %d, %Y')}", styles['Normal']))
        story.append(Spacer(1, 20))
        
        # 2. AI Executive Summary
        story.append(Paragraph("Executive Summary (AI Generated)", styles['Heading2']))
        summary_text = self._generate_ai_summary(user_id)
        story.append(Paragraph(summary_text, styles['Normal']))
        story.append(Spacer(1, 20))
        
        # 3. Timeline Table
        story.append(Paragraph("Medical Timeline", styles['Heading2']))
        timeline_table = self._get_timeline_table(user_id)
        story.append(timeline_table)
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer

    def _generate_ai_summary(self, user_id: str):
        """Ask Gemini to summarize the patient history"""
        timeline = self.db.get_user_timeline(user_id)
        
        if not timeline:
            return "No records found to summarize."

        # Create a text version of history for the AI
        history_text = ""
        for event in timeline[:10]: # Analyze last 10 events
            history_text += f"- {event.get('date', 'N/A')}: {event.get('title', 'Event')} ({event.get('description', '')})\n"

        prompt = f"""
        Write a professional 1-paragraph medical summary for a doctor based on this patient history. 
        Focus on chronic conditions and recent major events.
        
        Patient History:
        {history_text}
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except:
            return "Summary currently unavailable."

    def _get_timeline_table(self, user_id: str):
        timeline = self.db.get_user_timeline(user_id)
        
        # Table Header
        data = [['Date', 'Type', 'Description']]
        
        # Table Rows
        for event in timeline[:20]:  # Limit to 20 rows for space
            # Wrap long text
            desc = event.get('description', '')
            if len(desc) > 60:
                desc = desc[:60] + "..."
                
            data.append([
                str(event.get('date', 'N/A')),
                event.get('event_type', 'General').replace('_', ' ').title(),
                desc
            ])
            
        # Styling
        table = Table(data, colWidths=[1.5*inch, 1.5*inch, 4*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563eb')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        return table