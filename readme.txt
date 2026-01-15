# AI Technical Support Agent (RAG + Twilio)

## Overview
This project is a Proof of Concept (PoC) designed to automate Tier-1 technical support for complex industrial instrumentation. 

It solves the "manual lookup" bottleneck by allowing field engineers to text questions via SMS (Twilio) and receive instant answers sourced directly from technical PDF manuals, using Retrieval-Augmented Generation (RAG).

## Architecture
**User (SMS)** -> **Twilio Webhook** -> **Flask API** -> **LangChain/OpenAI (RAG)** -> **Vector Store (FAISS)**

## Key Features
* **RAG Architecture:** Uses LangChain to ingest unstructured PDF documentation and FAISS for vector similarity search.
* **Real-time Interface:** Deployed via Flask to handle synchronous Twilio webhooks.
* **Context Awareness:** Reduces hallucinations by grounding LLM responses strictly in the provided technical documentation.

## Tech Stack
* **Python 3.10+**
* **Orchestration:** LangChain
* **LLM:** OpenAI (GPT-4o)
* **Vector DB:** FAISS
* **API:** Flask
* **Gateway:** Twilio

## How to Run locally
1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Add your API keys to a `.env` file.
4. Run the application: `python app.py`