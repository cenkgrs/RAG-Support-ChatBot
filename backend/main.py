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
import json
from utils.refundRequest import *
from utils.addToCartRequest import *


# ENV yükle
load_dotenv()

# OpenAI istemcisi
client = OpenAI(api_key=os.getenv("OPENAI_KEY"))

app = FastAPI()

session_store = {}

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
    userKey: str
    messages: List[Message]

@app.post("/chat")
async def chat_endpoint(req: ChatRequest):

    userKey = req.userKey
    session = session_store.get(userKey, {})

    session_store[userKey] = session

    search_query = prep_query(req.messages)

    print(search_query)

    context = retrieve(search_query, top_k=3) 

    # System Prompt
    system_prompt = (
        "Sen bir e-ticaret destek asistanısın. "
        "Adın Arge-Destek. Asla bir yapay zeka veya ChatGPT olduğunu söyleme. "
        "Görevin gelen soruları geçmiş konuşmaları dikkate alarak yanıtlamak"
        "Cevaplarını HTML yerine Markdown formatında ver. "
        "Asla <span>, <div>, <p> gibi HTML etiketleri üretme. "
        "Liste, başlık, kalın yazı, satır başı gibi tüm biçimlendirmeleri Markdown ile yap. "
    )

    # Context Prompt
    context_block = (
        "Aşağıdaki bilgiler yalnızca yardımcı kaynaktır. "
        "Cevap verirken kullanıcıya bunlardan bahsetme:\n\n"
        f"{chr(10).join(context)}"
    )

    # Messages Data
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "system", "content": context_block},
        *[{"role": m.role, "content": m.content} for m in req.messages]
    ]

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages,
        temperature=0,
        tools = [
            {
                "name": "initiate_return",
                "description": "Kullanıcının ürün iade talebini başlatır, sipariş numarası, müşteri e-postası ve iade sebebini sorar ve onay aldıktan sonra API çağrısını yapar.",
                "type": "function",
                "function": {
                    "name": "initiate_return",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "order_number": {"type": "string", "description": "İade edilecek sipariş numarası"},
                            "return_reason": {"type": "string", "description": "İade sebebi"},
                            "customer_email": {"type": "string", "description": "Üye E-Posta Adresi"}
                        },
                        "required": ["order_number", "customer_email"]
                    }
                }
            },
            {
                "name": "add_to_cart",
                "description": "Kullanıcının sepete ürün ekleme talebini yerine getirir. Ürün adı, adet bilgisi tespit edilir.",
                "type": "function",
                "function": {
                    "name": "add_to_cart",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "product_id": {"type": "string"},
                            "product_name": {"type": "string"},
                            "quantity": {"type": "integer"}
                        },
                        "required": ["product_id", "quantity"]
                    }
                }
            }
        ]
    )

    msg = response.choices[0].message

    print(msg)

    tool_calls = getattr(msg, "tool_calls", [])

    if tool_calls:
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)

            if tool_name == "initiate_return":

                returnData = {
                    "orderNumber": tool_args.get("order_number"),
                    "returnReason": tool_args.get("return_reason"),
                    "customerEmail": tool_args.get("customer_email")
                }
                
                # API çağrısı
                result = returnOrderApi(returnData)

                if not result['status']:
                    reply_text = result['message']

                    return {"reply": reply_text}

                session.clear()
                reply_text = f"{returnData['orderNumber']} numaralı siparişinizin iade talebiniz onaylandı. Size en yakın MNG şubesine, {result['code']} iade kodu ile kolinizi teslim edebilirsiniz. Not: İade etmek istediğiniz ürünlerinizi eksiksiz ve kendi kolisinde kargoya teslim etmeniz gerekmektedir."

            elif tool_name == "add_to_cart":

                data = {
                    "userKey": userKey,
                    "productId": tool_args.get("product_id"),
                    "quantity": tool_args.get("quantity")
                }

                result = addToCart(data)

                reply_text = "Ürün sepete eklendi !"

    else:
        reply_text = msg.content

        reply_text = re.sub(r'<[^>]+>', '', msg.content)


    return {"reply": reply_text}

def prep_query(messages):

    query_prep = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": 
                '''
                Kullanıcının şu anda ne sorduğunu belirle ve bunu 1 cümlelik bir arama sorgusu olarak döndür.
                ÖNEMLİ KURAL:
                Eğer son mesaj, müşteri hizmetleri, kargo, iade, ödeme, iletişim, adres, üyelik, hesap, çağrı merkezi veya genel destek konularıyla ilgiliyse, bu durumda önceki ürünlerle bağ kurma. Bu sorular ÜRÜNDEN BAĞIMSIZDIR. Bu durumda sadece son mesajı esas alarak bir arama sorgusu üret.
                Sadece arama sorgusu döndür. Açıklama yazma.
                '''
            },
            *[{"role": m.role, "content": m.content} for m in messages]
        ],
        temperature=0
    )

    search_query = query_prep.choices[0].message.content.strip()

    return search_query

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

