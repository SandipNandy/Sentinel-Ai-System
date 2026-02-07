# Sentinel-AI Documentation Hub

## 📚 Overview

Welcome to the Sentinel-AI documentation. This is an AI-powered platform intelligence system designed specifically for Technical Program Managers (TPMs).

## 📁 Documentation Structure

### **Core Documentation**
1. **[Architecture](./Documents/ARCHITECTURE.md)** - Technical architecture and design decisions
2. **[Metrics & KPIs](./Documents/METRICES.md)** - Measurement framework and success metrics
3. **[Product Requirements](./Documents/PRD.md)** - Product vision, features, and requirements

### **Quick Links**
- [Getting Started Guide](../README.md)
- [API Documentation](http://localhost:8000/docs) (when API is running)
- [Dashboard](http://localhost:8501) (when dashboard is running)

## 🎯 What is Sentinel-AI?

Sentinel-AI transforms infrastructure telemetry into executive decisions by:

1. **Correlating** service failures with program impact
2. **Predicting** delivery risks before they escalate
3. **Generating** executive-ready reports automatically
4. **Translating** technical incidents into business language

## 🚀 Quick Start

### **Prerequisites**
```bash
Python 3.11+
PostgreSQL 15+ (optional for demo)
OpenAI API key (for AI features)

### 🏗️ System Architecture

```mermaid
graph TB
    subgraph "Presentation Layer"
        A[TPM Dashboard Streamlit]
        A1[Real-time Visualizations]
        A2[Interactive Controls]
    end
    ...


### 4. **Embedding in Your Project:**
```html
<!-- If using HTML documentation -->
<!DOCTYPE html>
<html>
<head>
  <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
  <script>mermaid.initialize({startOnLoad:true});</script>
</head>
<body>
  <div class="mermaid">
    graph TB
        subgraph "Presentation Layer"
            A[TPM Dashboard]
        end
        ...
  </div>
</body>
</html>