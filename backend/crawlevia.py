import requests
from bs4 import BeautifulSoup
import json
import time
from urllib.parse import urlparse

# Yardımcı fonksiyon: HTML'den metin temizleme
def clean_text(text):
    if not text:
        return ""
    return " ".join(text.strip().split())

# Ürün sayfasını parse eden fonksiyon
def parse_product_page(url):
    """Verilen eviahome URL'sinden başlık, açıklama, fiyat ve paket bilgilerini JSONL formatında hazırlar."""
    print(f"🔍 {url} taranıyor...")
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
    except Exception as e:
        print(f"❌ Hata: {e}")
        return None

    soup = BeautifulSoup(r.text, "html.parser")

    # Başlık
    title_tag = soup.find("h1", class_="product-title") or soup.find("h1")
    title_text = clean_text(title_tag.text) if title_tag else ""

    # Açıklama
    accordion_div = soup.find("div", id="accordion")
    accordion_texts = []

    if accordion_div:
        # Accordion içindeki tüm card-body'leri seç
        card_bodies = accordion_div.find_all("div", class_="card-body")
        for body in card_bodies:
            # İçeriği temizle ve ekle
            text = clean_text(body.get_text(separator=" "))
            if text:
                accordion_texts.append(text)

    # 2️⃣ Normal <li class="detail-desc-list"> açıklamaları
    desc_items = []
    li_elements = soup.find_all("li", class_="detail-desc-list")
    for li in li_elements:
        desc_items.append(clean_text(li.text))

    # 3️⃣ Hepsini birleştir
    desc_text = " ".join(desc_items + accordion_texts)


    # Fiyat bilgisi
    price_text = ""
    old_price_text = ""
    price_tag = soup.find("h4", class_="ps-product__price")
    if price_tag:
        span_tag = price_tag.find("span")
        if span_tag:
            price_text = clean_text(span_tag.text)  # örn: "2 130.04₺"
        del_tag = price_tag.find("del")
        if del_tag:
            old_price_text = clean_text(del_tag.text)  # örn: "2 330.04₺"


    # Paket bilgisi
    package_text = ""
    package_div = soup.find("div", id="productDetail-content") or soup.find("div", class_="product-packaging")
    if package_div:
        h4_tags = package_div.find_all("h4")
        package_text = " ".join([clean_text(h4.text) for h4 in h4_tags])

    # Kategoriler
    categories_p = soup.find("p", class_="categories")
    categories = []

    if categories_p:
        for a in categories_p.find_all("a"):
            strong_tag = a.find("strong")
            if strong_tag:
                categories.append(clean_text(strong_tag.text))

    # Tek string olarak birleştirebilirsin
    categories_text = ", ".join(categories)

    # Marka bilgisi
    brand_p = soup.find("p", string=lambda t: t and "Marka:" in t)
    brand = ""
    if brand_p:
        strong_tag = brand_p.find("strong")
        if strong_tag:
            brand = clean_text(strong_tag.text)

    # İlk ürün resmi
    meta_img = soup.find("meta", property="og:image")
    image_url = meta_img.get("content") if meta_img else ""

    # Tek text alanında birleştir
    combined_text = f"{title_text}\n\n{desc_text}\n\nFiyat: {price_text} \nPaket: {package_text}\Kategorileri: {categories_text}\n\Marka: {brand}\nÜrün Linki: {url}\nÜrün Resmi: {image_url}"

    # product_id oluşturma
    parsed = urlparse(url)
    slug = parsed.path.strip("/").split("/")[-1]
    product_id = slug.replace("-", "_")

    return {
        "id": product_id,
        "product_id": product_id,
        "source_url": url,
        "text": combined_text,
        "metadata": {},
        "lang": "tr"
    }

# Ana fonksiyon: URL listesini okuyup JSONL oluşturur
def main():
    input_file = "eviaurls.txt"       # Her satırda bir ürün URL'si
    output_file = "eviadata.jsonl"

    with open(input_file, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]

    with open(output_file, "w", encoding="utf-8") as out:
        for url in urls:
            data = parse_product_page(url)
            if data:
                json_line = json.dumps(data, ensure_ascii=False)
                out.write(json_line + "\n")
                print(f"✅ {data['id']} eklendi")
            time.sleep(1)  # sitelere yüklenmemek için bekleme süresi

    print(f"\n📦 {output_file} dosyası oluşturuldu! Toplam {len(urls)} ürün işlendi.")

if __name__ == "__main__":
    main()
