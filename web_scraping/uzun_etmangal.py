import requests
from bs4 import BeautifulSoup
import csv

# Scraper API
api_key = 'e8836fad6227ae0fdc009d8e90d2fee0'
base_url = 'https://www.tripadvisor.com.tr/Restaurant_Review-g297977-d7701911-Reviews-or{page}-Uzan_Et_Mangal-Bursa.html'

# CSV dosya kurulumu
output_file = "uzan_et_mangal_reviews.csv"

# # CSV dosyasina baslik ekleme
with open(output_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Page", "Review Number", "Rating", "Review Text"])

# yorumlari kazimak icin fonksiyon
def scrape_page(page_number):
    url = base_url.format(page=page_number)
    payload = {
        'api_key': api_key,
        'url': url
    }

    r = requests.get('https://api.scraperapi.com/', params=payload)
    soup = BeautifulSoup(r.text, 'html.parser')


    review_cards = soup.find_all("div", class_="_c")

    # Her bir inceleme icin verileri cikaran kod
    reviews_data = []
    for index, card in enumerate(review_cards):
        # SVG ogesinden puani cikar
        svg_element = card.find("svg", class_="UctUV d H0")
        rating_text = None
        if svg_element:
            title_element = svg_element.find("title")
            if title_element:
                rating_text = title_element.text.split()[3]  # puanin sayisal kismini al

        # inceleme metnini cikar
        review_text_element = card.find("span", class_="JguWG")
        review_text = review_text_element.text.strip() if review_text_element else "No review text found"

        # cikarilan verileri listeye ekle
        reviews_data.append([page_number // 15 + 1, index + 1, rating_text, review_text])

    # yorumlari CSV dosyasina kaydet
    with open(output_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(reviews_data)

# birden fazla sayfada dongu ile yorumlari kazimak
for page in range(0, 400, 15):
    scrape_page(page)

print(f"kazima tamamlandi. veri kaydedildi {output_file}.")
