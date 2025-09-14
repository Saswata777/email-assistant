# # llm.py
# import os
# import google as genai
# from google.genai import types

# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


# def generate_response(email_text: str, context_docs: list) -> str:
#     """
#     Generate AI response to an email using RAG + Google Generative AI.
#     """
#     context_text = "\n\n".join(context_docs)
#     prompt = f"""
# You are a helpful customer support assistant. 
# Use the following context from the company knowledge base to answer the email professionally and politely.

# Context:
# {context_text}

# Customer Email:
# {email_text}

# Response:
# """
#     client = genai.Client()
    
#     response = client.models.generate_content(
#         model="gemini-2.5-flash",
#         contents=[prompt],
#         config = types.GenerateContentConfig(
#             temperature=0.2,
#             max_output_tokens=500
#         )
#     )
    
    
#     return response.candidates[0].content


# llm.py
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv() 
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY is missing! Check your .env file.")

client = genai.Client(api_key=api_key)

def generate_response(email_text: str, context_docs: list) -> str:
    """
    Generate AI response to an email using RAG + Google Generative AI.
    """
    context_text = "\n\n".join(context_docs)
    prompt = f"""
You are a helpful customer support assistant. 
Use the following context from the company knowledge base to answer the email professionally and politely.

Context:
{context_text}

Customer Email:
{email_text}

Response:
"""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[prompt],
        config=types.GenerateContentConfig(
            temperature=0.2,
            max_output_tokens=500
        )
    )
    return response.text
