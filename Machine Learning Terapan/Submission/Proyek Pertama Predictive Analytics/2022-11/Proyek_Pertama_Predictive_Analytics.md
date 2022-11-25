# Laporan Proyek Machine Learning - Achmad Noer Aziz

## Domain Proyek
Perubahan cuaca yang ekstrem membuat semua orang waspada terhadap kemungkinan cuaca yang akan datang khususnya hujan. Saat cuaca cerah atau berawan tiap individu pasti akan beraktivitas dengan santai seperti biasa. Tetapi saat hujan, semua bisa jadi berbeda dimulai dari pakaian yang dikenakan, jenis alas kaki yang digunakan, perlunya membawa payung atau jas hujan, sampai menetap di dalam rumah.

Semua hal tersebut perlu diobservasi terlebih dahulu. Dimulai adanya hujan atau tidak sampai seberapa derasnya hujan yang terjadi. Belum lagi apabila sedang berada di luar negeri yang mempunyai 4 musim, berbeda dengan Indonesia yang hanya mempunyai 2 musim. Pasti akan lebih kompleks lagi cara observasi keadaan sekitar. Ditambah lagi ramalan cuaca yang tidak bisa menjamin 100 persen akurat. Oleh karena itu, tiap individu harus sadar akan situasi dan kondisi lingkungan, jangan sampai keliru untuk mengenakan jas hujan di saat tidak ada hujan atau saat cuaca sedang cerah.

## Business Understanding
Berdasarkan masalah yang diceritakan sebelumnya, perlu dibuat kategori terhadap kondisi cuaca diambil dari data klimatologi seperti tingginya curah hujan dan temperatur udara. Tujuannya supaya tiap individu bisa menentukan pakaian atau perlengkapan seperti apa yang perlu dibawa contohnya jaket, payung, dan jas hujan.

### Problem Statements
- Berapa banyak jumlah kategori cuaca yang bisa dikelompokkan?
- Apa nama yang tepat dari masing-masing kategori cuaca berdasar tinggi curah hujan dan temperatur pada saat itu?

### Goals
- Menghitung dan memperkirakan jumlah kategori hujan dengan menggunakan bantuan teknik *Elbow Curve*.
- Menganalisa data atau grafik yang dihasilkan oleh komputasi dari algoritma *K-Means* dan *Gaussian Mixture*, kemudian memberi label secara manual sesuai nama yang cocok kepada tiap-tiap kategori hujan.

