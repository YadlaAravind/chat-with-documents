
import time

from google import genai
from google.genai.errors import ServerError
from flask import current_app


def generate_answer(query, retrieved_chunks):

    # 1. Get Gemini API key
    api_key = current_app.config.get("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("Gemini API key is missing")

    # 2. Check retrieved chunks
    if not retrieved_chunks:
        return "No relevant information found in the uploaded document."

    # 3. Initialize Gemini client
    client = genai.Client(api_key=api_key)

    # 4. Prepare document context
    context = "\n\n".join(
        chunk["content"]
        for chunk in retrieved_chunks
    )

    # 5. Prepare prompt
    prompt = f"""
You are an intelligent document question-answering assistant.

Answer questions using ONLY the provided document context.

STRICT RULES:
1. Understand the user's question carefully.
2. Answer only with information available in the context.
3. Never invent or assume information.
4. Include only relevant information.
5. Avoid repeating information.
6. Use simple and professional English.
7. Use clear headings and bullet points.
8. For project questions, include project name,
   technologies, features and purpose when available.
9. For technical skills, organize skills by category.
10. For education, include degree, college, duration
    and percentage when available.
11. If information is unavailable, clearly say so.

DOCUMENT CONTEXT:
{context}

USER QUESTION:
{query}

ANSWER:
"""

    # 6. Generate answer with retry handling
    for attempt in range(2):

        try:

            interaction = client.interactions.create(
                model="gemini-3.8-flash",
                input=prompt
            )

            answer = interaction.output_text

            if answer and answer.strip():
                return answer.strip()

            raise ValueError("Gemini returned an empty response")

        except ServerError as error:

            status_code = getattr(error, "status_code", None)

            if status_code != 503:
                raise

            if attempt == 1:
                raise

            wait_time = 2

            print(
                f"Gemini temporarily unavailable. "
                f"Retrying in {wait_time} seconds..."
            )

            time.sleep(wait_time)

    raise RuntimeError(
        "Unable to generate an answer using Gemini"
    )
