from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def get_open_ai():
    GPT_DEPLOYMENT_NAME = "give your model"

    llm = AzureChatOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("OPENAI_API_VERSION"),
        model="give your model name",
        azure_deployment=GPT_DEPLOYMENT_NAME,
    )

    return llm

def get_open_ai_json():
    GPT_DEPLOYMENT_NAME = "Give your model"

    llm = AzureChatOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("OPENAI_API_VERSION"),
        model="give your model name",
        azure_deployment=GPT_DEPLOYMENT_NAME,
        model_kwargs={"response_format": {"type": "json_object"}},
    )

    return llm
