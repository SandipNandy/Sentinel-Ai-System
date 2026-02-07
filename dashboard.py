# dashboard.py - Main TPM Dashboard
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime

# Import our modules
from database import db
from ai_engine import analyzer


# In dashboard.py, replace the database import with:
import requests

# Example: Fetch platform health
response = requests.get("http://localhost:8000/health")
data = response.json()
platform_health = data["platform_health"]

# Page configuration
st.set_page_config(
    page_title="Sentinel-AI TPM Dashboard",
    page_icon="🔷",
    layout="wide"
)

# Custom CSS for better appearance
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #374151;
        margin-top: 1rem;
    }
    .metric-card {
        background-color: #F3F4F6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #3B82F6;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main dashboard function"""
    
    # Header
    st.markdown('<h1 class="main-header">🔷 Sentinel-AI TPM Dashboard</h1>', unsafe_allow_html=True)
    st.markdown("**Platform Health & Delivery Risk Intelligence**")
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to:",
        ["Dashboard", "Platform Health", "Program Risks", "Incident Analysis", "AI Insights"]
    )
    
    if page == "Dashboard":
        show_dashboard()
    elif page == "Platform Health":
        show_platform_health()
    elif page == "Program Risks":
        show_program_risks()
    elif page == "Incident Analysis":
        show_incident_analysis()
    elif page == "AI Insights":
        show_ai_insights()

def show_dashboard():
    """Main dashboard view"""
    
    # Get data
    platform_health = db.get_platform_health()
    services = db.services
    risks = db.get_program_risks()
    
    # Top metrics row
    st.markdown("## 📊 Executive Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Platform Health", f"{platform_health:.0f}%", "+2%")
    
    with col2:
        high_risks = sum(1 for r in risks if r["level"] == "High")
        st.metric("High Risk Programs", high_risks)
    
    with col3:
        total_incidents = len(db.incidents)
        st.metric("Recent Incidents", total_incidents)
    
    with col4:
        services_healthy = sum(1 for s in services if s["health"] > 90)
        st.metric("Healthy Services", f"{services_healthy}/{len(services)}")
    
    # Platform Health Gauge
    st.markdown("## 🏥 Platform Health Score")
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=platform_health,
        title={'text': "Overall Health"},
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 50], 'color': "red"},
                {'range': [50, 80], 'color': "yellow"},
                {'range': [80, 100], 'color': "green"}
            ]
        }
    ))
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Quick Actions
    st.markdown("## ⚡ Quick Actions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📋 Generate Weekly Report", type="primary"):
            with st.spinner("Generating report..."):
                platform_data = {
                    "health": platform_health,
                    "services": services,
                    "incidents": db.incidents[:3]  # Last 3 incidents
                }
                summary = analyzer.generate_exec_summary(platform_data)
                st.success("Report Generated!")
                st.info(summary)
    
    with col2:
        if st.button("🔍 Analyze Latest Incident"):
            if db.incidents:
                latest = db.incidents[0]
                analysis = analyzer.analyze_incident(latest)
                st.json(analysis)
            else:
                st.warning("No incidents found")

