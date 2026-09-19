📚 AI-Powered Document Intelligence & RAG Assistant

A Retrieval-Augmented Generation (RAG) application that allows users to upload PDF documents and ask natural-language questions about their contents.

The system retrieves relevant information from the uploaded document using semantic search and generates answers using a locally running LLM through Ollama.

🚀 Project Overview

Traditional document search requires users to manually scan large PDF files to find information.

This project provides a conversational interface where users can:

Upload a PDF document

Extract text from the document

Split the text into smaller chunks

Convert chunks into semantic embeddings

Store embeddings in a FAISS vector database

Retrieve the most relevant chunks for a question

Generate an answer using a local LLM

Display the source pages used for the answer

The project was tested using a 100-page synthetic company knowledge-base PDF containing company information, employees, departments, projects, products, financial data, dates, and relationships.

🏗️ System Architecture

                    ┌─────────────────┐
                    │   User uploads  │
                    │      PDF        │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   PDF Loader    │
                    │    PyPDF        │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │    Chunking     │
                    │ Recursive Text  │
                    │     Splitter    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   Embeddings    │
                    │ MiniLM Model    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │      FAISS      │
                    │ Vector Database │
                    └────────┬────────┘
                             │
                       User Question
                             │
                             ▼
                    ┌─────────────────┐
                    │    Similarity   │
                    │     Search      │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  Retrieved      │
                    │    Context      │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   Gemma LLM     │
                    │     Ollama      │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Answer + Source │
                    │      Pages      │
                    └─────────────────┘

🔄 RAG Pipeline

The application follows three main stages:

1. Retrieval

The user's question is converted into an embedding and compared with document embeddings stored in FAISS.

The most relevant document chunks are retrieved.

2. Augmentation

The retrieved chunks are added to a prompt as context.

The LLM is instructed to answer using the provided context.

3. Generation

The local Gemma model generates the final answer based on the retrieved document context.

Question
   ↓
Embedding
   ↓
FAISS Similarity Search
   ↓
Relevant Chunks
   ↓
Context + Question
   ↓
Gemma
   ↓
Final Answer

🛠️ Technologies Used

Technology

Purpose

Python

Core programming language

Streamlit

Web application interface

LangChain

RAG pipeline orchestration

PyPDF

PDF text extraction

RecursiveCharacterTextSplitter

Document chunking

Sentence Transformers

Text embeddings

all-MiniLM-L6-v2

Embedding model

FAISS

Vector similarity search

Ollama

Local LLM runtime

Gemma 3 1B

Local language model

python-dotenv

Environment configuration

Git/GitHub

Version control

📁 Project Structure

AI-RAG-Assistant/
│
├── app.py
├── requirements.txt
├── .env
├── .gitignore
│
├── documents/
│   └── uploaded PDF files
│
├── vector_db/
│   └── FAISS vector database
│
├── tests/
│   ├── test_embeddings.py
│   ├── test_faiss.py
│   └── test_ollama.py
│
└── src/
    ├── __init__.py
    ├── document_processor.py
    ├── embeddings.py
    ├── vector_store.py
    └── rag_pipeline.py

📌 Main Components

app.py

The main Streamlit application.

Responsibilities:

PDF upload

Document processing

Embedding creation

FAISS database creation

Question input

Answer generation

Source page display

src/document_processor.py

Loads the PDF using PyPDFLoader and splits the extracted text into chunks.

Current configuration:

chunk_size=1000
chunk_overlap=200

src/embeddings.py

Creates embeddings using:

sentence-transformers/all-MiniLM-L6-v2

The model produces a 384-dimensional vector representation for each text input.

src/vector_store.py

Creates and loads the FAISS vector database.

FAISS is used to efficiently search for document chunks that are semantically similar to a user's question.

src/rag_pipeline.py

Handles:

Relevant chunk retrieval

Context creation

Prompt construction

Local LLM invocation

Answer generation

The application uses:

Gemma 3 1B

through Ollama.

⚙️ Installation

1. Clone the repository

git clone <YOUR_GITHUB_REPOSITORY_URL>
cd AI-RAG-Assistant

2. Create a virtual environment

python -m venv venv

3. Activate the virtual environment

Windows:

venv\Scripts\activate

4. Install dependencies

pip install -r requirements.txt

🦙 Install Ollama

Install Ollama on your system and download the Gemma model.

Check installed models:

ollama list

Download the model:

ollama pull gemma3:1b

Test Ollama:

python tests/test_ollama.py

🧪 Test the Components

Test embeddings

python tests/test_embeddings.py

Expected output includes:

Embedding created!
Vector size: 384

Test FAISS

python tests/test_faiss.py

The test should return relevant documents for a semantic query.

Test Ollama

python tests/test_ollama.py

The model should return an answer to the test question.

▶️ Run the Application

Start Streamlit:

streamlit run app.py

The application will open in the browser.

Upload a PDF and wait for:

Document is ready for questions! ✅

Then enter a question and click:

Ask Question

🧪 RAG Testing

The application was tested using a company knowledge-base PDF.

Example questions:

Direct Retrieval

What is the headquarters of TechNova Systems?

Numerical Retrieval

What was TechNova Systems' 2025 revenue?

Entity Retrieval

Who manages Project Orion at TechNova Systems?

Multi-hop Question

Who manages Project Orion at TechNova Systems and what technology does the project use?

Filtering

Which projects at TechNova Systems have budgets above $1 million?

Product Information

What products does CoreStack Innovations offer?

Hallucination Test

What is the CEO's personal phone number at TechNova Systems?

For information that does not exist in the document, the application is instructed to respond:

The answer is not available in the document.

📊 Example Output

For the question:

What is the headquarters of TechNova Systems?

the application retrieved relevant document chunks and generated:

Bengaluru

The interface also displayed the source pages used during retrieval.

🔍 Why FAISS?

FAISS is used because traditional keyword search may fail when the question and document use different wording.

For example:

Question:
Which city is TechNova Systems headquartered in?

Document:
The headquarters of TechNova Systems is located in Bengaluru.

The words are not exactly identical, but their meanings are related.

Semantic embeddings allow the system to retrieve the relevant information based on meaning.
