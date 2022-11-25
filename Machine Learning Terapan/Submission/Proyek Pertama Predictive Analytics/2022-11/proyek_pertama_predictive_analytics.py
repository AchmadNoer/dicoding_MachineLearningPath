# -*- coding: utf-8 -*-
"""rain-classification-with-k-means-gmm.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Srrm8c6jvznLVWaYvJ45Q6L_sMLx7l7l

# Introduction

Dataset ini merupakan rekaman data klimatologi harian di Seattle dari tahun 1948 hingga 2017 [[source](https://www.kaggle.com/datasets/rtatman/did-it-rain-in-seattle-19482017)]. Terdapat 5 variabel yang dicatat.

**Metadata:**

* DATE = Tanggal dilakukannya observasi (YYYY-MM-DD)
* PRCP = Intensitas curah hujan harian (dalam inci)
* TMAX = Temperatur tertinggi harian (dalam Fahrenheit)
* TMIN = Temperatur terendah harian (dalam Fahrenheit)
* RAIN = Hasil observasi Ada atau Tidak adanya hujan (True/False)

# Data Loading
"""

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.cluster import Birch
from sklearn.mixture import GaussianMixture

import seaborn as sns
sns.set_theme(style="whitegrid")

import warnings
warnings.filterwarnings('ignore')

condition = pd.read_csv("../input/did-it-rain-in-seattle-19482017/seattleWeather_1948-2017.csv")
condition

print("Ukuran dataset:", condition.shape)

"""# Data Cleaning"""

condition.info()

"""## 1.) Checking Missing Value"""

condition.isna().sum()

print(condition[condition.isnull().any(axis=1)])

"""Seperti yang bisa dilihat, kita memiliki 3 data yang mengandung data kosong. Terdapat beberapa opsi yang bisa dilakukan untuk menanganinya, salah satunya adalah dengan cara menghapus 3 data tersebut."""

condition.dropna(inplace=True)
print("Ukuran setelah cleaning:", condition.shape)

"""## 2.) Checking Duplicated Value"""

condition.duplicated().sum()

"""## 3.) Dropping Unused Columns"""

condition.drop(['DATE', 'RAIN'], axis=1, inplace=True)
print("Ukuran setelah drop kolom:", condition.shape)

"""Kolom *DATE* yang berisi tanggal dianggap tidak berpengaruh terhadap tinggi atau rendahnya curah hujan sehingga perlu dihapus. Sedangkan kolom *RAIN* dihapus karena terpengaruh oleh nilai pada kolom *PRCP*, sehingga sudah cukup diwakili oleh 1 kolom saja.

## 4.) Rename Columns
"""

condition = condition.rename(columns={"PRCP": "precipitation",
                                      "TMAX": "max_temp",
                                      "TMIN": "min_temp"
                                     })

"""# Exploring Data"""

condition.info()

condition.nunique()

condition.describe()

"""## 1.) Box Plot"""

sns.boxplot(data=condition[["max_temp", "min_temp"]], orient="h")

sns.boxplot(x=condition['precipitation'])

"""## 2.) Removing Outliers

Outlier merupakan data-data yang sifatnya tidak biasa atau berbeda dari data atau kondisi yang umum terjadi. Kita ambil satu contoh pada kolom *precipitation* yang menunjukan nilai curah hujan tertingginya sebesar 5.02 inch. Apabila dilihat di boxplot, curah hujan sebesar itu sangat jarang terjadi sehingga bisa diklasifikasikan sebagai outlier.

Maka dari itu, outlier perlu dihapus supaya data-data yang digunakan pada proses selanjutnya memiliki keseragaman. Teknik yang digunakan untuk menghapus outlier adalah IQR (Inter Quartile Range).
"""

Q1 = condition.quantile(0.25)
Q3 = condition.quantile(0.75)
IQR = Q3-Q1

print('Ukuran sebelum pembersihan outlier:', condition.shape)
condition = condition[~((condition<(Q1-1.5*IQR))|(condition>(Q3+1.5*IQR))).any(axis=1)].reset_index(drop=True)
print('Ukuran sesudah pembersihan outlier:', condition.shape)

"""# Data Visualization"""

condition.describe()

condition['precipitation'].hist(bins=25, figsize=(10,5))

condition['max_temp'].hist(bins=25, figsize=(10,5))

condition['min_temp'].hist(bins=25, figsize=(10,5))

"""# Development

Tujuannya di sini adalah untuk mengetahui jenis-jenis kondisi hujan yang bisa diklasifikasikan oleh model. Untuk jumlah kategorinya bisa dideklarasikan dari awal atau juga bisa melalui percobaan.

Model memiliki kemampuan untuk mempelajari fitur-fitur yang tidak terlihat/tersembunyi pada data. Itulah alasan diperlukannya proses pembersihan outlier supaya data memiliki ciri dan karakteristik yang bisa dikenali.

## 1.) Standarizing Data
"""

scaler = StandardScaler()
condition_scaled = scaler.fit_transform(condition)
condition_scaled

"""## 2.) Model Building"""

# Finding n Cluster
trial = []
for i in range(1, 11): 
    kmeans = KMeans(n_clusters = i, init = 'k-means++', random_state = 321)
    kmeans.fit(condition_scaled) 
    trial.append(kmeans.inertia_)

