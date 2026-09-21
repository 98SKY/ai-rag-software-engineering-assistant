import os
from functools import lru_cache

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


@lru_cache(maxsize=1)
def get_llm_client() -> OpenAI:
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is not configured."
        )

    return OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1",
    )


def generate_answer(
    question: str,
    context: str,
) -> str:
    client = get_llm_client()

    model = os.getenv(
        "GROQ_MODEL",
        "openai/gpt-oss-20b",
    )

    instructions = """
You are an AI Software Engineering Assistant.

Answer the user's question using only the retrieved
document context supplied to you.

Rules:
1. Use only information contained in the context.
2. Do not invent facts.
3. If the context does not contain enough information,
   say that the available documents do not provide
   enough information.
4. Keep the answer concise and technically accurate.
5. When useful, reference sources as [Source 1],
   [Source 2], etc.
""".strip()

    prompt = f"""
RETRIEVED CONTEXT:

{context}

USER QUESTION:

{question}
""".strip()

    response = client.responses.create(
        model=model,
        instructions=instructions,
        input=prompt,
    )

    return response.output_text