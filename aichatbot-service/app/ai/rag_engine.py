import os
from dotenv import load_dotenv

load_dotenv()

from .vectorstore import get_vectorstore

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage


llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile"
)


def ask(user_question: str) -> dict:

    vectorstore = get_vectorstore()

    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 4}
    )

    matched_docs = retriever.invoke(user_question)

    if not matched_docs:
        return {
            "answer": "Sorry, we don't have that currently.",
            "matched_products": []
        }

    context = "\n\n".join([
        doc.page_content for doc in matched_docs
    ])

    system_prompt = """
You are a rental assistant for Rentout.in in Kerala.

Help customers find products to rent.

Answer ONLY from the provided product context.

Keep responses SHORT and CONCISE.

Mention:
- product name
- price
- location

If unavailable say:
'Sorry, we don't have that currently.'
"""

    user_prompt = f"""
Customer question:
{user_question}

Available products:
{context}
"""

    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ])

    matched_products = [
        {
            "product_id": doc.metadata.get("product_id"),
            "title": doc.metadata.get("title"),
            "price_per_day": doc.metadata.get("price_per_day"),
            "locality": doc.metadata.get("locality"),
        }
        for doc in matched_docs
    ]

    return {
        "answer": response.content,
        "matched_products": matched_products
    }