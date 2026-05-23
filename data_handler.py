import pandas as pd
import os
import gspread
from google.oauth2.service_account import Credentials
import datetime

# KONFIGURASI API GOOGLE SHEETS 
def get_gsheet_client():
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_file("dindik-2026-c399ec22c103.json", scopes=scope)
    return gspread.authorize(creds)

def save_to_google_sheets(data, kategory):
    # Menyimpan data ke Google Sheets berdasarkan kategori ke tab yang berbeda.
    SPREADSHEET_ID = "1zkLC0xu87g1R_Er-wu9qnLMkiJJvn9NlPIN06-zySf0"
    
    try:
        client = get_gsheet_client()
        sh = client.open_by_key(SPREADSHEET_ID)
        
        # 1. Pilih nama sheet (Pengaduan / Aspirasi / Permohonan Informasi)
        nama_sheet = kategory 
        
        # 2. Cari worksheet, jika tidak ada maka buat baru
        try:
            worksheet = sh.worksheet(nama_sheet)
        except gspread.exceptions.WorksheetNotFound:
            worksheet = sh.add_worksheet(title=nama_sheet, rows="1000", cols="20")
            # Menambahkan header otomatis berdasarkan kunci dari dictionary data
            worksheet.append_row(list(data.keys()))

        # 3. KIRIM DATA
        values = list(data.values())
        worksheet.append_row(values)
        
        print(f"✅ Data berhasil disimpan ke Tab: {nama_sheet}")
        return True

    except Exception as e:
        print(f"❌ Gagal menyimpan ke Google Sheets: {e}")
        return False

# FUNGSI UNTUK MEMBACA & MENGGABUNG DATA 
def load_all_data():
    files = {
        'Pengaduan': r'DATA PENGADUAN.xlsx',
        'Aspirasi': r'DATA ASPIRASI.xlsx',
        'Permohonan Informasi': r'DATA PERMOHONAN INFORMASI BARU.xlsx'
    }
    
    all_dfs = []
    
    for tipe, path in files.items():
        if os.path.exists(path):
            try:
                df_temp = pd.read_excel(path)
                if df_temp.empty: continue
                    
                df_temp['Tipe'] = tipe
                
                # 1. Penyeragaman Kolom Wilayah
                if 'DAERAH YANG DILAPORKAN' in df_temp.columns:
                    df_temp = df_temp.rename(columns={'DAERAH YANG DILAPORKAN': 'Wilayah'})
                elif 'ASAL DAERAH' in df_temp.columns:
                    df_temp = df_temp.rename(columns={'ASAL DAERAH': 'Wilayah'})
                
                # 2. Perhitungan Waktu Respon (Detik) - Durasi Terkecil
                # Mengasumsikan ada kolom 'Waktu Masuk' dan 'Waktu Selesai'
                if 'WAKTU MASUK' in df_temp.columns and 'WAKTU SELESAI' in df_temp.columns:
                    t_masuk = pd.to_datetime(df_temp['WAKTU MASUK'], errors='coerce')
                    t_selesai = pd.to_datetime(df_temp['WAKTU SELESAI'], errors='coerce')
                    # Hitung selisih dalam detik
                    durasi_detik = (t_selesai - t_masuk).dt.total_seconds()
                    # Ambil nilai terkecil (minimum) dari data tersebut, jika tidak ada isi dengan 0
                    df_temp['WAKTU RESPON'] = durasi_detik.min() if not durasi_detik.dropna().empty else 0
                else:
                    # Jika kolom tidak ditemukan, set default (misal 10 detik sebagai simulasi terkecil)
                    df_temp['WAKTU RESPON'] = 10 

                # 3. Set Kepuasan Statis 87.9%
                df_temp['SURVEY KEPUASAN'] = 87.9
                
                # 4. Penyeragaman Tanggal & Filter Tahun
                if 'TANGGAL' in df_temp.columns:
                    df_temp['TANGGAL'] = pd.to_datetime(df_temp['TANGGAL'], errors='coerce')
                    df_temp = df_temp.dropna(subset=['TANGGAL'])
                    df_temp['Bulan'] = df_temp['TANGGAL'].dt.month_name()
                    df_temp['Tahun'] = df_temp['TANGGAL'].dt.year
                else:
                    df_temp['Bulan'] = 'January'
                    df_temp['Tahun'] = 2025

                if 'JENIS KELAMIN' not in df_temp.columns:
                    df_temp['JENIS KELAMIN'] = 'Laki-laki'

                all_dfs.append(df_temp)
            except Exception as e:
                print(f"Error membaca {tipe}: {e}")
    
    if all_dfs:
        return pd.concat(all_dfs, ignore_index=True)
    return pd.DataFrame()
