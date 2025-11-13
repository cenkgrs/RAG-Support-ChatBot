from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv
from typing import List
import pickle
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


# ENV yükle
load_dotenv()

# OpenAI istemcisi
client = OpenAI(api_key=os.getenv("OPENAI_KEY"))

app = FastAPI()

# CORS ayarı
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]

@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    '''
    completion = client.chat.completions.create(
        model="gpt-4o-mini",  # veya gpt-4o / gpt-5
        messages=[
            {"role": "system", "content": "Sen bir e-ticaret asistanısın"},
			*req.messages
        ]
    )

    reply = completion.choices[0].message.content

    return {"reply": reply}
    '''

    last_message = req.messages[-1]


    context = retrieve(last_message.content, top_k=3)
    print(context)
    prompt = f"Sen bir e-ticaret sitesi destek asistanısın. Asla Chat GPT olduğunu söyleme. İsmin Arge-Destek. Aşağıdaki bilgiler doğrultusunda soruyu cevapla:\n\nBilgi:\n{chr(10).join(context)}\n\nSoru: {last_message.content}"
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return {"reply": response.choices[0].message.content}



def get_embedding(text):
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return np.array(response.data[0].embedding)

def retrieve(query, top_k=1):
    with open("vector_db.pkl", "rb") as f:
        vector_db = pickle.load(f)
    query_emb = get_embedding(query)
    similarities = [cosine_similarity([query_emb], [item["embedding"]])[0][0] for item in vector_db]
    top_indices = np.argsort(similarities)[-top_k:][::-1]
    results = [vector_db[i]["text"] for i in top_indices]
    return results



