import os
from pathlib import Path
from openai import OpenAI
from docx import Document
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pickle
import json
from dotenv import load_dotenv
import os

# Env
load_dotenv()

# OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_KEY"))

# Embedding fonksiyonu
def get_embedding(text):
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )

    # Verilen textin embedding değerini np array e ekle
    return np.array(response.data[0].embedding)

# Dökümanları okuma | docx veya jsonl
def read_docx(file_path):
    doc = Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        if para.text.strip():
            full_text.append(para.text.strip())
    for table in doc.tables:
        for row in table.rows:
            row_text = " | ".join([cell.text.strip() for cell in row.cells if cell.text.strip()])
            if row_text:
                full_text.append(row_text)
    return full_text


def read_jsonl(file_path):
    # JSONL ve DOCX dosyasındaki her satırı okuyup text ve metadata döndür
    items = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                obj = json.loads(line)

                # Her veri satırını item olarak ekle
                items.append({
                    "id": obj.get("id"),
                    "text": obj.get("text", ""),
                    "metadata": obj.get("metadata", {})
                })
    return items

# Belgelerden embedding oluşturma
def process_documents(folder_path):
    vector_db = []
    for file in Path(folder_path).glob("*"):
        if file.suffix.lower() == ".docx":
            texts = read_docx(file)
            for i, text in enumerate(texts):
                emb = get_embedding(text)
                vector_db.append({
                    "id": f"{file.stem}_{i}",
                    "text": text,
                    "embedding": emb
                })
        elif file.suffix.lower() == ".jsonl":
            records = read_jsonl(file)
            for rec in records:
                emb = get_embedding(rec["text"])

                # Her item verisini embedding verisi ile birlikte ekle
                vector_db.append({
                    "id": rec["id"],
                    "text": rec["text"],
                    "metadata": rec["metadata"],
                    "embedding": emb
                })

    # Kaydetmek için
    with open("evia_vector_db.pkl", "wb") as f:
        pickle.dump(vector_db, f)
    print(f"{len(vector_db)} belge parçası işlendi ve embedding kaydedildi.")
    return vector_db


# Belgeleri işle
process_documents("data/")
