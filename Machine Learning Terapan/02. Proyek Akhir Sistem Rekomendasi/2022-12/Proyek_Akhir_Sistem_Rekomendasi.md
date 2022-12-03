# Laporan Proyek Machine Learning - Achmad Noer Aziz

## Project Overview

Terkadang ada masanya dimana seseorang merasa bosan dengan apa yang dikerjakannya berulang-ulang termasuk dalam bermain game. Sangat mungkin terjadi jika seseorang merasa bosan dengan konsep atau desain dari game modern dan memilih untuk bernostalgia dengan game-game klasik. Bermain game klasik bisa membangkitkan ingatan dan memori-memori indah saat masa kanak-kanak dahulu tentang betapa santainya kehidupan sebelum ada tugas yang menumpuk dan sibuknya pekerjaan. Beberapa orang bahkan masih menyimpan konsol lama mereka dan tidak menutup kemungkinan untuk dimainkan kembali. Masalahnya, tidak semua game yang dahulu ramai dipasaran masih diperjual belikan di toko-toko. Atau beberapa dari mereka justru bingung ingin memainkan game yang mana karena terlalu banyak pilihan yang dimiliki.

## Business Understanding

Berdasarkan masalah yang diceritakan sebelumnya, dibuatlah sistem yang bisa merekomendasikan pengguna beberapa game yang kemungkinan disukainya. Cukup dengan menyebutkan game favorit masa kecil, sistem akan merekomendasikan game yang serupa. Tidak hanya game klasik, game modern pun turun ditampilkan oleh sistem rekomendasi ini.

### Problem Statements
- Apa game yang paling disukai oleh masyarakat di seluruh dunia?
- Apa saja game terpopuler berdasarkan pada jumlah penjualan pada genre yang ditentukan?
- Apa saja game yang kemungkinan disukai oleh pengguna berdasarkan game favoritnya?

### Goals
- Menampilkan 3 game dengan skor tertinggi menurut penilaian Metacritic.
- Menampilkan 5 game terlaris pada genre yang sama dengan game favorit pengguna.
- Merekomendasikan 10 game yang mirip dengan game favorit pengguna.

