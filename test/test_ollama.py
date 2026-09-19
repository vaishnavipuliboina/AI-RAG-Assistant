from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="gemma3:1b",
    temperature=0
)

response = llm.invoke("What is machine learning?")

print(response.content)