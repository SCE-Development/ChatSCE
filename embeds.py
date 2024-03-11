from openai import OpenAI
import pandas as pd
import os
import json
from dotenv import load_dotenv
import tiktoken

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

file = open('core_classes.json')

df = pd.read_json(file)
df = df[["title","units","description","prereqs","coreqs","grading_type","note"]]
df = df.dropna()
df["combined"] = (
    "Title: " + df.title.str.strip() + "; description: " + df.description.str.strip()
)
df.head(2)

def get_embedding(text, model="text-embedding-3-small"):
    text = text.replace("\n", " ")
    return client.embeddings.create(input=[text], model=model).data[0].embedding

df.to_csv('classes.csv', index=False)
df['ada_embedding'] = df.combined.apply(lambda x: get_embedding(x, model='text-embedding-3-small'))
df.to_csv('embedded.csv', index=False)
