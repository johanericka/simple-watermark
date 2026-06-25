# Simple watermark python script

## Fungsi
- Menambahkan informasi (teks) setelah End of File (EOF)
- Dapat digunakan pada semua format file
- Otomatis di zip untuk menghindari kehilangan data akibat kompresi

## Cara Penggunaan
- Menambahkan teks rahasia (encode)
`python watermark.py encode namafile.pdf "pesan rahasia"`
- Membaca teks rahasia (decode)
`python watermark.py decode namafile`

## Kelemahan
- kompresi file (data rahasia akan hilang karena ditulis setelah EOF)
