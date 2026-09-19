import os

from langchain_community.vectorstores import FAISS


VECTOR_DB_PATH = "vector_db"


def create_vector_store(chunks, embeddings):

    vector_store = FAISS.from_documents(
        chunks,
        embeddings
    )

    # Save FAISS database
    vector_store.save_local(VECTOR_DB_PATH)

    return vector_store


def load_vector_store(embeddings):

    if not os.path.exists(VECTOR_DB_PATH):
        return None

    vector_store = FAISS.load_local(
        VECTOR_DB_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vector_store