"""
Sentinel-AI TPM Platform - REST API Server
Simple FastAPI server for the TPM intelligence platform
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import json
import random

# Initialize FastAPI app
app = FastAPI(
    title="Sentinel-AI TPM Platform API",
    description="AI-powered platform intelligence API for Technical Program Managers",
    version="1.0.0"
)

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class Incident(BaseModel):
    service: str
    severity: str
    description: str
    impact: str

class ServiceMetric(BaseModel):
    name: str
    health_score: float
    latency_ms: int
    error_rate: float

class ProgramRisk(BaseModel):
    program_name: str
    risk_score: int
    confidence: int
    status: str

# In-memory database (in production, use real database)
class TPMDatabase:
    def __init__(self):
        self.services = [
            {"id": 1, "name": "auth-service", "type": "tier1", "health": 95, "latency": 45, "error_rate": 0.1},
            {"id": 2, "name": "payment-service", "type": "tier1", "health": 87, "latency": 120, "error_rate": 0.5},
            {"id": 3, "name": "inventory-service", "type": "tier2", "health": 92, "latency": 65, "error_rate": 0.2},
            {"id": 4, "name": "notification-service", "type": "tier3", "health": 98, "latency": 30, "error_rate": 0.05},
            {"id": 5, "name": "search-service", "type": "tier2", "health": 89, "latency": 85, "error_rate": 0.3},
        ]
        
        self.programs = [
            {"id": "q4-launch", "name": "Q4 Platform Launch", "confidence": 85, "risk": "Medium", "owner": "Platform TPM"},
            {"id": "ai-migration", "name": "AI Infrastructure Migration", "confidence": 72, "risk": "High", "owner": "AI TPM"},
            {"id": "mobile-v2", "name": "Mobile App V2", "confidence": 90, "risk": "Low", "owner": "Mobile TPM"},
            {"id": "data-lake", "name": "Enterprise Data Lake", "confidence": 78, "risk": "Medium", "owner": "Data TPM"},
        ]
        
        self.incidents = self._generate_sample_incidents()
        self.executive_reports = self._generate_sample_reports()
    
    def _generate_sample_incidents(self):
        incidents = []
        severities = ["SEV1", "SEV2", "SEV3"]
        services = ["auth-service", "payment-service", "inventory-service", "notification-service"]
        
        for i in range(10):
            days_ago = random.randint(1, 30)
            incident_time = datetime.now() - timedelta(days=days_ago, hours=random.randint(1, 23))
            
            incidents.append({
                "id": f"INC-{1000 + i}",
                "service": random.choice(services),
                "severity": random.choice(severities),
                "timestamp": incident_time.isoformat(),
                "description": random.choice([
                    "Latency spike above threshold",
                    "Increased error rates",
                    "Service timeout failures",
                    "Database connection pool exhausted",
                    "Cache miss storm detected"
                ]),
                "status": random.choice(["resolved", "investigating", "mitigated"]),
                "impact": random.choice([
                    "Checkout flow degraded",
                    "User authentication delays",
                    "Search functionality impacted",
                    "Notifications backlogged"
                ]),
                "assigned_to": f"Engineer-{random.randint(1, 5)}"
            })
        
        # Sort by timestamp (most recent first)
        return sorted(incidents, key=lambda x: x["timestamp"], reverse=True)
    
    def _generate_sample_reports(self):
        reports = []
        
        for i in range(3):
            reports.append({
                "id": f"REPORT-{i+1}",
                "title": f"Q{random.randint(1,4)} {random.randint(2023,2024)} Platform Health Report",
                "type": random.choice(["Weekly", "Monthly", "Quarterly"]),
                "generated_at": (datetime.now() - timedelta(days=i*7)).isoformat(),
                "summary": f"Platform health remains stable with {random.randint(1,5)} critical incidents this period.",
                "key_metrics": {
                    "platform_health": random.randint(85, 95),
                    "incident_count": random.randint(3, 8),
                    "mttr_hours": random.uniform(1.5, 4.0),
                    "sla_compliance": random.randint(95, 100)
                }
            })
        
        return reports
    
    def calculate_platform_health(self):
        """Calculate overall platform health score"""
        if not self.services:
            return 100.0
        
        total_health = sum(service["health"] for service in self.services)
        return round(total_health / len(self.services), 1)
    
    def get_program_risks(self):
        """Get program risk analysis"""
        risks = []
        for program in self.programs:
            confidence = program["confidence"]
            risk_score = 100 - confidence
            
            # Determine risk level
            if risk_score > 40:
                level = "Critical"
                color = "#EF4444"  # Red
            elif risk_score > 25:
                level = "High"
                color = "#F59E0B"  # Yellow
            elif risk_score > 15:
                level = "Medium"
                color = "#3B82F6"  # Blue
            else:
                level = "Low"
                color = "#10B981"  # Green
            
            risks.append({
                "program_id": program["id"],
                "program_name": program["name"],
                "confidence_score": confidence,
                "risk_score": risk_score,
                "risk_level": level,
                "risk_color": color,
                "owner": program["owner"],
                "status": program["risk"]
            })
        
        return risks

# Initialize database
db = TPMDatabase()

# AI Analysis Simulation (in production, connect to OpenAI API)
class TPM_AIAnalyzer:
    """Simulated AI analyzer for demo purposes"""
    
    def analyze_incident(self, incident_data: Dict) -> Dict:
        """Simulate AI analysis of incident"""
        
        # Map severity to business impact
        severity_impact = {
            "SEV1": {"revenue_risk": "High", "delay_days": "3-7", "escalation": "Immediate exec alert"},
            "SEV2": {"revenue_risk": "Medium", "delay_days": "1-3", "escalation": "Team lead review"},
            "SEV3": {"revenue_risk": "Low", "delay_days": "0-1", "escalation": "Standard process"}
        }
        
        impact = severity_impact.get(incident_data["severity"], {"revenue_risk": "Unknown", "delay_days": "Unknown", "escalation": "Monitor"})
        
        # Generate business impact summary
        service_impacts = {
            "auth-service": ["User signup", "Authentication", "All programs"],
            "payment-service": ["Checkout", "Revenue", "E-commerce programs"],
            "inventory-service": ["Product catalog", "Order management", "Retail programs"],
            "notification-service": ["Alerts", "User engagement", "Mobile programs"]
        }
        
        affected_programs = service_impacts.get(incident_data["service"], ["General platform"])
        
        return {
            "incident_id": incident_data["id"],
            "business_impact_summary": f"{incident_data['service']} incident may impact {', '.join(affected_programs[:2])}",
            "affected_programs": affected_programs,
            "revenue_risk": impact["revenue_risk"],
            "estimated_delay_days": impact["delay_days"],
            "escalation_recommendation": impact["escalation"],
            "mitigation_suggestions": [
                "Implement circuit breaker pattern",
                "Increase monitoring frequency",
                "Prepare rollback plan"
            ],
            "communication_templates": {
                "engineer": f"Fix {incident_data['service']} {incident_data['description'].lower()}",
                "manager": f"{incident_data['service']} degraded, working on fix",
                "executive": f"Temporary {incident_data['service']} issue, no customer impact expected"
            }
        }
    
    def generate_executive_summary(self) -> Dict:
        """Generate executive summary of platform health"""
        platform_health = db.calculate_platform_health()
        
        # Count incidents by severity
        sev1_count = sum(1 for i in db.incidents if i["severity"] == "SEV1")
        sev2_count = sum(1 for i in db.incidents if i["severity"] == "SEV2")
        
        # Get high risk programs
        high_risk_programs = [p for p in db.get_program_risks() if p["risk_level"] in ["High", "Critical"]]
        
        return {
            "timestamp": datetime.now().isoformat(),
            "platform_health_score": platform_health,
            "platform_status": "Stable" if platform_health > 90 else "Degraded" if platform_health > 80 else "Critical",
            "incident_summary": {
                "total": len(db.incidents),
                "sev1": sev1_count,
                "sev2": sev2_count,
                "sev3": len(db.incidents) - sev1_count - sev2_count
            },
            "high_risk_programs": [
                {"name": p["program_name"], "risk": p["risk_level"]}
                for p in high_risk_programs[:3]  # Top 3
            ],
            "key_insights": [
                f"Platform health at {platform_health}% - within target range" if platform_health > 90 else f"Platform health at {platform_health}% - needs attention",
                f"{len(high_risk_programs)} programs with high/critical risk",
                f"{sev1_count + sev2_count} significant incidents this month"
            ],
            "recommendations": [
                "Review payment-service health (currently at 87%)",
                "Schedule risk review for high-risk programs",
                "Implement additional monitoring for auth-service"
            ]
        }

# Initialize AI analyzer
ai_analyzer = TPM_AIAnalyzer()

# API Endpoints
@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "name": "Sentinel-AI TPM Platform API",
        "version": "1.0.0",
        "status": "operational",
        "description": "AI-powered platform intelligence for Technical Program Managers",
        "endpoints": {
            "health": "/health - Platform health status",
            "services": "/services - List all services",
            "incidents": "/incidents - Get recent incidents",
            "programs": "/programs/risks - Get program risk analysis",
            "ai": {
                "analyze_incident": "/ai/incident/{incident_id} - AI analysis of incident",
                "executive_summary": "/ai/executive-summary - Generate executive summary"
            }
        }
    }

@app.get("/health")
async def get_platform_health():
    """Get overall platform health status"""
    return {
        "timestamp": datetime.now().isoformat(),
        "platform_health": db.calculate_platform_health(),
        "status": "healthy" if db.calculate_platform_health() > 90 else "degraded" if db.calculate_platform_health() > 80 else "critical",
        "services_healthy": sum(1 for s in db.services if s["health"] > 90),
        "services_total": len(db.services)
    }

@app.get("/services")
async def get_services():
    """Get all platform services with health metrics"""
    return {
        "timestamp": datetime.now().isoformat(),
        "services": db.services,
        "count": len(db.services)
    }

@app.get("/services/{service_name}")
async def get_service_details(service_name: str):
    """Get detailed metrics for a specific service"""
    service = next((s for s in db.services if s["name"] == service_name), None)
    
    if not service:
        raise HTTPException(status_code=404, detail=f"Service '{service_name}' not found")
    
    # Get recent incidents for this service
    service_incidents = [i for i in db.incidents if i["service"] == service_name]
    
    return {
        "service": service,
        "recent_incidents": service_incidents[:5],  # Last 5 incidents
        "incident_count": len(service_incidents),
        "health_trend": "improving" if service["health"] > 90 else "stable" if service["health"] > 85 else "declining"
    }

@app.get("/incidents")
async def get_incidents(limit: Optional[int] = 10, severity: Optional[str] = None):
    """Get recent incidents"""
    incidents = db.incidents
    
    # Filter by severity if provided
    if severity:
        incidents = [i for i in incidents if i["severity"] == severity.upper()]
    
    # Apply limit
    incidents = incidents[:limit]
    
    return {
        "timestamp": datetime.now().isoformat(),
        "incidents": incidents,
        "count": len(incidents),
        "by_severity": {
            "SEV1": sum(1 for i in db.incidents if i["severity"] == "SEV1"),
            "SEV2": sum(1 for i in db.incidents if i["severity"] == "SEV2"),
            "SEV3": sum(1 for i in db.incidents if i["severity"] == "SEV3")
        }
    }

@app.get("/incidents/{incident_id}")
async def get_incident_details(incident_id: str):
    """Get details for a specific incident"""
    incident = next((i for i in db.incidents if i["id"] == incident_id), None)
    
    if not incident:
        raise HTTPException(status_code=404, detail=f"Incident '{incident_id}' not found")
    
    return {
        "incident": incident,
        "similar_incidents": [
            i for i in db.incidents 
            if i["service"] == incident["service"] and i["id"] != incident_id
        ][:3]  # Get 3 similar incidents
    }

@app.post("/incidents")
async def create_incident(incident: Incident):
    """Create a new incident (simulated)"""
    new_incident = {
        "id": f"INC-{1000 + len(db.incidents)}",
        "service": incident.service,
        "severity": incident.severity,
        "timestamp": datetime.now().isoformat(),
        "description": incident.description,
        "impact": incident.impact,
        "status": "new",
        "assigned_to": "Unassigned"
    }
    
    db.incidents.insert(0, new_incident)  # Add to beginning of list
    
    # Update service health based on incident severity
    for service in db.services:
        if service["name"] == incident.service:
            # Reduce health based on severity
            health_reduction = {
                "SEV1": 15,
                "SEV2": 8,
                "SEV3": 3
            }.get(incident.severity, 5)
            
            service["health"] = max(50, service["health"] - health_reduction)
            break
    
    return {
        "message": "Incident created successfully",
        "incident": new_incident,
        "incident_id": new_incident["id"]
    }

@app.put("/incidents/{incident_id}/resolve")
async def resolve_incident(incident_id: str):
    """Mark an incident as resolved"""
    incident = next((i for i in db.incidents if i["id"] == incident_id), None)
    
    if not incident:
        raise HTTPException(status_code=404, detail=f"Incident '{incident_id}' not found")
    
    incident["status"] = "resolved"
    incident["resolved_at"] = datetime.now().isoformat()
    
    # Improve service health after resolution
    for service in db.services:
        if service["name"] == incident["service"]:
            service["health"] = min(100, service["health"] + 5)  # Small health improvement
            break
    
    return {
        "message": f"Incident {incident_id} marked as resolved",
        "incident": incident
    }

@app.get("/programs/risks")
async def get_program_risks():
    """Get program risk analysis"""
    return {
        "timestamp": datetime.now().isoformat(),
        "program_risks": db.get_program_risks(),
        "high_risk_count": sum(1 for p in db.get_program_risks() if p["risk_level"] in ["High", "Critical"]),
        "overall_confidence": round(sum(p["confidence_score"] for p in db.get_program_risks()) / len(db.get_program_risks()), 1)
    }

@app.get("/programs/{program_id}")
async def get_program_details(program_id: str):
    """Get detailed information about a specific program"""
    program = next((p for p in db.programs if p["id"] == program_id), None)
    
    if not program:
        raise HTTPException(status_code=404, detail=f"Program '{program_id}' not found")
    
    # Find related incidents (based on service-program mapping)
    service_to_program = {
        "auth-service": ["q4-launch", "ai-migration", "mobile-v2"],
        "payment-service": ["q4-launch"],
        "inventory-service": ["q4-launch", "data-lake"],
        "notification-service": ["mobile-v2"],
        "search-service": ["q4-launch", "data-lake"]
    }
    
    related_services = [service for service, programs in service_to_program.items() if program_id in programs]
    related_incidents = [i for i in db.incidents if i["service"] in related_services]
    
    return {
        "program": program,
        "related_services": related_services,
        "recent_incidents": related_incidents[:5],
        "service_dependencies": len(related_services),
        "incident_impact_score": min(100, len(related_incidents) * 10)  # Simple impact score
    }

@app.get("/reports")
async def get_reports(report_type: Optional[str] = None):
    """Get executive reports"""
    reports = db.executive_reports
    
    if report_type:
        reports = [r for r in reports if r["type"].lower() == report_type.lower()]
    
    return {
        "reports": reports,
        "count": len(reports)
    }

@app.post("/reports/generate")
async def generate_report(title: str, report_type: str = "Monthly"):
    """Generate a new executive report (simulated)"""
    new_report = {
        "id": f"REPORT-{len(db.executive_reports) + 1}",
        "title": title,
        "type": report_type,
        "generated_at": datetime.now().isoformat(),
        "summary": f"{report_type} platform health report generated by Sentinel-AI",
        "key_metrics": {
            "platform_health": db.calculate_platform_health(),
            "incident_count": len([i for i in db.incidents if datetime.fromisoformat(i["timestamp"]).month == datetime.now().month]),
            "mttr_hours": random.uniform(1.5, 3.5),
            "sla_compliance": random.randint(97, 100),
            "high_risk_programs": sum(1 for p in db.get_program_risks() if p["risk_level"] in ["High", "Critical"])
        }
    }
    
    db.executive_reports.insert(0, new_report)
    
    return {
        "message": "Report generated successfully",
        "report": new_report
    }

# AI Analysis Endpoints
@app.get("/ai/incident/{incident_id}")
async def analyze_incident_with_ai(incident_id: str):
    """Get AI-powered analysis of an incident"""
    incident = next((i for i in db.incidents if i["id"] == incident_id), None)
    
    if not incident:
        raise HTTPException(status_code=404, detail=f"Incident '{incident_id}' not found")
    
    analysis = ai_analyzer.analyze_incident(incident)
    
    return {
        "incident": incident,
        "ai_analysis": analysis,
        "analysis_timestamp": datetime.now().isoformat()
    }

@app.get("/ai/executive-summary")
async def get_executive_summary():
    """Get AI-generated executive summary"""
    summary = ai_analyzer.generate_executive_summary()
    
    return {
        "summary": summary,
        "generated_at": datetime.now().isoformat(),
        "source": "Sentinel-AI TPM Intelligence"
    }

@app.get("/ai/risk-prediction")
async def predict_risks(lookahead_days: int = 30):
    """Predict risks for the next N days"""
    
    # Simple prediction based on historical data
    recent_incidents = [i for i in db.incidents 
                       if datetime.fromisoformat(i["timestamp"]) > datetime.now() - timedelta(days=30)]
    
    incidents_per_day = len(recent_incidents) / 30
    predicted_incidents = int(incidents_per_day * lookahead_days)
    
    # Identify services at risk
    service_incident_counts = {}
    for incident in recent_incidents:
        service_incident_counts[incident["service"]] = service_incident_counts.get(incident["service"], 0) + 1
    
    high_risk_services = [
        service for service, count in service_incident_counts.items()
        if count > 2  # More than 2 incidents in last 30 days
    ]
    
    return {
        "prediction_period_days": lookahead_days,
        "predicted_incidents": predicted_incidents,
        "predicted_sev1_incidents": max(0, int(predicted_incidents * 0.1)),  # Assume 10% are SEV1
        "high_risk_services": high_risk_services,
        "confidence_score": 0.75,  # Prediction confidence
        "recommendations": [
            f"Increase monitoring for: {', '.join(high_risk_services[:3])}" if high_risk_services else "No high-risk services identified",
            f"Expected {predicted_incidents} incidents in next {lookahead_days} days",
            "Schedule proactive maintenance for high-risk services"
        ]
    }

# Real-time Monitoring Endpoint
@app.get("/monitoring/realtime")
async def get_realtime_metrics():
    """Get real-time platform metrics (simulated)"""
    
    # Generate simulated real-time metrics
    realtime_metrics = []
    for service in db.services:
        # Add some random variation to simulate real-time data
        current_health = max(50, min(100, service["health"] + random.uniform(-5, 5)))
        current_latency = max(10, service["latency"] + random.randint(-20, 20))
        current_errors = max(0, service["error_rate"] + random.uniform(-0.1, 0.1))
        
        realtime_metrics.append({
            "service": service["name"],
            "health": round(current_health, 1),
            "latency_ms": current_latency,
            "error_rate": round(current_errors, 3),
            "status": "healthy" if current_health > 90 else "degraded" if current_health > 80 else "critical",
            "last_updated": datetime.now().isoformat()
        })
    
    # Calculate overall platform health
    overall_health = round(sum(m["health"] for m in realtime_metrics) / len(realtime_metrics), 1)
    
    return {
        "timestamp": datetime.now().isoformat(),
        "platform_health": overall_health,
        "metrics": realtime_metrics,
        "alerts": [
            {
                "service": "payment-service",
                "alert": "Latency above threshold",
                "severity": "warning"
            }
        ] if overall_health < 90 else []
    }

# Health Check Endpoint
@app.get("/health/check")
async def health_check():
    """Comprehensive health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "components": {
            "api": "operational",
            "database": "operational",
            "ai_engine": "operational"
        },
        "version": "1.0.0",
        "uptime": "0 days 0 hours 0 minutes"  # In production, calculate actual uptime
    }

# Run the server
if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting Sentinel-AI TPM Platform API...")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🌐 Root endpoint: http://localhost:8000/")
    
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Auto-reload on code changes
    )
