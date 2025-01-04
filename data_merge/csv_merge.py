import pandas as pd

csv1_path = "sehzade_cagkebap_reviews.csv"
csv2_path = "uzan_et_mangal_reviews.csv"
csv3_path = "yesemek_gaziantep_reviews.csv"

# CSV dosyalarini yukleme
data1 = pd.read_csv(csv1_path)
data2 = pd.read_csv(csv2_path)
data3 = pd.read_csv(csv3_path)

# Tum dosyalari birlestirme
merged_data = pd.concat([data1, data2, data3], ignore_index=True)

# istenmeyen sutunlari kaldirma
columns_to_drop = ["Page", "Review Number"]
merged_data = merged_data.drop(columns=columns_to_drop, errors='ignore')

# eksik verileri kontrol etme ve doldurma
if merged_data.isnull().sum().sum() > 0:
    merged_data = merged_data.fillna(method='ffill').fillna(method='bfill')

# analiz icin uygun formatta kaydetme
output_path = "merged_data.csv"
merged_data.to_csv(output_path, index=False)

# temel analiz
print("Birlestirilen veri kumesinin ilk 5 satiri:")
print(merged_data.head())

print("\nSutunlara gore ozet bilgiler:")
print(merged_data.describe(include='all'))

print("\nEksik degerlerin toplami:")
print(merged_data.isnull().sum())
