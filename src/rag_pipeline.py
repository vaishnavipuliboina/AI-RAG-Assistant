from langchain_ollama import ChatOllama


def get_llm():

    llm = ChatOllama(
        model="gemma3:1b",
        temperature=0
    )

    return llm


def generate_answer(question, vector_store):

    # Retrieve relevant chunks
    results = vector_store.similarity_search(
        question,
        k=3
    )

    # Create context
    context = ""

    for result in results:
        context += result.page_content
        context += "\n\n"

    # Prompt
    prompt = f"""
You are a document question-answering assistant.

Answer the question using ONLY the information
provided in the context below.

Do not use outside knowledge.

If the answer is not available in the context,
say:

"The answer is not available in the document."

Context:
{context}

Question:
{question}

Answer:
"""

    # Load LLM
    llm = get_llm()

    # Generate response
    response = llm.invoke(prompt)

    return response.content, results