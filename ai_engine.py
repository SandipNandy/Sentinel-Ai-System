
# ai_engine.py - Simple AI analysis for TPM context
import openai
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

class TPM_AIAnalyzer:
    """Simple AI analyzer for TPM insights"""
    
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        
        self.system_prompt = """You are a Principal Technical Program Manager (TPM) at a FAANG company.
        Your job is to analyze platform incidents and translate them into business impact.
        Focus on: program delays, revenue risk, and executive communication."""
    
    def analyze_incident(self, incident_data):
        """Analyze a single incident for business impact"""
        
        user_prompt = f"""Incident Details:
        Service: {incident_data['service']}
        Severity: {incident_data['severity']}
        Time: {incident_data['time']}
        Description: {incident_data['description']}
        
        As a TPM, provide:
        1. Business impact summary (one sentence)
        2. Which programs are affected
        3. Estimated timeline impact
        4. Recommended action for leadership
        
        Format as JSON with these keys: summary, affected_programs, timeline_impact, recommended_action"""
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Use gpt-4 if available
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=300
            )
            
            return json.loads(response.choices[0].message.content)
        except:
            # Fallback if API fails
            return {
                "summary": f"{incident_data['service']} incident may impact user experience",
                "affected_programs": ["All dependent programs"],
                "timeline_impact": "1-2 days delay",
                "recommended_action": "Monitor and prepare rollback plan"
            }
    
    def generate_exec_summary(self, platform_data):
        """Generate executive summary from platform data"""
        
        user_prompt = f"""Platform Status:
        Overall Health: {platform_data['health']}%
        Services: {len(platform_data['services'])}
        Recent Incidents: {len(platform_data['incidents'])}
        
        Generate a brief executive summary (3 bullet points) for leadership meeting."""
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.2,
                max_tokens=200
            )
            
            return response.choices[0].message.content
        except:
            return "Platform is stable with minor incidents. Monitor payment-service health."

# Create analyzer instance
analyzer = TPM_AIAnalyzer()
