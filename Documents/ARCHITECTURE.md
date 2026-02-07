# System Architecture

## Overview
```mermaid
graph TB
    %% Presentation Layer
    subgraph "Presentation Layer - User Interface"
        direction TB
        UI[TPM Dashboard]
        UI_Comp1[Streamlit Framework]
        UI_Comp2[Plotly/Altair Visualizations]
        UI_Comp3[WebSocket Connections]
        UI_Comp4[Responsive Design]
        
        UI --> UI_Comp1
        UI --> UI_Comp2
        UI --> UI_Comp3
        UI --> UI_Comp4
    end
    
    %% API Layer
    subgraph "API Layer - Business Logic"
        direction TB
        API[FastAPI Application]
        API_Comp1[RESTful Endpoints]
        API_Comp2[Pydantic Schemas]
        API_Comp3[Middleware & CORS]
        API_Comp4[Authentication]
        
        API --> API_Comp1
        API --> API_Comp2
        API --> API_Comp3
        API --> API_Comp4
        
        %% API Endpoints
        subgraph "Key Endpoints"
            EP1[GET /health]
            EP2[GET /services]
            EP3[GET /incidents]
            EP4[POST /incidents]
            EP5[GET /programs/risks]
            EP6[GET /ai/analysis]
            EP7[GET /reports]
        end
        
        API_Comp1 --> EP1
        API_Comp1 --> EP2
        API_Comp1 --> EP3
        API_Comp1 --> EP4
        API_Comp1 --> EP5
        API_Comp1 --> EP6
        API_Comp1 --> EP7
    end
    
    %% AI Layer
    subgraph "AI Intelligence Layer"
        direction TB
        AI[AI Engine]
        AI_Comp1[OpenAI/Claude Integration]
        AI_Comp2[LangChain Framework]
        AI_Comp3[Prompt Engineering]
        AI_Comp4[Model Management]
        
        AI --> AI_Comp1
        AI --> AI_Comp2
        AI --> AI_Comp3
        AI --> AI_Comp4
        
        %% AI Capabilities
        subgraph "AI Capabilities"
            AI_Cap1[Incident Analysis]
            AI_Cap2[Risk Prediction]
            AI_Cap3[Report Generation]
            AI_Cap4[Business Translation]
        end
        
        AI --> AI_Cap1
        AI --> AI_Cap2
        AI --> AI_Cap3
        AI --> AI_Cap4
    end
    
    %% Data Processing Layer
    subgraph "Data Processing Layer"
        direction TB
        DP[Signal Pipeline]
        DP_Comp1[Python + Pandas]
        DP_Comp2[NumPy + Scikit-learn]
        DP_Comp3[Real-time Processing]
        DP_Comp4[Batch Processing]
        
        DP --> DP_Comp1
        DP --> DP_Comp2
        DP --> DP_Comp3
        DP --> DP_Comp4
        
        %% Processing Steps
        subgraph "Processing Steps"
            PS1[Metric Collection]
            PS2[Anomaly Detection]
            PS3[Correlation Engine]
            PS4[Health Scoring]
            PS5[Incident Generation]
        end
        
        DP --> PS1
        DP --> PS2
        DP --> PS3
        DP --> PS4
        DP --> PS5
    end
    
    %% Data Storage Layer
    subgraph "Data Storage Layer"
        direction TB
        DB[PostgreSQL Database]
        DB_Comp1[SQLAlchemy ORM]
        DB_Comp2[Connection Pooling]
        DB_Comp3[Index Optimization]
        DB_Comp4[Backup & Recovery]
        
        DB --> DB_Comp1
        DB --> DB_Comp2
        DB --> DB_Comp3
        DB --> DB_Comp4
        
        %% Database Tables
        subgraph "Core Tables"
            T1[platform_services]
            T2[incidents]
            T3[programs]
            T4[service_metrics]
            T5[executive_reports]
            T6[risk_registers]
        end
        
        DB --> T1
        DB --> T2
        DB --> T3
        DB --> T4
        DB --> T5
        DB --> T6
    end
    
    %% External Integrations
    subgraph "External Integrations"
        direction TB
        EXT[Third-party Services]
        EXT_Comp1[Monitoring Tools<br/>Datadog/Prometheus]
        EXT_Comp2[Incident Management<br/>PagerDuty/Opsgenie]
        EXT_Comp3[Project Management<br/>Jira/Asana]
        EXT_Comp4[Communication<br/>Slack/Teams]
        
        EXT --> EXT_Comp1
        EXT --> EXT_Comp2
        EXT --> EXT_Comp3
        EXT --> EXT_Comp4
    end
    
    %% Data Flow
    UI -- HTTP Requests --> API
    API -- Data Queries --> AI
    AI -- Processed Analysis --> DP
    DP -- Store Results --> DB
    DB -- Retrieve Data --> DP
    DP -- Send Signals --> AI
    AI -- Return Insights --> API
    API -- JSON Responses --> UI
    
    %% External Connections
    EXT_Comp1 -- Metric Ingestion --> DP
    EXT_Comp2 -- Incident Sync --> API
    EXT_Comp3 -- Program Data --> DB
    EXT_Comp4 -- Notifications --> API
    
    %% Styling
    classDef presentation fill:#bbdefb,stroke:#0d47a1,stroke-width:2px,color:#000
    classDef api fill:#e1bee7,stroke:#4a148c,stroke-width:2px,color:#000
    classDef ai fill:#c8e6c9,stroke:#1b5e20,stroke-width:2px,color:#000
    classDef processing fill:#ffecb3,stroke:#ff6f00,stroke-width:2px,color:#000
    classDef storage fill:#f8bbd9,stroke:#880e4f,stroke-width:2px,color:#000
    classDef external fill:#d7ccc8,stroke:#3e2723,stroke-width:2px,color:#000
    
    class UI,UI_Comp1,UI_Comp2,UI_Comp3,UI_Comp4 presentation
    class API,API_Comp1,API_Comp2,API_Comp3,API_Comp4,EP1,EP2,EP3,EP4,EP5,EP6,EP7 api
    class AI,AI_Comp1,AI_Comp2,AI_Comp3,AI_Comp4,AI_Cap1,AI_Cap2,AI_Cap3,AI_Cap4 ai
    class DP,DP_Comp1,DP_Comp2,DP_Comp3,DP_Comp4,PS1,PS2,PS3,PS4,PS5 processing
    class DB,DB_Comp1,DB_Comp2,DB_Comp3,DB_Comp4,T1,T2,T3,T4,T5,T6 storage
    class EXT,EXT_Comp1,EXT_Comp2,EXT_Comp3,EXT_Comp4 external