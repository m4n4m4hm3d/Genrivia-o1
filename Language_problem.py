import os
from langchain_google_genai import ChatGoogleGenerativeAI
from groq import Groq

os.environ['GOOGLE_API_KEY'] = 'AIzaSyA8IEPpCUcyAQVACLPKYlJEW_j3FdJD6_A'

llm = ChatGoogleGenerativeAI(model='gemini-1.5-flash') #gemini

client = Groq(
    api_key= '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',
) #Llama 3

def bangla_to_english(bangla_sentence):
    messages = [
    {
        "role": "user",
        "content": f"Translate the following Bengali sentence to English(Just one sentence): {bangla_sentence}"
    }
    ]
    
    response = llm.invoke(messages)
    message = response.content
    
    return message

def english_to_bangla(english_sentence):
    messages = [
    {
        "role": "user",
        "content": f"Translate the following english sentence to Bengali(Just bangla part): {english_sentence}"
    }
    ]
    
    response = llm.invoke(messages)
    message = response.content
    
    return message

def main_llm(message):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": message,
            }
        ],
        model="llama3-70b-8192",
        )
    return chat_completion.choices[0].message.content

english_to_bangla(main_llm(bangla_to_english("বাংলাদেশের সংক্ষিপ্ত ইতিহাস লিখ। ৫ লাইনে।")))
