from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_ollama import ChatOllama


# --------------------------------
# 1. Load PDF
# --------------------------------

loader = PyPDFLoader("temp.pdf")

documents = loader.load()

print("PDF loaded")
print("Number of pages:", len(documents))


# --------------------------------
# 2. Split PDF into chunks
# --------------------------------

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = text_splitter.split_documents(documents)

print("Number of chunks:", len(chunks))


# --------------------------------
# 3. Create embeddings
# --------------------------------

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

print("Creating vector database...")


# --------------------------------
# 4. Store embeddings in FAISS
# --------------------------------

vector_store = FAISS.from_documents(
    chunks,
    embeddings
)

print("FAISS database created")


# --------------------------------
# 5. Load LLM
# --------------------------------

llm = ChatOllama(
    model="gemma3:1b",
    temperature=0
)

print("LLM loaded")


# --------------------------------
# 6. Ask question
# --------------------------------

question = input("\nAsk a question about the PDF: ")


# --------------------------------
# 7. Retrieve relevant chunks
# --------------------------------

results = vector_store.similarity_search(
    question,
    k=3
)

print("\nRelevant chunks found:", len(results))


# --------------------------------
# 8. Combine retrieved chunks
# --------------------------------

context = ""

for result in results:
    context += result.page_content + "\n\n"


# --------------------------------
# 9. Create prompt
# --------------------------------

prompt = f"""
You are a document question-answering assistant.

Answer the question using ONLY the information
provided in the context below.

If the answer is not present in the context,
say "The answer is not available in the document."

Context:
{context}

Question:
{question}

Answer:
"""


# --------------------------------
# 10. Send to LLM
# --------------------------------

response = llm.invoke(prompt)


# --------------------------------
# 11. Display answer
# --------------------------------

print("\nAnswer:")
print(response.content)