## Data Understanding
Dataset ini merupakan rekaman data klimatologi harian di Seattle, Amerika Serikat dari tahun 1948 hingga 2017. Terdapat 5 variabel yang dicatat dalam observasi.
[Kaggle Dataset](https://www.kaggle.com/datasets/rtatman/did-it-rain-in-seattle-19482017)

### Variabel-variabel pada Rain in Seattle dataset adalah sebagai berikut:
- DATE = Tanggal dilakukannya observasi (YYYY-MM-DD)
- PRCP = Intensitas curah hujan dalam satu hari (Inci)
- TMAX = Temperatur tertinggi dalam satu hari (Fahrenheit)
- TMIN = Temperatur terendah dalam satu hari (Fahrenheit)
- RAIN = Hasil observasi Ada atau Tidak adanya hujan (True/False)

## Data Preparation
Terdapat beberapa tahapan yang dilakukan kepada data sebelum bisa digunakan pada tahapan selanjutnya.

- **Memeriksa Nilai yang Hilang.** Melihat apakah ada data yang kosong lalu menghapus data tersebut sehingga tidak menggangu pada tahapan selanjutnya.

	|       | DATE       | PRCP | TMAX | TMIN | RAIN |
	| ----- | ---------- | ---- | ---- | ---- | ---- |
	| 18415 | 1998-06-02 | NaN  | 72   | 52   | NaN  |
	| 18416 | 1998-06-03 | NaN  | 66   | 51   | NaN  |
	| 21067 | 2005-09-05 | NaN  | 70   | 52   | NaN  |

	Terdapat 3 data yang mengandung data kosong. Ada beberapa opsi yang bisa dilakukan untuk menanganinya, salah satunya adalah dengan cara menghapus 3 data tersebut dengan fungsi `dropna` milik *library pandas*. Berhubung data yang dihapus hanya 3, sangat kecil dibandingkan dengan total data di dataset, maka dirasa aman untuk dihapus secara cuma-cuma.

- **Memeriksa Nilai yang Duplikat.** Melihat apakah ada data yang duplikat sehingga bisa berpengaruh pada tahapan selanjutnya.

	Tahapan ini perlu untuk menghindari data yang bias karena duplikasi data itu tadi, sehingga perlu dicek terlebih dahulu. Karena tidak ditemukan data duplikat pada proses ini, maka akan dilanjutkan ke proses selanjutnya. 
	
- **Membuang Kolom yang Tidak Digunakan.** Memilah kolom yang representatif lalu membuang yang sekiranya tidak memiliki pengaruh yang banyak pada tahapan selanjutnya.

	|     | PRCP  | TMAX | TMIN |
	| --- | ----- | ---- | ---- |
	|  0  | 0.47  | 51   | 42   |
	|  1  | 0.59  | 45   | 36   |
	|  2  | 0.42  | 45   | 35   |
	| ... | ...   | ...  | ...  |
	
	Kolom *DATE* yang berisi tanggal dianggap tidak berpengaruh terhadap tinggi atau rendahnya curah hujan ataupun temperatur sehingga bisa dihapus. Sedangkan kolom *RAIN* dihapus karena nilainya sangat dipengaruhi oleh nilai pada kolom *PRCP*, sehingga sudah cukup diwakili oleh 1 kolom saja. 
	
- **Mengubah Nama Kolom.** Mengganti nama kolom ke nama yang lebih representatif agar mudah dipahami.

	Kolom yang tersisa hanya 3 yaitu, *PRCP*, *TMAX*, dan *TMIN*. Supaya mudah dipahami, maka nama dari ketiga kolom tersebut perlu diganti.
	- Kolom *PRCP* diganti menjadi *precipitation*
	- Kolom *TMAX* diganti menjadi *max_temp*
	- Kolom *TMIN* diganti menjadi *min_temp*


- **Membuang *Outlier*.** Menghilangkan *outlier* supaya data menjadi lebih seragam dengan membuang data-data anomali.

	| ![Imgur](https://imgur.com/WjIqT3H.jpg) |
	|:--:|
	| Gambar 4.1 Memvisualisasikan sebaran data dengan *Box Plot* |

	*Outlier* merupakan data-data yang sifatnya tidak biasa atau berbeda dari data atau kondisi yang umum terjadi. Maka dari itu, *outlier* perlu dihapus supaya data-data yang digunakan pada proses selanjutnya memiliki keseragaman. Teknik yang digunakan untuk menghapus *outlier* adalah IQR (*Inter Quartile Range*). Pada Gambar 4.1 terlihat terdapat banyak titik-titik hitam, itulah yang disebut *outlier* karena nilainya lebih kecil dari kuartal 1 dan lebih besar dari kuartal 3.

## Modeling
Pada tahap ini akan mengembangkan model *machine learning* dengan menggunakan algoritma *K-Means* yang sudah sangat populer untuk masalah *clustering*. Kemudian, akan membandingkan hasil *clustering* dengan algoritma yang lain yaitu *Gaussian Mixture Model* (GMM). Kedua algoritma ini termasuk ke dalam *Unsupervied Learning*, *clustering* bertugas untuk mengelompokkan data berdasarkan pengetahuan yang mereka pelajari dari data.

*K-Means* bekerja dengan cara menaruh *centroid* ditempat yang acak lalu terus memperbarui lokasinya tiap iterasinya sampai nilai galatnya sudah kecil atau posisi *centroid* tidak bisa berpindah lagi. Jumlah *centroid* dipengaruhi oleh parameter `n_cluster` yang diisi, dan bisa dibilang juga bahwa *centroid* adalah titik pusat dari sebuah *cluster* atau kelompok.

*Gaussian Mixture Model* (GMM) dikenal oleh peminat *machine learning* karena kemampuannya dalam mengklasifikasikan data yang sebarannya padat atau berkumpul pada satu tempat. GMM secara *default* menggunakan *hyperparameter* `kmeans` yang dimana memanfaatkan kecepatan pemrosesan K-Means untuk mencapai nilai konvergen. 

Saat melakukan *clustering*, dibutuhkan parameter **n** yang dimana menentukan jumlah kategori dan bisa menggunakan bantuan teknik *Elbow Curve* untuk mendapatkan nilai **n** tersebut. 

| ![Imgur](https://imgur.com/blTc269.jpg) |
|:--:|
| Gambar 5.1 Hasil perhitungan nilai n oleh *Elbow Curve* |

Setelah dilakukan pengujian menggunakan metode *Elbow Curve* barulah bisa dilihat di Gambar 5.1 bahwa kurva mulai melandai pada **n** ke 2, 3, 4 dan terlihat lurus pada **n** yang seterusnya. Maka dari itu, **n** yang akan dipakai pada tahap training adalah **4**, berlaku untuk kedua algoritma yang digunakan.

Kemudian nilai **n** sama dengan **4** dimasukkan ke parameter `n_clusters` pada algoritma *K-Means* dan parameter `n_components` pada algoritma *Gaussian Mizture*. Kedua parameter menggunakan parameter `random_state` bernilai **123** dengan tujuan supaya hasil *clustering* selalu sama walaupun kode dijalankan berkali-kali.

Sebenarnya jumlah **n** bisa ditentukan dari awal dengan menentukan jumlah kelas yang ingin diinginkan tanpa perlu melalui tahap percobaan, semua itu tergantung kebutuhan masing-masing individu. Tetapi pada kali ini dipasrahkan semuanya kepada kemampuan *Elbow Curve* dalam mencari nilai **n**.

## Evaluation
Pada bagian ini akan mengulas hasil *clustering* yang dilakukan oleh algoritma *K-Means* dan algoritma *Gaussian Mixture*.

***K-Means*** 
Data terbagi menjadi 4 kelas, sesuai dengan jumlah n yang sudah ditentukan di tahap sebelumnya. 

| ![Imgur](https://imgur.com/KNQWQXD.jpg) |
|:--:|
| Gambar 6.1 Sebaran Kategori menurut Algoritma *K-Means* |

Apabila dilihat di Gambar 6.1, kelas-kelas yang telah dikelompokkan adalah Hujan pada Musim Semi (Jingga 🟠), Hujan pada Musim Panas (Biru 🔵), Hujan pada Musim Gugur (Hijau 🟢), dan Hujan pada Musim Dingin (Kuning 🟡). Karena algoritma *K-Means* termasuk *unsupervised learing* maka label perlu dituliskan secara manual berdasar pengamatan yang dilakukan.

*K-Means* memang merupakan salah satu metode terfavorit saat menyelesaikan masalah *clustering*. Tetapi hasil perhitungannya masih terlihat berantakan. Sisi positifnya, model *K-Means* berhasil menyajikan data yang 'tidak terlihat' yaitu mengklasifikasikan curah hujan berdasarkan musim. Untuk mendapatkan hasil yang baik, perlu melakukan pelatihan dan percobaan berulang-ulang dengan cara menghapus parameter `random_state` supaya hasilnya bisa bervariasi hingga dirasa sudah sesuai.

Bicara soal kecepatan, K-Means sudah tidak perlu diragukan, ditambah lagi kemampuannya dalam belajar dari kesalahan yang dimana akan memperbarui posisi *centroid* setiap iterasinya. Sayangnya masih kurang kuat dalam menangani data yang sebarannya padat atau berkumpul di satu tempat.

***Gaussian Mixture***
Data terbagi menjadi 4 kelas, sesuai dengan jumlah n yang sudah ditentukan di tahap sebelumnya.

| ![Imgur](https://imgur.com/GtsEyTg.jpg) |
|:--:|
| Gambar 6.2 Sebaran Kategori menurut Algoritma *Gaussian Mixture* |

Apabila dilihat di Gambar 6.2, kelas-kelas yang telah dikelompokkan adalah Tidak Hujan (Biru 🔵), Hujan Ringan (Jingga 🟠), Hujan Deras (Hijau 🟢), dan Hujan Salju (Kuning 🟡). Data berwarna kuning diberi label Hujan Salju karena hanya ditemui saat temperatur berada dibawah 50 derajat Fahrenheit (10 derajat Celsius). Perlu diingat bahwa data yang digunakan merupakan hasil observasi di Seattle yang dimana memiliki 4 musim. Karena algoritma *Gaussian Mixture* termasuk *unsupervised learing* maka label perlu dituliskan secara manual berdasar pengamatan yang dilakukan.

Di sisi lain, algoritma *Gaussian Mixture* berhasil menyajikan data klasifikasi yang rapih. Sepertinya klasifikasi Hujan Deras (Hijau) bisa dibagi lagi menjadi Hujan Deras dan Badai Salju yang menjadikan jumlah n sama dengan 5. Hal tersebut bisa saja dilakukan mengikuti kebutuhan penggunaan.

Melihat kepada ketepatan dalam menyelesaikan masalah, algoritma *Gaussian Mixture Model* (GMM) bisa dinyatakan lebih baik dibandingkan dengan algoritma *K-Means*. Kategori jenis hujan yang diklasifikasikan cukup representatif dengan fakta di lapangan. Sifatnya yang fleksibel membuat algoritma ini mampu menghadapi data yang sebarannya padat atau tidak tersebar.

**---Ini adalah bagian akhir laporan---**