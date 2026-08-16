# Enterprise AI Digital Employee

An AI-powered enterprise assistant that combines ServiceNow, Generative AI, FastAPI, conversation memory, RAG, and workflow automation to help employees solve requests and trigger enterprise actions.

## Overview

The Enterprise AI Digital Employee provides a unified AI interface inside ServiceNow.

It can understand employee requests, maintain conversation context, retrieve information from uploaded documents, adapt to different enterprise personas, and automate ServiceNow actions.

## Key Features

- Generative AI-powered employee assistant
- Conversation memory for multi-turn interactions
- AI personas for different enterprise roles
- Document upload and processing
- Retrieval-Augmented Generation (RAG)
- Automated ServiceNow incident creation
- AI task analytics and execution metrics
- ServiceNow REST API integration
- FastAPI-based AI backend

## Architecture

```text
Employee
    |
    v
ServiceNow AI Chat
    |
    | REST API
    v
FastAPI AI Backend
    |
    +-------------------+
    |                   |
    v                   v
OpenAI API         ServiceNow APIs
    |                   |
    |              +----+----+------+
    |              |         |      |
    |              v         v      v
    |          Incidents   AI Tasks Analytics
    |
    v
AI Response
Core Workflow
Employee Request
       |
       v
ServiceNow AI Chat
       |
       v
FastAPI AI Engine
       |
       v
AI + Memory + RAG
       |
       v
Response or Enterprise Action
       |
       v
ServiceNow

Tested Scenarios
Scenario	Status
Standard AI Response	PASS
Conversation Memory	PASS
AI Persona Context	PASS
Document Upload + RAG	PASS
ServiceNow Incident Creation	PASS
Technology Stack
Backend
Python
FastAPI
Pydantic
Uvicorn
Requests
AI
OpenAI API
Generative AI
Conversation Memory
Retrieval-Augmented Generation
Enterprise Platform
ServiceNow
ServiceNow Script Includes
ServiceNow REST APIs
ServiceNow Service Portal
ServiceNow Tables
ServiceNow Dashboard
Project Structure
Enterprise-AI-Digital-Employee/
|
+-- backend/
|   +-- main.py
|   +-- config.py
|   +-- models.py
|   +-- requirements.txt
|   |
|   +-- services/
|   |   +-- analytics_service.py
|   |   +-- document_service.py
|   |   +-- incident_service.py
|   |   +-- memory_service.py
|   |   +-- openai_service.py
|   |   +-- rag_service.py
|   |
|   +-- utils/
|       +-- helpers.py
|       +-- logger.py
|
+-- servicenow/
|   +-- widget/
|   +-- script_includes/
|   +-- rest_messages/
|   +-- tables/
|   +-- dashboard/
|
+-- README.md
+-- .gitignore
+-- LICENSE
Local Setup

Clone the repository:

git clone https://github.com/Meghana-040324/Enterprise-AI-Digital-Employee.git
cd Enterprise-AI-Digital-Employee

Go to the backend:

cd backend

Install dependencies:

pip install -r requirements.txt

Create a .env file with your own credentials:

OPENAI_API_KEY=your_openai_api_key
INSTANCE_URL=your_servicenow_instance_url
USERNAME=your_servicenow_username
PASSWORD=your_servicenow_password

Start the backend:

python -m uvicorn main:app --reload

The API runs at:

http://127.0.0.1:8000

API documentation:

http://127.0.0.1:8000/docs
Security

API keys and ServiceNow credentials are stored in environment variables and excluded from Git using .gitignore.

Never commit API keys, passwords, or other secrets to GitHub.

Use Cases
IT support automation
Employee self-service
Enterprise knowledge search
Document-based question answering
Incident management
HR assistance
Enterprise workflow automation
AI-powered service desk
Future Enhancements
Advanced enterprise knowledge bases
Additional enterprise system integrations
Role-based AI access control
Advanced monitoring and observability
Voice-based employee interaction
Additional workflow automation
Production cloud deployment
Author

Meghana B

Enterprise AI automation project combining ServiceNow and Generative AI.