## Data Understanding
Dataset yang berjudul [Video Game Sales with Ratings](https://www.kaggle.com/datasets/rush4ratio/video-game-sales-with-ratings) terdiri dari kumpulan lebih dari  16 ribu data yang berisi daftar video game dengan penjualan diatas 100 ribu salinan. Pengumpulan data dilakukan dengan teknik *web scraping* di [VGChart](https://www.vgchartz.com). Skrip yang digunakan dalam proses *web scraping* bisa dilihat di [GitHub](https://github.com/GregorUT/vgchartzScrape) yang tertulis dalam bahasa *Python*.

### Variabel-variabel pada Video Game Sales dataset adalah sebagai berikut:
- Name : Judul atau nama sebuah video game.
- Platform : Perangkat atau konsol yang compatible untuk menjalankan game.
- Year_of_Release : Tahun dirilisnya sebuah game.
- Genre : Jenis kategori sebuah game.
- Publisher : Perusahaan penerbit game.
- NA_Sales : Jumlah penjualan game di Amerika Utara (satuan juta).
- EU_Sales : Jumlah penjualan game di Eropa (satuan juta).
- JP_Sales : Jumlah penjualan game di Jepang (satuan juta).
- Other_Sales : Jumlah penjualan game di sisa belahan dunia lainnya (satuan juta).
- Global_Sales : Jumlah kumulatif penjualan game di seluruh dunia (satuan juta).
- Critic_Score : Skor penilaian agregat yang dinilai oleh staf Metacritic.
- Critic_Count : Jumlah penilaian yang dilakukan oleh staf Metacritic.
- User_Score : Skor agregat yang dinilai oleh pelanggan Metacritic.
- User_Count : Jumlah penilaian yang dilakukan oleh pelanggan Metacritic.
- Developer : Tim pengembang dari game.
- Rating : Rating lulus sensor yang diberikan oleh [ESRB](https://www.esrb.org/).

### Exploring Data
Terdapat 5 produsen yang terlihat pada Gambar 1, "Multi_Platform" tidak dihitung karena terdiri dari gabungan beberapa konsol. Produsen dengan jumlah game eksklusif terbanyak adalah "Nintendo" dilanjutkan oleh "Sony PlayStation" yang berada tidak jauh dibawahnya. Kedua konsol ini memang cukup populer, sehingga mampu menarik perhatian *developer* dan *publisher* untuk merilis game eksklusif di sana.
| ![Imgur](https://imgur.com/PESGi8B.jpg) |
|:--:|
| Gambar 1. Jumlah game tiap *Platform General* |

Melihat kepada genre di Gambar 2, game Action menjadi game terlaris yang berada di pasaran karena kebanyakan adalah game yang rilis lebih dari satu produsen konsol atau *multi-platform*. Selanjutnya ada genre *Sports* dan *Shooters* menempati posisi dibawah *Action*. Dari ketiga genre yang baru disebutkan, pengaruh dari game *multi-platform* berpengaruh besar terhadap penjualan game secara keseluruhan.
| ![Imgur](https://imgur.com/SbfRT6L.jpg) |
|:--:|
| Gambar 2. Penjualan Global Video Game tiap *Platform* pada Masing-masing *Genre* |

## Data Preparation
Terdapat beberapa tahapan yang dilakukan kepada data sebelum bisa digunakan pada tahapan selanjutnya.
- **Membuang Kolom yang Tidak Digunakan**. Melihat banyaknya kolom yang ada, dipilihlah kolom yang hanya akan berpengaruh terhadap memberikan rekomendasi. Sisanya yang tidak berpengaruh akan dibuang. Atau kolom-kolom jumlah penjualan yang cukup diwakili oleh kolom *Global_Sales* saja.

- **Memeriksa Nilai yang Hilang**. Melihat apakah ada data yang kosong lalu menghapus data tersebut sehingga tidak menggangu pada tahapan selanjutnya.
	|     | Name                     | Platform | Year_of_Release | Genre        | Global_Sales | Critic_Score |
	| --- | ------------------------ | -------- | --------------- | ------------ | ------------ | ------------ |
	|  0  | Super Mario Bros.        | NES      | 1985.0          | Platform     | 40.24        | NaN          |
	|  2  | Pokemon Red/Pokemon Blue | GB       | 1996.0          | Role-Playing | 31.37        | NaN          |
	|  3  | Tetris                   | GB       | 1989.0          | Puzzle       | 30.26        | NaN          |
	| ... | ...                      | ...      | ...             | ...          | ...          | ...          |
	
	Terdapat setidaknya 8000 kolom yang terdeteksi memiliki nilai hilang yang mayoritas berada pada kolom *Critic_Score*. Pilihan satu-satunya adalah dengan cara membuang data tersebut menggunakan fungsi `dropna` milik *library pandas* karena tidak mungkin skor penilaian direkayasa dengan mengisinya dengan nilai *mean* atau *median*.

- **Memeriksa Nilai yang Duplikat**. Melihat apakah ada data yang duplikat sehingga bisa berpengaruh memberikan bias dalam memberikan rekomendasi. Tahapan ini perlu untuk menghindari data yang bias karena duplikasi data itu tadi, sehingga perlu dicek terlebih dahulu. Karena tidak ditemukan data duplikat pada proses ini, maka akan dilanjutkan ke proses selanjutnya. 

- **Mengelompokkan Berdasarkan Platform**. Membuat kolom baru berisi produsen dari *platform* atau konsol.
	```
	Berbagai jenis platform: ['Wii' 'DS' 'X360' 'PS3' 'PS2' '3DS' 'PS4' 'PS' 'XB' 'PC' 'PSP' 'WiiU' 'GC' 'GBA' 'XOne' 'PSV' 'DC']
	```

	```
	Berbagai jenis platform general: ['Nintendo' 'Microsoft_Xbox' 'Sony_Playstation' 'PC' 'Sega']
	```
	|     | Name                  | Platform | Year_of_Release | Genre    | Global_Sales | Critic_Score | Platform_General |
	| --- | --------------------- | -------- | --------------- | -------- | ------------ | ------------ | ---------------- |
	|  0  | Wii Sports            | Wii      | 2006.0          | Sports   | 82.53        | 76.0         | Nintendo         |
	|  2  | Mario Kart Wii        | Wii      | 2008.0          | Racing   | 35.52        | 82.0         | Nintendo         |
	|  3  | Wii Sports Resort     | Wii      | 2009.0          | Sports   | 32.77        | 80.0         | Nintendo         |
	|  6  | New Super Mario Bros. | DS       | 2006.0          | Platform | 29.80        | 89.0         | Nintendo         |
	|  7  | Wii Play              | Wii      | 2006.0          | Misc     | 28.92        | 58.0         | Nintendo         |
	| ... | ...                   | ...      | ...             | ...      | ...          | ...          | ...              |

- **Membersihkan Dataset**. Membersihkan dataset supaya menjadi lebih rapih dan siap dipakai.
	- **Mengubah Tipe Data**. Kolom *Year_of_Release* memiliki tipe data `float64` akan diubah ke tipe data `object` yang akan bersifat kategorikal. Sedangkan kolom "Critic_Score" berisi penilaian bilangan bulat antara 1 sampai 100 lebih cocok apabila diubah ke tipe data `int`.
	
	- **Mengubah Nilai**. Untuk game yang memiliki judul yang sama, nilai di kolom *Platform* dan *Platform_General* diubah menjadi "Multi_Platform". Tahap ini sangat penting pada proses pembersihan data tahap berikutnya.
	
	- **Menggabungkan Berdasarkan Nama**. Beberapa game dirilis pada platform yang berbeda sehingga terekam lebih dari satu. Lebih baik apabila digabungkan menjadi satu lalu menggabungkan seluruh total penjualan dari masing masing platform. Untuk *Critic_Score* akan diambil berdasarkan tahun rilis yang paling awal rilisnya.
	
	- **Mengubah Urutan Kolom**. Memindahkan kolom *Platform_General* supaya bersebelahan dengan kolom *Platform* untuk estetika. Lalu mengatur ulang index menggunakan fungsi `reset_index` dengan parameter `drop=True` milik *library pandas*.

## Modeling
Dibuatlah sistem rekomendasi dengan pendekatan *content-based filtering* yang dimana akan memberikan rekomendasi game serupa berdasarkan game favorit pengguna. Akan ditampilkan juga game dengan skor penilaian tertinggi atau terbaik sepanjang masa dan juga game terlaris berdasarkan genre dari game favorit pengguna.

Pertama-tama, dataset yang sudah siap pakai akan diambil kolom *Genre* dan akan diambil fitur penting atau vektornya menggunakan fungsi `TfidfVectorizer()` milik *library sklearn* lalu diubah ke dalam bentuk matriks. Karena genre bentuknya kategorikal, maka perlu di*encoding* dulu menggunakan teknik *One-Hot Encoding* dengan fungsi `todense()` milik *library sklearn*.

Setelah berhasil mendapatkan fitur, selanjutnya akan dicari nilai kemiripan antar game dengan menghitung derajat kesamaan menggunakan fungsi `cosine_similarity` milik *library sklearn*. Tujuannya untuk mengelompokkan judul game yang berbeda tetapi dengan genre yang sama supaya bisa digunakan untuk memberikan rekomendasi nantinya. Seperti pada Gambar 3, matriks dengan nilai 1 berarti memiliki kesamaan antara game satu dengan yang lainnya, begitupun sebaliknya.
|                                               |MadWorld| ESPN College Hoops |Sega Bass Fishing|Tiger Woods PGA Tour 13| Need for Speed: Porsche Unleashed |
| --------------------------------------------- | ------ | ------------------ | --------------- | --------------------- | --------------------------------- |
|Battlestations: Midway                         | 0.0    | 0.0                | 0.0             | 0.0                   | 0.0                               |
|Uncharted 2: Among Thieves                     | 1.0    | 0.0                | 0.0             | 0.0                   | 0.0                               |
|Real Soccer 2009                               | 0.0    | 1.0                | 1.0             | 1.0                   | 0.0                               |
|Beautiful Katamari                             | 0.0    | 0.0                | 0.0             | 0.0                   | 0.0                               |
|Dynasty Warior 8                               | 0.0    | 0.0                | 0.0             | 0.0                   | 0.0                               |
|Mario Party 6                                  | 0.0    | 0.0                | 0.0             | 0.0                   | 0.0                               |
|Go Vacation                                    | 0.0    | 0.0                | 0.0             | 0.0                   | 0.0                               |
|Doctor Lautrec and the Forgotten Knights       | 0.0    | 0.0                | 0.0             | 0.0                   | 0.0                               |
|Marvel Trading Card Game                       | 0.0    | 0.0                | 0.0             | 0.0                   | 0.0                               |
|Tom Clancy's Rainbow Six: Vegas 2              | 0.0    | 0.0                | 0.0             | 0.0                   | 0.0                               |

Saatnya menguji sistem rekomendasi, cukup memasukan judul game favorit pengguna maka sistem akan memberikan rekomendasinya. Yang pertama ada 3 teratas game dengan rating tertinggi lalu diikuti oleh 5 game terlaris menurut genre yang sama dengan game favorit pengguna. Selanjutnya, barulah ditampilkan 10 rekomendasi game yang mirip dengan game favorit pengguna.

```
dataset[dataset['Name'].eq('Crash Team Racing')]
```
Keluaran:
|   |Name                 |Platform|Platform_General|Year_of_Release|Genre |Global_Sales|Critic_Score|
| - | ------------------- | ------ | -------------- | ------------- | ---- | ---------- | ---------- |
|133|Crash Team Racing    |PS      |Sony_Playstation|1999           |Racing|4.79        |88          |

Anggap saja game favorit salah satu pengguna adalah "Crash Team Racing", game bergenre *Racing* keluaran tahun 1999. Maka sistem akan merekomendasikan game lainnya yang mirip dengan "Crash Team Racing".
```
Top 3 Greatest Games of All Time:
--------------------------------------------------
[Score: 98/100] Grand Theft Auto IV (2008)
[Score: 98/100] Tony Hawk's Pro Skater 2 (2000)
[Score: 98/100] SoulCalibur (1999)
==================================================
Top 5 Best Selling Racing Games of All Time:
--------------------------------------------------
Mario Kart Wii (2008) - Wii
Mario Kart DS (2005) - DS
Gran Turismo 3: A-Spec (2001) - PS2
Mario Kart 7 (2011) - 3DS
Gran Turismo 4 (2004) - PS2
==================================================
Since you play Crash Team Racing,
here are the Top 10 Games you probably like:
--------------------------------------------------
L.A. Rush (2005) - Multi_Platform
MotorStorm: Apocalypse (2011) - PS3
World of Outlaws: Sprint Cars 2002 (2002) - PS2
Racing Gears Advance (2004) - GBA
Hot Wheels Velocity X (2002) - Multi_Platform
Tokyo Xtreme Racer Zero (2000) - PS2
Ford Racing Off Road (2008) - Multi_Platform
Sega GT 2002 (2002) - XB
Sonic Rivals 2 (2007) - PSP
NASCAR 2005: Chase for the Cup (2004) - Multi_Platform
```

## Evaluation
Rekomendasi yang dihasilkan menggunakan "Crash Team Racing" sebagai *input*an, terlihat bahwa 10 game yang direkomendasikan memiliki tema yang sama yaitu balapan atau *Racing*. Begitupun dengan 5 game terlaris pada genre *Racing*, nama-nama yang ditampilkan cukup familiar dan tidak perlu diragukan lagi bahwa mereka adalah game yang paling populer untuk genre *Racing*. Untuk daftar 3 game terbaik sepanjang masa memang tidak dipengaruhi oleh *input*an sehingga hasilnya dapat dinyatakan valid berdasarkan skor yang diraih yaitu 98 dari 100 untuk ketiga game tersebut.
```
Out of a total of 500 recommendation lists,
- Number of relevant recommendations: 425
- Number of irrelevant recommendations: 75
Precision Score = 0.85
```
Untuk mengukur performa sistem dalam memberikan rekomendasi maka perlu dihitung skor presisinya dengan rumus, jumlah data yang relevan dibagi dengan total sampel. Diketahui dari 500 sample, 425 diantaranya termasuk ke dalam rekomendasi yang relevan dan 75 sisanya tidak. Dapat dihitung skor presisinya sebesar 85 persen.

**---Ini adalah bagian akhir laporan---**