import sys
import os
import zipfile

# Penanda rahasia untuk melacak posisi pesan di dalam file biner
MARKER_RAHASIA = b"__FORENSIK_MARKER_2026__"

def cetak_panduan():
    print("\nFormat Penggunaan (Semua type file):")
    print("1. Untuk ENCODE (Menanam Pesan & Otomatis ZIP):")
    print("   python watermark.py encode [input] \"[pesan]\"")
    print("   Contoh: python watermark.py encode ktp.jpg \"dokumen diminta oleh Fulan\"")
    print("\n2. Untuk DECODE (Memeriksa File):")
    print("   python watermark.py decode [input]")
    print("   Contoh: python watermark.py decode ktp_encoded.jpg")
    print("   *Catatan: Ekstrak dulu file .zip yang Anda terima sebelum melakukan decode.\n")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        cetak_panduan()
        sys.exit(1)

    mode = sys.argv[1].lower()
    input_file = sys.argv[2]

    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' tidak ditemukan!")
        sys.exit(1)

    # =====================================================================
    # MODE 1: ENCODE (TANAM PESAN & BUNGKUS ZIP)
    # =====================================================================
    if mode == "encode":
        if len(sys.argv) < 4:
            print("Error: Pesan yang ingin ditanam belum dimasukkan!")
            cetak_panduan()
            sys.exit(1)
            
        pesan = sys.argv[3]
        
        # Format nama file output otomatis
        nama_asli, ekstensi = os.path.splitext(input_file)
        file_encoded = f"{nama_asli}{ekstensi}"
        file_zip_output = f"{nama_asli}.zip"
        
        print("\n--- PROSES PENANAMAN & PROTEKSI ZIP START ---")
        print(f"File Input    : {input_file}")
        print(f"Pesan Ditanam : \"{pesan}\"")
        
        # 1. Baca data biner asli
        with open(input_file, "rb") as f:
            data_asli = f.read()
            
        if MARKER_RAHASIA in data_asli:
            print("Peringatan: File ini sudah memiliki watermark tersembunyi!")
            sys.exit(1)
            
        # 2. Sisipkan pesan teks di akhir struktur biner file
        data_encoded = data_asli + MARKER_RAHASIA + pesan.encode('utf-8')
        
        # 3. Simpan file ber-watermark sementara
        with open(file_encoded, "wb") as f_out:
            f_out.write(data_encoded)
            
        # 4. Bungkus file ber-watermark tersebut ke dalam arsip ZIP agar aman dari WhatsApp
        print(f"Mengunci file '{file_encoded}' ke format ZIP...")
        with zipfile.ZipFile(file_zip_output, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(file_encoded, os.path.basename(file_encoded))
            
        # Hapus file sementara '_encoded' agar folder Anda tetap rapi (opsional)
        if os.path.exists(file_encoded):
            os.remove(file_encoded)
            
        print(f"Sukses! Silahkan kirim file zip ini.\n")

    # =====================================================================
    # MODE 2: DECODE (MEMERIKSA FILE SETELAH DI-EKSTRAK DARI ZIP)
    # =====================================================================
    elif mode == "decode":
        # Proteksi jika pengguna langsung memasukkan file .zip secara tidak sengaja
        if input_file.endswith('.zip'):
            print("Peringatan: Harap ekstrak (unzip) terlebih dahulu file tersebut,")
            print("lalu jalankan decode pada file gambar/dokumen hasil ekstraknya.")
            sys.exit(1)
            
        print("\n--- PROSES PEMERIKSAAN FORENSIK START ---")
        print(f"File di-Scan  : {input_file}")
        
        with open(input_file, "rb") as f:
            konten_file = f.read()
            
        posisi_marker = konten_file.find(MARKER_RAHASIA)
        
        print("\n=== HASIL SCAN SOFTWARE ===")
        if posisi_marker != -1:
            posisi_awal_pesan = posisi_marker + len(MARKER_RAHASIA)
            data_pesan_bytes = konten_file[posisi_awal_pesan:]
            
            try:
                pesan_terbongkar = data_pesan_bytes.decode('utf-8')
                print(f"Teks Tersembunyi Ditemukan:")
                print(f"\"{pesan_terbongkar}\"")
            except UnicodeDecodeError:
                print("Marker ditemukan, tetapi struktur teks di dalamnya rusak.")
        else:
            print("File Bersih. Tidak ditemukan tanda air forensik pada file ini.")
        print("===========================\n")
        
    else:
        print("Error: Mode tidak dikenal!")
        cetak_panduan()

