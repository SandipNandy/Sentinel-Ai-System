# database.py - Simple in-memory database for the demo
import json
from datetime import datetime, timedelta
import random

class SimpleDatabase:
    """A simple database simulator for TPM data"""
    
    def __init__(self):
        self.services = [
            {"name": "auth-service", "type": "tier1", "health": 95},
            {"name": "payment-service", "type": "tier1", "health": 87},
            {"name": "inventory-service", "type": "tier2", "health": 92},
            {"name": "notification-service", "type": "tier3", "health": 98}
        ]
        
        self.programs = [
            {"id": "q4-launch", "name": "Q4 Platform Launch", "confidence": 85},
            {"id": "ai-migration", "name": "AI Migration", "confidence": 72},
            {"id": "mobile-app", "name": "Mobile App V2", "confidence": 90}
        ]
        
        self.incidents = self._generate_sample_incidents()
    
    def _generate_sample_incidents(self):
        """Generate sample incident data"""
        incidents = []
        severities = ["SEV1", "SEV2", "SEV3"]
        
        for i in range(5):
            days_ago = random.randint(1, 30)
            incident_time = datetime.now() - timedelta(days=days_ago)
            
            incidents.append({
                "id": f"INC-{1000 + i}",
                "service": random.choice(self.services)["name"],
                "severity": random.choice(severities),
                "time": incident_time.strftime("%Y-%m-%d %H:%M"),
                "description": f"Service degradation detected",
                "impact": f"Affects {random.choice(['checkout', 'login', 'search'])} flow"
            })
        
        return incidents
    
    def get_platform_health(self):
        """Calculate overall platform health"""
        total_health = sum(service["health"] for service in self.services)
        return total_health / len(self.services)
    
    def get_program_risks(self):
        """Get program risk data"""
        risks = []
        for program in self.programs:
            # Calculate risk score (100 - confidence)
            risk_score = 100 - program["confidence"]
            
            if risk_score > 30:
                level = "High"
            elif risk_score > 15:
                level = "Medium"
            else:
                level = "Low"
            
            risks.append({
                "program": program["name"],
                "risk_score": risk_score,
                "level": level,
                "confidence": program["confidence"]
            })
        
        return risks

# Create a global database instance
db = SimpleDatabase()