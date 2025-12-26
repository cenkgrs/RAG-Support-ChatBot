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

# Sayfa içeriğini parse eden fonksiyon
def parse_product_page(url):
    """Verilen ürün URL'sinden başlık, açıklama, fiyat ve paket bilgilerini tek text alanına koyar."""
    print(f" {url} taranıyor...")
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
    except Exception as e:
        return None

    soup = BeautifulSoup(r.text, "html.parser")

    # Başlık
    title = soup.find("h1")
    title_text = clean_text(title.text) if title else ""

    # Açıklama
    description_div = soup.find("div", id="attributesDetail")
    desc_text = ""
    if description_div:
        lis = description_div.find_all("li")
        desc_items = [clean_text(li.text) for li in lis]
        desc_text = " ".join(desc_items)

    # Fiyat bilgisi
    price_bg = soup.find("div", id="productDetail-priceBg")
    price_text = ""
    unit_price_text = ""
    if price_bg:
        sale_price_tag = price_bg.find("price", class_="sale-price")
        price_text = clean_text(sale_price_tag.text) if sale_price_tag else ""
        unit_price_tag = price_bg.find("span", class_="priceBirim")
        unit_price_text = clean_text(unit_price_tag.text) if unit_price_tag else ""

    # Paket bilgisi
    package_div = soup.find("div", id="productDetail-content")
    package_text = ""
    if package_div:
        h4_tags = package_div.find_all("h4")
        package_text = " ".join([clean_text(h4.text) for h4 in h4_tags])

    # Ürün tipi
    type_span = soup.find("span", class_="product-type")
    type_text = clean_text(type_span.text) if type_span else ""

    # Tüm verileri tek text alanına birleştir
    combined_text = f"{title_text}\n\n{desc_text}\n\nFiyat: {price_text} ({unit_price_text})\nPaket: {package_text}\nÜrün Tipi: {type_text}\nÜrün Linki: {url}"

    # Ekstra metaveri: sadece id ve url
    parsed = urlparse(url)
    product_id = parsed.path.strip("/").split("/")[-1].replace("-", "_")

    return {
        "id": product_id,
        "source_url": url,
        "text": combined_text,
        "metadata": {},
        "lang": "tr"
    }

# Ana fonksiyon: URL listesini okuyup JSONL dosyası oluşturma
def main():
    input_file = "pinurls.txt"
    output_file = "pindata.jsonl"

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

    print(f"\n {output_file} dosyası oluşturuldu! Toplam {len(urls)} ürün işlendi.")

if __name__ == "__main__":
    main()
