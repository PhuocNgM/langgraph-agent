# ASTM Standard RAG Agent

![Python](https://img.shields.io/badge/Python-3.10-blue)
![LangGraph](https://img.shields.io/badge/Framework-LangGraph-orange)
![RAG](https://img.shields.io/badge/Architecture-RAG-green)
![OpenAI](https://img.shields.io/badge/Model-GPT--4o-purple)

An Autonomous AI Agent designed to assist laboratory engineers in retrieving, analyzing, and calculating technical specifications from ASTM Standards (D5185, etc.).

> Purpose: Built to support new-hire onboarding and reduce manual lookup time in VILAS accredited laboratories.

---

## Overview

In lubricant testing laboratories, technicians struggle with navigating thousands of pages of PDF standards. Manual lookup is time-consuming and prone to human error.

This project implements a Stateful Agent using LangGraph that goes beyond simple RAG. It can plan, search internal documents, execute Python code for precise calculations, and reflect on its own answers to ensure accuracy.

### Key Features
- Smart Retrieval (RAG): Semantic search over ASTM PDF documents (D5185, D6557, D5222) using ChromaDB.
- Precision Calculation: Uses a Python REPL Tool to perform chemical formulas (e.g., ppm to %wt conversion) instead of relying on LLM hallucination.
- Data Analysis: Integrated Pandas DataFrame Agent to query historical lab results from CSV files.
- Self-Correction: Implements a Reflection Node to verify answer quality and re-plan if data is missing.
- Cyclic Workflow: Unlike linear chains, this agent supports loops to refine search queries dynamically.

---

## Architecture

The system is built on a cyclic graph architecture using LangGraph:

graph 
    Start --> Planner
    Planner -->|Need Info| Retriever
    Planner -->|Need Calc| Action
    Retriever --> Action
    Action --> Reflect
    Reflect -->|Good Answer| Memory
    Reflect -->|Bad Answer| Planner


### Core Components

1.  Planner Node: Analyzes user intent (Retrieval vs. Calculation vs. Chat).
2.  Retriever Node: Fetches top-k chunks from ChromaDB (hybrid search).
3.  Action Node: Executes Python scripts or Pandas queries in a sandbox.
4.  Reflect Node: Critiques the generated answer and formats it professionally.

-----

## Installation

### Prerequisites

  - Python 3.10+
  - OpenAI API Key

### Setup Steps

1.  Clone the repository

    git clone [https://github.com/PhuocNgM/langgraph-agent.git](https://github.com/PhuocNgM/langgraph-agent.git)
    cd langgraph-agent

2.  Create Virtual Environment

    conda create -n langgraph-env python=3.10
    conda activate langgraph-env

3.  Install Python Dependencies

    pip install -r requirements.txt

4.  Configure Environment Variables
    Create a .env file in the root directory:

    OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxx

-----

## Usage

### 1. Ingest Data (Build Knowledge Base)

Place your PDF files in the /document and run:

    python ingest.py

This process will parse PDFs, split them into chunks, and save vectors to memory/knowledge_base_store.

### 2. Run the Agent

Start the interactive CLI chat:

    python main.py
    
-----

## Project Structure

langgraph-agent/
├── core/                   # Agent Logic
│   ├── graph.py            # Graph definition
│   ├── state.py            # AgentState definition
│   ├── planner_node.py     # Intent classification
│   └── ...
├── memory/                 # Database Layer
│   ├── knowledge_base.py   # Ingestion pipeline
│   └── vector_store.py     # ChromaDB wrapper
├── data/                   # Raw PDF/TXT files (Gitignored)
├── ingest.py               # Data processing script
├── main.py                 # Entry point
├── requirements.txt
└── README.md

-----

## Future Roadmap

  - [ ] Internal SOP Integration: Add internal lab procedures to the Knowledge Base.
  - [ ] UI Development: Build a frontend using Streamlit or Chainlit.
  - [ ] Dockerization: Containerize the application for easier deployment.
  - [ ] Hybrid Search: Implement BM25 + Vector Search for better keyword matching.



