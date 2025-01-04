
# **Proje Adı: Tripadvisor Yorum Analizi**

Bu proje, Tripadvisor'dan Türk mutfağına sahip işletmelerden kullanıcı yorumlarını ve puanlarını **Scraper API** kullanarak kazımayı, bu verilerden bir veri seti oluşturmayı ve gelecekteki analizlere zemin hazırlamayı hedefler.

---

## **Özellikler**
- **Scraper API entegrasyonu** ile Tripadvisor verilerine erişim.
- Kullanıcı **yorumlarının** ve **puanlarının** kazınması.
- Verilerin düzenli bir şekilde **CSV dosyasına kaydedilmesi.**
- Çoklu sayfa desteği ile birden fazla yorum sayfasının işlenmesi.

---

## **Kullanım Alanları**
- Restoran işletmeleri için müşteri geri bildirimlerini analiz etmek.
- **Doğal Dil İşleme (NLP)** teknikleriyle duygu analizi yapmak.
- Farklı şehirlerdeki restoranların karşılaştırmalı analizlerini gerçekleştirmek.

---

## **Gerekli Araçlar ve Kütüphaneler**
Bu projeyi çalıştırmak için aşağıdaki araç ve kütüphaneler gereklidir:
- **Python 3.x**
- **Scraper API Hesabı**
- **Kütüphaneler:**
  ```bash
  pip install requests beautifulsoup4
  ```

---

## **Kurulum Adımları**

1. **Projeyi indirin:**
   ```bash
   git clone https://github.com/kullanici_adi/tripadvisor-yorum-analizi.git
   cd tripadvisor-yorum-analizi
   ```

2. **API Anahtarını Ayarlayın:**
   Scraper API hesabı oluşturun ve API anahtarınızı alın.
   `api_key` değişkenini şu şekilde düzenleyin:
   ```python
   api_key = 'SİZİN_API_ANAHTARINIZ'
   ```

3. **Kod dosyasını çalıştırın:**
   ```bash
   python scraper.py
   ```

---

## **Kodun Genel Akışı**

1. **Hedef URL’lerin Tanımlanması**

   Tripadvisor yorum sayfalarının dinamik URL yapısı şu şekildedir:
   ```python
   base_url = 'https://www.tripadvisor.com.tr/Restaurant_Review-g293974-d2288800-Reviews-or{page}-Sehzade_Cag_Kebap-Istanbul.html'
   ```
   Bu yapıda `{page}`, yorumların bulunduğu sayfa numarasına göre değişir. Örneğin:
   - İlk sayfa için: `Reviews-or0-...`
   - İkinci sayfa için: `Reviews-or15-...`

2. **Scraper API Kullanımı**

   Scraper API, erişim kısıtlamalarını aşmak ve sayfaların HTML içeriğini almak için kullanılır:
   ```python
   payload = {
       'api_key': api_key,
       'url': url
   }
   r = requests.get('https://api.scraperapi.com/', params=payload)
   ```

3. **HTML'den Verilerin Ayrıştırılması**

   BeautifulSoup, HTML'deki yorum ve puanları ayrıştırmak için kullanılır:
   ```python
   soup = BeautifulSoup(r.text, 'html.parser')
   review_cards = soup.find_all("div", class_="_c")
   ```

4. **Çoklu Sayfa Desteği**

   Tripadvisor sayfaları 15 yorum içerdiği için birden fazla sayfa şu döngüyle işlenir:
   ```python
   for page in range(0, 400, 15):
       scrape_page(page)
   ```

5. **Verilerin Kaydedilmesi**

   Kazınan yorumlar ve puanlar bir CSV dosyasına şu formatta yazılır:
   ```csv
   Page,Review Number,Rating,Review Text
   1,1,5,"Mükemmel bir lezzet, mutlaka deneyin!"
   1,2,4,"Fiyatlar biraz yüksek ama lezzet güzel."
   ```

---

## **Örnek Çıktı**

