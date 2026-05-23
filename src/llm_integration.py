from dotenv import load_dotenv
load_dotenv()
import os
from langchain_groq import ChatGroq

def get_llm():
    api_key = os.getenv("GROQ_CLOUD_API_KEY")
    
    if not api_key:
        try:
            import streamlit as st
            api_key = st.secrets.get("GROQ_CLOUD_API_KEY")
        except Exception:
            pass
            
    if api_key:
        return ChatGroq(
            groq_api_key=api_key, model="llama-3.3-70b-versatile"
        )
    return None

if __name__ == "__main__":
    llm = get_llm()
    if llm:
        response = llm.invoke("How to cook mutton kosha?")
        print(response.content)
    else:
        print("API Key not found.")
