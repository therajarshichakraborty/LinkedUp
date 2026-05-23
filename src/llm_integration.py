from dotenv import load_dotenv
load_dotenv()
import os
from langchain_groq import ChatGroq

api_key = os.getenv("GROQ_CLOUD_API_KEY")

if api_key:
    llm = ChatGroq(
        groq_api_key=api_key, model="llama-3.3-70b-versatile"
    )
else:
    llm = None

if __name__ == "__main__":
    response = llm.invoke("How to cook mutton kosha?")
    print(response.content)