def show_platform_health():
    """Platform health details"""
    st.markdown("## 🏥 Platform Health Details")
    
    # Create service health table
    service_data = []
    for service in db.services:
        status = "✅ Healthy" if service["health"] > 90 else "⚠️ Degraded" if service["health"] > 80 else "🔴 Critical"
        
        service_data.append({
            "Service": service["name"],
            "Type": service["type"],
            "Health Score": service["health"],
            "Status": status
        })
    
    df = pd.DataFrame(service_data)
    st.dataframe(df, use_container_width=True)
    
    # Health bar chart
    st.markdown("### Service Health Comparison")
    
    fig = px.bar(
        df,
        x="Service",
        y="Health Score",
        color="Health Score",
        color_continuous_scale=["red", "yellow", "green"],
        title="Service Health Scores"
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_program_risks():
    """Program risk analysis"""
    st.markdown("## 🎯 Program Risk Analysis")
    
    risks = db.get_program_risks()
    
    if not risks:
        st.info("No program risks identified")
        return
    
    # Risk table
    risk_data = []
    for risk in risks:
        risk_data.append({
            "Program": risk["program"],
            "Risk Level": risk["level"],
            "Risk Score": risk["risk_score"],
            "Delivery Confidence": f"{risk['confidence']}%"
        })
    
    df = pd.DataFrame(risk_data)
    
    # Color coding
    def color_risk(val):
        if val == "High":
            return 'background-color: #FECACA; color: black'
        elif val == "Medium":
            return 'background-color: #FEF3C7; color: black'
        else:
            return 'background-color: #D1FAE5; color: black'
    
    styled_df = df.style.applymap(color_risk, subset=['Risk Level'])
    st.dataframe(styled_df, use_container_width=True)
    
    # Risk pie chart
    st.markdown("### Risk Distribution")
    
    risk_counts = df["Risk Level"].value_counts()
    fig = px.pie(
        values=risk_counts.values,
        names=risk_counts.index,
        color=risk_counts.index,
        color_discrete_map={
            "High": "red",
            "Medium": "yellow",
            "Low": "green"
        }
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_incident_analysis():
    """Incident analysis"""
    st.markdown("## 🚨 Incident Analysis")
    
    incidents = db.incidents
    
    if not incidents:
        st.success("🎉 No recent incidents!")
        return
    
    # Incident table
    incident_data = []
    for incident in incidents:
        incident_data.append({
            "ID": incident["id"],
            "Service": incident["service"],
            "Severity": incident["severity"],
            "Time": incident["time"],
            "Description": incident["description"]
        })
    
    df = pd.DataFrame(incident_data)
    st.dataframe(df, use_container_width=True)
    
    # AI Analysis Section
    st.markdown("### 🤖 AI-Powered Incident Analysis")
    
    selected_incident = st.selectbox(
        "Select an incident for AI analysis:",
        [f"{i['id']}: {i['service']} - {i['severity']}" for i in incidents]
    )
    
    if st.button("Analyze with AI", type="primary"):
        # Find selected incident
        incident_id = selected_incident.split(":")[0]
        incident = next(i for i in incidents if i["id"] == incident_id)
        
        with st.spinner("Analyzing business impact..."):
            analysis = analyzer.analyze_incident(incident)
            
            # Display results
            st.success("Analysis Complete!")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("##### 📋 Summary")
                st.info(analysis.get("summary", "No summary available"))
                
                st.markdown("##### 🎯 Affected Programs")
                programs = analysis.get("affected_programs", [])
                for program in programs:
                    st.write(f"- {program}")
            
            with col2:
                st.markdown("##### ⏱️ Timeline Impact")
                st.warning(analysis.get("timeline_impact", "Unknown"))
                
                st.markdown("##### ⚡ Recommended Action")
                st.success(analysis.get("recommended_action", "Monitor situation"))

def show_ai_insights():
    """AI insights page"""
    st.markdown("## 🤖 AI Insights Engine")
    
    st.markdown("""
    This section demonstrates AI capabilities for TPM work:
    
    1. **Incident → Business Impact Translation**
    2. **Risk Prediction & Analysis**
    3. **Executive Summary Generation**
    """)
    
    # Demo area
    st.markdown("### 🧪 Try It Yourself")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### Simulate an Incident")
        
        service = st.selectbox(
            "Service",
            ["auth-service", "payment-service", "inventory-service", "notification-service"]
        )
        
        severity = st.selectbox("Severity", ["SEV1", "SEV2", "SEV3"])
        
        description = st.text_area(
            "Description",
            "Latency spike and increased error rates"
        )
    
    with col2:
        st.markdown("##### AI Analysis Results")
        
        if st.button("Generate AI Analysis", type="primary"):
            incident_data = {
                "service": service,
                "severity": severity,
                "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "description": description
            }
            
            with st.spinner("AI analyzing..."):
                analysis = analyzer.analyze_incident(incident_data)
                
                # Display formatted results
                st.markdown("**Business Impact:**")
                st.write(analysis.get("summary", "No analysis"))
                
                st.markdown("**Affected Programs:**")
                for program in analysis.get("affected_programs", []):
                    st.write(f"- {program}")
    
    # Sample TPM Prompts
    st.markdown("### 📝 Sample TPM Prompts")
    
    prompts = [
        "Create an executive summary for this week's platform health",
        "Translate this technical incident into business impact",
        "Generate risk mitigation strategies for our Q4 launch",
        "Create talking points for a leadership update meeting"
    ]
    
    selected_prompt = st.selectbox("Select a prompt template:", prompts)
    
    if st.button("Run Selected Prompt"):
        with st.spinner("AI thinking..."):
            # This would call the AI with the selected prompt
            st.info(f"Running: {selected_prompt}")
            st.success("This would generate AI-powered insights in the full version!")

if __name__ == "__main__":
    main()