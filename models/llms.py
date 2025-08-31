from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os

os.environ["GOOGLE_API_KEY"] = ""

grader_model  = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.2,
)

vision_model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.2,
)

response_model = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.2,
    #convert_system_message_to_human=True
)

embedding_model = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001"
)