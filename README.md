
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

Sonuç olarak, her bir Rating değeri ve bu değerin kaç kez geçtiğini belirten bir seri elde edilir.

Her bir derecelendirme için inceleme sayısını çizdikten sonra, sınıf dengesizliğinin olduğu açıktır. 1 ve 2 derecelerini, 3 ve 4 derecelerini ve 5 derecesini bir araya getirerek, sınıf dengesizliği azaltılmalıdır.
```python
def new_rating(num):
    if (num == 1) or (num == 2):
        return 'dusuk'
    elif (num == 3) or (num == 4):
        return 'ortalama'
    else:
        return 'harika'

df['new_rating'] = df['Rating'].apply(new_rating)
```


![countrating](https://github.com/user-attachments/assets/e1b8c539-bdb9-4576-bfc7-30b37df98c93)


Sınıf dengesizliği şimdi daha az belirgin, ancak hâlâ daha az "kötü" inceleme türü var. Modellerde class_weight="balanced" parametresi kullanılarak bu durum dikkate alınacaktır.

**Kelime Sayısı Grafiği**
```python
df['words'] = [x.split() for x in df['Review Text']]
df['word_count'] = [len(x) for x in df['words']]

grouped_rating = df.groupby('new_rating')['word_count'].mean()
sns.barplot(x = grouped_rating.index, y = grouped_rating.values).set_title('Word Count by Review')
```
![wordcount](https://github.com/user-attachments/assets/3a94325d-305e-4a88-b818-2a96a22fc40e)

Türkçe stopwords listesini yükle
sw = stopwords.words('turkish')


pip install stanza
Stanza, doğal dil işleme projelerinde kapsamlı ve güçlü araçlar sunarak metin verilerinden anlam çıkarma süreçlerini kolaylaştırır.

def doc_preparer_stanza(doc, stop_words=stopwords_tr):
Bu fonksiyon, verilen bir metni işleyerek küçük harfe dönüştürür, noktalama ve durdurma kelimelerini çıkarır ve kelimeleri kök hâline getirir.

df['tokenized'] = df['Review Text'].apply(doc_preparer_stanza)
Bu kod, Review Text sütunundaki her metni doc_preparer_stanza fonksiyonuyla işleyerek elde edilen sonuçları tokenized adlı yeni bir sütunda saklar.

Kelimelerde Frekans Dağılımı


df['tokenized_words'] = [x.split() for x in df['tokenized']]
tokenized_words = df['tokenized_words'].to_list()

word_list = []
for x in tokenized_words:
    word_list.extend(x)
word_list
freq_dist_text = nltk.FreqDist(word_list)
plt.subplots(figsize=(20,12))
freq_dist_text.plot(30)

![kelimedagilimi](https://github.com/user-attachments/assets/7d0e0ded-7e70-475a-ad15-09bdef58bf95)

Bu frekans dağılımı, hangi kelimelerin daha yüksek bir sıklığa sahip olduğunu göstermektedir.

daha sonra kelime bukutları oluşturldu
for rating in list(df['new_rating'].unique()):
    show_wordcloud(df[df['new_rating']==rating]['tokenized'], title=rating)


![keliembulutu](https://github.com/user-attachments/assets/9ba0a4a0-d232-4b21-9be5-1da36f2114a9)

Yukarıdaki kelime bulutu, her kategoride en sık görünen kelimeleri göstermektedir.

def pos_tags_stanza(doc):

Bu kod bir metin veri kümesini işlemek ve belirli metrikleri hesaplamak için kullanılır.

POS Etiketleme: Stanza kütüphanesi kullanılarak kelimelerin dil bilgisel etiketleri (POS tags) çıkarılıyor.

Yeni Bir DataFrame Oluşturma: df_eda adında yeni bir veri çerçevesi oluşturuluyor.

Lemmatized Metin: İşlenmiş metin (LEM) sütununa atanıyor.

POS Etiketleri: LEM sütunundaki her kelimenin POS etiketleri çıkarılıyor ve POS sütununa atanıyor.

(POS etiketleme, doğal dil işleme (NLP) alanında bir metindeki her kelimenin dil bilgisel kategorisini belirlemek için kullanılır.)


voilin plot oluşrululması

import seaborn as sns
import matplotlib.pyplot as plt

import math

Görselleştirilecek sütunlar
cols = ['NOUN', 'ADJ', 'ADV', 'VERB', 'CHAR', 'WORD', 'SENT', 'LEN', 'AVG']

Alt alta grafik düzeni için ayarlar
fig, ax = plt.subplots(nrows=len(cols), ncols=1, figsize=(10, len(cols) * 4), facecolor='w')
plt.subplots_adjust(hspace=0.5)  # Grafikler arasındaki boşluk

sns.set_style('whitegrid')
sns.set_context("talk")

Her sütun için grafik çizimi
for idx, col in enumerate(cols):
    sns.violinplot(
        data=df_eda,
        y=df_eda[col],
        x=df_eda['target'],
        ax=ax[idx],
        inner=None,
        palette='mako',
        dodge=False
    ).set_title(col)

    # Eksen ayarları
    ax[idx].set_xticks([])
    ax[idx].set_xlabel('')
    ax[idx].set_ylabel('')

Grafikleri göster
plt.show()


![voiln](https://github.com/user-attachments/assets/d5023404-8928-4f3c-aa3c-148502e4d25b)



Correlation Heatmap oluştulasmı



![correllasyon](https://github.com/user-attachments/assets/8033e2a4-9130-4d89-87f9-8bd8f2670616)



Bu özellikten özelliğe korelasyon ısı haritasına dayanarak, karakter sayısı, kelime sayısı ve ortalama cümle uzunluğunun birbirleriyle yüksek bir korelasyona sahip olduğu görülmektedir.

Vektörleştirme(Vectorizing)

TF-IDF Vektörleştirici kullanılmıştır; bu, bir kelimenin bir belgede ne kadar sık göründüğünü ve ayrıca kelimenin genel korpustaki ne kadar benzersiz olduğunu dikkate alır. En anlamlı kelimeleri yakalayabilmek için, belgelerdeki kelimelerin en üst %20'sini ve en alt %10'unu kesiyoruz.

("Korpus" terimi, belirli bir amaca yönelik olarak toplanmış metin veri kümesini ifade eder.)

tfidf_train = TfidfVectorizer(sublinear_tf=True, max_df=.9, min_df=.05,  ngram_range=(1, 1))

train_features = tfidf_train.fit_transform(X_train).toarray()
test_features = tfidf_train.transform(X_test).toarray()
Bu kod, eğitim ve test verilerini TF-IDF vektörlerine dönüştürmek için kullanılır. 
PCA

Sonuçların değişip değişmeyeceğini belirlemek için bazı modellerde çok boyutluluğu azaltmak amacıyla PCA (Ana Bileşen Analizi) kullandım.

pca.n_components_
     
84
ca.n_components_ PCA (Principal Component Analysis): modelinin kaç tane ana bileşen seçtiğini gösterir. Bu değer, modelin veri setindeki toplam varyansın ne kadarını açıkladığını belirler. n_components=0.9 olarak ayarladığınında, PCA toplam varyansın %90'ını açıklayan yeterli sayıda bileşeni seçecektir.

pcaresmi

![pca](https://github.com/user-attachments/assets/bd33e820-3045-4863-aba8-52b5cc2def03)


def metrics_score(train_preds, y_train, test_preds, y_test):

Naive Bayes, Logisitic Regression, Logisitic Regression with PCA, Decision Tree, Decision Tree with PCA, random forest, lightgbm, knn kullnıldı(buraya bunlarla ilgili birşeyler yaz kod örneği olabilir) En yüksek doğruluk ve F1 skorunu hangi modelin verdiğini değerlendirmek için birkaç farklı modeli uygun hale getirdim. Her modeli birbirine karşı doğru bir şekilde karşılaştırmak amacıyla, her model için en uygun hiperparametreleri belirlemek üzere bir grid-search gerçekleştirdim.

MODEL DEĞERLENDİRME



model_candidates = [

    {'name':'Naive Bayes',
     'accuracy score':accuracy_score(y_test, nb_test_preds),
     'f1 score':metrics.f1_score(y_test, nb_test_preds, average='weighted')},

    {'name':'Logistic Regression',
     'accuracy score':accuracy_score(y_test, lr_test_preds),
     'f1 score':metrics.f1_score(y_test, lr_test_preds, average='weighted')},

    {'name':'Logistic Regression (PCA)',
     'accuracy score':accuracy_score(y_test, lr_test_preds_pca),
    'f1 score':metrics.f1_score(y_test, lr_test_preds_pca, average='weighted')},

    {'name':'Decision Tree',
     'accuracy score':accuracy_score(y_test, dt_test_preds),
     'f1 score':metrics.f1_score(y_test, dt_test_preds, average='weighted')},

    {'name':'Decision Tree (PCA)',
     'accuracy score':accuracy_score(y_test, dt_test_preds_pca),
     'f1 score':metrics.f1_score(y_test, dt_test_preds_pca, average='weighted')},

    {'name':'Random Forest',
     'accuracy score':accuracy_score(y_test, rf_test_preds),
     'f1 score':metrics.f1_score(y_test, rf_test_preds, average='weighted')},

    {'name':'Light GBM',
     'accuracy score':accuracy_score(y_test, gbm_test_preds),
     'f1 score':metrics.f1_score(y_test, gbm_test_preds, average='weighted')},

    {'name':'KNN',
     'accuracy score':accuracy_score(y_test, knn_test_preds),
    'f1 score':metrics.f1_score(y_test, knn_test_preds, average='weighted')}

]


	accuracy score	f1 score
name		
Naive Bayes	0.712963	0.645777
Logistic Regression	0.597222	0.621896
Logistic Regression (PCA)	0.597222	0.623525
Decision Tree	0.662037	0.593373
Decision Tree (PCA)	0.680556	0.568102
Random Forest	0.675926	0.545222
Light GBM	0.726852	0.703356
KNN	0.694444	0.586114
 modeller için confussion matris
 
![conf2](https://github.com/user-attachments/assets/f5866f3b-de7b-4b32-8331-c4d0cb63d5f3)

![conf4](https://github.com/user-attachments/assets/7b95ab28-7071-4082-ad1c-5146375ff1e6)



