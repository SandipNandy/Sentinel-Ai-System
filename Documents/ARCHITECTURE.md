# System Architecture

## Overview
```mermaid
flowchart TB
    %% Layer 1: Presentation
    Dashboard[TPM Dashboard<br/>Streamlit Frontend] --> API[API Gateway<br/>FastAPI]
    
    %% Layer 2: API Services
    API --> Health[Health Service]
    API --> Services[Services Service]
    API --> Incidents[Incidents Service]
    API --> Programs[Programs Service]
    API --> AI[AI Service]
    API --> Reports[Reports Service]
    
    %% Layer 3: AI Engine
    AI --> LLM[LLM Integration<br/>OpenAI/Claude]
    AI --> Predictor[Risk Predictor]
    AI --> Translator[Business Translator]
    AI --> Generator[Report Generator]
    
    %% Layer 4: Data Processing
    LLM --> Pipeline[Signal Pipeline]
    Predictor --> Pipeline
    Translator --> Pipeline
    Generator --> Pipeline
    
    Pipeline --> Collector[Metric Collector]
    Pipeline --> Analyzer[Anomaly Analyzer]
    Pipeline --> Correlator[Correlation Engine]
    Pipeline --> Scorer[Health Scorer]
    
    %% Layer 5: Data Storage
    Collector --> Database[(PostgreSQL)]
    Analyzer --> Database
    Correlator --> Database
    Scorer --> Database
    
    %% External Systems
    Collector -.-> External[External Monitoring<br/>Datadog, Prometheus]
    Incidents -.-> PagerDuty[PagerDuty]
    Reports -.-> Notifier[Slack/Teams]
    
    %% Styling
    classDef presentation fill:#bbdefb,stroke:#0d47a1
    classDef api fill:#e1bee7,stroke:#4a148c
    classDef ai fill:#c8e6c9,stroke:#1b5e20
    classDef processing fill:#ffecb3,stroke:#ff6f00
    classDef storage fill:#f8bbd9,stroke:#880e4f
    classDef external fill:#d7ccc8,stroke:#3e2723
    
    class Dashboard presentation
    class API,Health,Services,Incidents,Programs,AI,Reports api
    class LLM,Predictor,Translator,Generator ai
    class Pipeline,Collector,Analyzer,Correlator,Scorer processing
    class Database storage
    class External,PagerDuty,Notifier external