from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document


# Create sample documents
documents = [
    Document(page_content="Python is a programming language."),
    Document(page_content="Machine learning uses data to learn patterns."),
    Document(page_content="Python is widely used in machine learning."),
    Document(page_content="HTML is used to create web pages.")
]


# Load embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# Create FAISS vector store
vector_store = FAISS.from_documents(
    documents,
    embeddings
)


print("FAISS vector store created successfully!")


query = "Which language is used for machine learning?"

results = vector_store.similarity_search(
    query,
    k=2
)

print("\nRelevant documents:\n")

for result in results:
    print(result.page_content)