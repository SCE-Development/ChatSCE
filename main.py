from fastapi import FastAPI
from dotenv import load_dotenv
from openai import OpenAI
from collections import deque
import uvicorn
import os

load_dotenv()

try:
    client = OpenAI(
        api_key=os.getenv("API_KEY"),
    )

    # Necessary for saving messages for context
    # Latest messages are at the end of the list
    previous_messages = deque([])

    # These can be fine tuned later
    # Consult the OpenAI documentation for more information
    INSTRUCTIONS = None
    TEMPERATURE = 0.5
    MAX_TOKENS = 150
    FREQUENCY_PENALTY = 0
    PRESENCE_PENALTY = 0.5
    MAX_CONTEXT_LENGTH = 10
except Exception:
    print(
        "Error: Please make sure you have set the API_KEY environment variable correctly."
    )
    exit(1)

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Welcome": "This is the SCE Chatbot API"}


@app.get("/gpt/{query}")
async def gpt_query(query: str):
    messages = []

    for question, answer in previous_messages:
        messages.append({"role": "user", "content": question})
        messages.append({"role": "assistant", "content": answer})

    messages.append({"role": "user", "content": query})

    completion = client.chat.completions.create(
        messages=messages,
        model="gpt-3.5-turbo",
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
        top_p=1,
        frequency_penalty=FREQUENCY_PENALTY,
        presence_penalty=PRESENCE_PENALTY,
    )

    previous_messages.append((query, completion.choices[0].message.content))

    if len(previous_messages) > MAX_CONTEXT_LENGTH:
        deque.popleft(previous_messages)

    print(previous_messages)
    return {"response": completion.choices[0].message.content}


def main():
    try:
        HOST = os.getenv("HOST")
        PORT = int(os.getenv("PORT"))
    except Exception:
        print(
            "Error: Please make sure you have set the HOST and PORT environment variables correctly."
        )
        exit(2)
    uvicorn.run(
        app,
        host=HOST,
        port=PORT,
        log_level="info",
    )


if __name__ == "__main__":
    main()