Çalışma tamamlandığında, kazınan veriler şu şekilde bir CSV dosyasına kaydedilecektir:
```csv
Page,Review Number,Rating,Review Text
1,1,5,"Mükemmel bir lezzet, mutlaka deneyin!"
1,2,4,"Fiyatlar biraz yüksek ama lezzet güzel."
```


## **Proje Adı: CSV Dosya Birleştirme ve Temel Veri Analizi**

Bu proje, farklı restoranlardan (Sehzade Cag Kebap, Uzan Et Mangal ve Yesemek Gaziantep) alınan Tripadvisor yorumlarını içeren CSV dosyalarını birleştirir, eksik verileri doldurur ve temel analizler yapar.

---

## **Adımlar**

1. **CSV Dosyalarını Yükleme:**
   - `sehzade_cagkebap_reviews.csv`, `uzan_et_mangal_reviews.csv` ve `yesemek_gaziantep_reviews.csv` dosyaları yüklenir.

2. **CSV Dosyalarının Birleştirilmesi:**
   - Üç dosya birleştirilir ve tek bir veri kümesine (`merged_data`) dönüştürülür.

3. **İstenmeyen Sütunların Kaldırılması:**
   - `Page` ve `Review Number` sütunları kaldırılır çünkü analiz için gerekli değildir.

4. **Eksik Verilerin Kontrolü ve Doldurulması:**
   - Eksik veriler (`NaN` değerler) kontrol edilir ve `forward fill` (önceki değeri kullanarak doldurma) ve `backward fill` (sonraki değeri kullanarak doldurma) yöntemleriyle doldurulur.

5. **Verinin Analiz İçin Kaydedilmesi:**
   - Temizlenen veri `merged_data.csv` adıyla kaydedilir.

6. **Temel Veri Analizi:**
   - Birleştirilen veri kümesinin ilk 5 satırı görüntülenir.
   - Veri kümesindeki tüm sütunlara dair özet istatistiksel bilgiler (ortalama, standart sapma, vs.) hesaplanır.
   - Eksik değerlerin toplamı gösterilir.

---

## **Kodun Çalışma Prensibi**

```python
import pandas as pd

# CSV dosyalarını yükleme
data1 = pd.read_csv(csv1_path)
data2 = pd.read_csv(csv2_path)
data3 = pd.read_csv(csv3_path)

# Tüm dosyaları birleştirme
merged_data = pd.concat([data1, data2, data3], ignore_index=True)

# İstenmeyen sütunları kaldırma
columns_to_drop = ["Page", "Review Number"]
merged_data = merged_data.drop(columns=columns_to_drop, errors='ignore')

# Eksik verileri kontrol etme ve doldurma
if merged_data.isnull().sum().sum() > 0:
    merged_data = merged_data.fillna(method='ffill').fillna(method='bfill')

# Analiz için uygun formatta kaydetme
output_path = "merged_data.csv"
merged_data.to_csv(output_path, index=False)

# Temel analiz
print("Birleştirilen veri kümesinin ilk 5 satırı:")
print(merged_data.head())

print("\nSütunlara göre özet bilgiler:")
print(merged_data.describe(include='all'))

print("\nEksik değerlerin toplamı:")
print(merged_data.isnull().sum())
 ```


## **Veri Analizi ve Görselleştirme**

Birleştirilen verilerin analizi için **Rating** (puan) sütununa göre yorum sayısı hesaplanır ve bir barplot (çubuk grafiği) ile görselleştirilir.

**Kod:**
```python
import seaborn as sns
import matplotlib.pyplot as plt

# Rating'e göre grup oluşturma ve yorum sayısını hesaplama
grouped = df.groupby('Rating')['Rating'].count() 

# Barplot ile görselleştirme
sns.barplot(x = grouped.index, y = grouped.values, palette='mako').set_title('Review Count by Rating')
plt.show()
```



![rating](https://github.com/user-attachments/assets/4d742d60-ec23-49c2-862b-0ab1cf7b1270)




