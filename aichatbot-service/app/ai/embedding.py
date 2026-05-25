import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from langchain_core.embeddings import Embeddings

load_dotenv()

_embeddings = None


class GeminiEmbeddings(Embeddings):
    def __init__(self):
        self.client = genai.Client(
            api_key=os.getenv("GOOGLE_API_KEY"),
            http_options=types.HttpOptions(api_version="v1")
        )
        self.model = "models/gemini-embedding-001"  # ✅ available on your key

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        result = self.client.models.embed_content(
            model=self.model,
            contents=texts,
        )
        return [e.values for e in result.embeddings]

    def embed_query(self, text: str) -> list[float]:
        result = self.client.models.embed_content(
            model=self.model,
            contents=[text],
        )
        return result.embeddings[0].values


def get_embeddings():
    global _embeddings
    if _embeddings is None:
        print("⚡ Loading Gemini embeddings...")
        _embeddings = GeminiEmbeddings()
    return _embeddings

# import os
# from dotenv import load_dotenv
# from langchain_google_genai import GoogleGenerativeAIEmbeddings

# load_dotenv()

# _embeddings = None


# def get_embeddings():
#     global _embeddings

#     if _embeddings is None:
#         print("⚡ Loading Gemini embeddings...")

#         _embeddings = GoogleGenerativeAIEmbeddings(
#             model="models/gemini-embedding-004",
#             google_api_key=os.getenv("GOOGLE_API_KEY"),
#         )

#     return _embeddings


# availble model checoking command 
# save as test_embed.py in your project root and run: python test_embed.py
# import os
# from dotenv import load_dotenv
# from google import genai
# from google.genai import types

# load_dotenv()

# client = genai.Client(
#     api_key=os.getenv("GOOGLE_API_KEY"),
#     http_options=types.HttpOptions(api_version="v1")
# )

# # List all available embedding models
# print("Available embedding models:")
# for model in client.models.list():
#     if "embed" in model.name.lower():
#         print(" -", model.name)