plt.plot(trial, '--bo', markersize=10)
plt.show()

"""Setelah dilakukan pengujian menggunakan metode Elbow Curve barulah bisa dilihat bahwa kurva mulai melandai pada n ke 2, 3, 4 dan terlihat lurus pada n yang seterusnya. Maka dari itu, n yang akan dipakai pada tahap training adalah 4 supaya kategorinya bervariasi.

Faktanya, jumlah n bisa ditentukan dari awal dengan menentukan jumlah kelas yang ingin diinginkan tanpa perlu melalui tahap percobaan. Semua itu tergantung kebutuhan masing-masing individu.

### a.) K-Means
"""

kmeans = KMeans(n_clusters=4, random_state=321)
kmeans.fit(condition_scaled)

"""### b.) Gaussian Mixture"""

gmm = GaussianMixture(n_components=4, random_state=321)
gmm.fit(condition_scaled)

"""# Model Evaluation"""

condition.head()

df_kmeans = condition.copy()
df_gmm = condition.copy()

"""## 1.) K-Means"""

df_kmeans['category'] = kmeans.fit_predict(condition)
df_kmeans.head()

plt.figure(figsize=[15,10])
sns.scatterplot(data = df_kmeans,
                x = "min_temp", 
                y = "precipitation", 
                hue = df_kmeans['category'], 
                style = df_kmeans['category'], 
                palette = "colorblind", 
                s=100)
plt.suptitle("Sebaran Kategori Berdasarkan Temperatur Minimal dan Tinggi Curah Hujan Harian", size=20)
plt.title("Algoritma K-Means", size=12)
plt.xlabel("Temperatur Minimal (Fahrenheit)")
plt.ylabel("Curah Hujan (Inch)")
plt.show()

"""Data terbagi menjadi 4 kelas, sesuai dengan jumlah n yang sudah ditentukan di tahap sebelumnya. Apabila dilihat dari grafik, kelas-kelas tersebut adalah Hujan pada Musim Semi (Jingga), Hujan pada Musim Panas (Biru), Hujan pada Musim Gugur (Hijau), dan Hujan pada Musim Dingin (Kuning). Karena algoritma k-means termasuk unsupervised learing maka label perlu dituliskan secara manual berdasar pengamatan yang dilakukan.

## 2.) Gaussean Mixture
"""

df_gmm['category'] = gmm.fit_predict(condition)
df_gmm.head()

plt.figure(figsize=[15,10])
sns.scatterplot(data = df_gmm, 
                x = "min_temp", 
                y = "precipitation", 
                hue = df_gmm['category'], 
                style = df_gmm['category'], 
                palette = "colorblind", 
                s=100)
plt.suptitle("Sebaran Kategori Berdasarkan Temperatur Minimal dan Tinggi Curah Hujan Harian", size=20)
plt.title("Algoritma Gaussian Mixture", size=12)
plt.xlabel("Temperatur Minimal (Fahrenheit)")
plt.ylabel("Curah Hujan (Inch)")
plt.show()

"""Data terbagi menjadi 4 kelas, sesuai dengan jumlah n yang sudah ditentukan di tahap sebelumnya. Apabila dilihat dari grafik, kelas-kelas tersebut adalah Tidak Hujan (Biru), Hujan Ringan (Jingga), Hujan Deras (Hijau), dan Hujan Salju (Kuning). Data berwarna kuning diberi label Hujan Salju karena hanya ditemui saat temperatur berada dibawah 50 derajat Fahrenheit (10 derajat Celsius). Perlu diingat bahwa data yang digunakan merupakan hasil observasi di Seattle yang dimana memiliki 4 musim. Karena algoritma gaussian mixture termasuk unsupervised learing maka label perlu dituliskan secara manual berdasar pengamatan yang dilakukan.

# Conclusion

K-Means memang merupakan salah satu metode terfavorit saat menyelesaikan masalah clustering. Tetapi hasil perhitungannya masih meleset dari yang diekspektasikan di awal. Sisi positifnya, model k-means berhasil menyajikan data yang 'tidak terlihat' yaitu mengklasifikasikan curah hujan berdasarkan musim.

Di sisi lain, algoritma Gaussian Mixture berhasil menyajikan data klasifikasi yang sesuai dengan ekspektasi. Sepertinya klasifikasi Hujan Deras (Hijau) bisa dibagi lagi menjadi Hujan Deras dan Badai Salju yang menjadikan jumlah n sama dengan 5. Hal tersebut bisa saja dilakukan seperti yang sudah dituliskan di awal bahwa nilai n bisa menyesuaikan kebutuhan penggunaan.

Tapi mau bagaimana lagi, namanya saja 'Unsupervised Learning' sudah jelas bahwa model akan membuat klasifikasi sesuai apa yang dipelajarinya, terkadang sulit untuk mendapatkan klasifikasi yang sesuai dengan keinginan manusia apalagi sampai 100% akurat berdasar data di lapangan. Sedikit tuning juga diperlukan untuk hasil yang memuaskan. Selain itu, banyak algoritma lainnya yang bisa digunakan untuk clustering yang bisa dicoba.
"""