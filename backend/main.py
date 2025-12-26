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
import requests
import time
import base64
import uuid

# ENV yükle
load_dotenv()

# OpenAI istemcisi
client = OpenAI(api_key=os.getenv("OPENAI_KEY"))

app = FastAPI()

UPLOAD_FOLDER = "uploads"  # Resimlerin kaydedileceği klasör
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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
        "Ürün bilgisi verirken ürün resmini de göster. "
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

            elif tool_name == "create_image":

                user_image = tool_args.get("user_image")

                print(user_image)

                # Kullanıcı fotoğraf seçmemişse → GPT MESAJI İLE INPUT GÖNDER
                if user_image is None or user_image == "" or user_image == "None":
                    reply_text = (
                        "Lütfen kullanmak istediğiniz fotoğrafı yükleyin:<br>"
                        '<input type="file" id="chatUpload" accept="image/*">'
                    )
                else :
                    DEFAULT_PRODUCT_IMAGE = 'https://ikikiz.com/cdn/shop/files/3368-1_8ee7e859-195d-4ee0-b272-5e027578e05d_1000x.jpg?v=1713181770'

                    user_image_url = tool_args.get("user_image")
                    product_id = tool_args.get("product_id")

                    # şimdilik default resim
                    outfit_image_url = DEFAULT_PRODUCT_IMAGE

                    result = createImage({
                        "user_image_url": user_image_url,
                        "outfit_image_url": outfit_image_url
                    })

                    reply_text = result

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
    with open("evia_vector_db.pkl", "rb") as f:
        vector_db = pickle.load(f)
    query_emb = get_embedding(query)
    similarities = [cosine_similarity([query_emb], [item["embedding"]])[0][0] for item in vector_db]
    top_indices = np.argsort(similarities)[-top_k:][::-1]
    results = [vector_db[i]["text"] for i in top_indices]
    return results

@app.post("/upload-image")
def upload_image(data: dict):
    base64_image = data.get("image")
    userKey = data.get("userKey")  # İstersen kullanabilirsin

    if not base64_image:
        return {"error": "No image provided"}

    # Lokal olarak kaydet
    image_path = save_base64_image_locally(base64_image)

    return {"url": image_path}

def save_base64_image_locally(base64_image: str) -> str:
    """Base64 formatındaki resmi uploads klasörüne kaydeder ve path döndürür."""
    # Base64 verisinde varsa başlığı ayır
    if "," in base64_image:
        _, encoded = base64_image.split(",", 1)
    else:
        encoded = base64_image

    # Binary veriye çevir
    image_data = base64.b64decode(encoded)

    # Benzersiz dosya adı
    filename = f"{uuid.uuid4().hex}.png"
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    # Dosyayı kaydet
    with open(filepath, "wb") as f:
        f.write(image_data)

    # Lokal path olarak döndür
    return f"/{UPLOAD_FOLDER}/{filename}"

def createImage(data):

    print("resim oluştururcak")

    print(data)

    url = 'https://api.lightxeditor.com/external/api/v2/aivirtualtryon'

    headers = {
        'Content-Type': 'application/json',
        'x-api-key': '8d4a9b5ddca2481d9c68d81f677e7d9c_75c2e202ef424a63b183c029451111ec_andoraitools'  # Replace with your actual API key
    }

    data = {
        "imageUrl": data['user_image_url'],
        "outfitImageUrl": data['outfit_image_url'],
        "segmentationType": 0
    }

    response = requests.post(url, headers=headers, json=data)

    # Check if the request was successful
    if response.status_code == 200:
        print("Request was successful!")
        print(response.json())
    else:
        print(f"Request failed with status code: {response.status_code}")
        print(response.text)

    result = response.json()

    orderId = result["body"]["orderId"]

   # 2) SONUCU BEKLE
    status_url = "https://api.lightxeditor.com/external/api/v2/order-status"

    print("Waiting for image to be generated...")

    while True:
        time.sleep(3)  # LightX önerisi: 2–4 saniye bekle → tekrar sorgula

        resp = requests.post(status_url, headers=headers, json={"orderId": orderId})
        data = resp.json()

        status = data["body"].get("status")
        print("Current status:", status)

        # hâlâ işleniyor
        if status in ["init", "processing"]:
            continue

        # hata durumu
        if status == "failed":
            print("Image generation failed:", data)
            return None

        # tamamlandı → sonuç hazır
        if status == "active":
            output_data = data["body"].get("outputData")

            if output_data and "outputImageUrl" in output_data:
                image_url = output_data["outputImageUrl"]
                print("FINAL IMAGE:", image_url)
                return image_url
            
            if output_data and "output" in output_data:
                image_url = output_data["output"]
                print("FINAL IMAGE:", image_url)
                return image_url
            
            
            
            print("Completed but no output image found:", data)
            return None


'''
    {
        "name": "create_image",
        "description": "
            Kullanıcı resim istediğinde bu api call ı çağır. Kullanın resmini talep et, Link verebilir veya upload etmek isteyebilir
                Upload form u aşağıdaki gibi ilet
                "Lütfen ürünün resmini yükler misiniz? Aşağıdaki yükleme alanını kullanabilirsiniz."
                <input type="file" id="chatUpload" accept="image/*">

                Kullanıcı resim yükledikten sonra create_image fonksiyonunu çağır.
            ",
        "type": "function",
        "function": {
            "name": "create_image",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_image": {
                            "type": "string",
                            "description": "Kullanıcının yüklediği fotoğraf"
                        },
                        "product_id": {
                            "type": "string",
                            "description": "Kullanıcının seçtiği ürün ID’si"
                        }
                    },
                    "required": ["user_image_url", "product_id"]
                }
        }
    }
'''