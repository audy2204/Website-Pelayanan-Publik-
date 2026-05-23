import streamlit as st
from streamlit_option_menu import option_menu
from datetime import datetime
from data_handler import save_to_google_sheets

# REGISTRASI POP-UP DIALOG UNTUK SURVEI 
@st.dialog("Survei Kepuasan Pelayanan")
def pop_up_survei(kategori_laporan, data_mentah):
    # CSS khusus agar semua elemen p di dalam dialog ini berwarna HITAM
    st.markdown(
        """
        <style>
        div[data-testid="stDialog"] p, #text-survei {
            color: #000000 !important;
            font-weight: 600 !important;
            font-size: 16px !important;
            text-shadow: none !important; /* Hapus shadow agar teks putih bersih di latar belakang putih */
        }

        div[data-testid="stDialog"] [data-testid="stNotification"] p {
            color: #000000 !important;
            font-weight: 600 !important;
            text-shadow: none !important;
        }
        </style>
        """, 
        unsafe_allow_html=True
    )
    
    # Berikan id="text-survei" pada teks pertanyaan
    st.markdown('<p id="text-survei">Bagaimana pengalaman Anda menggunakan sistem pelayanan publik kami?</p>', unsafe_allow_html=True)
    
    # Widget feedback bintang 1-5
    rating_idx = st.feedback("stars")
    
    if rating_idx is not None:
        mapping_kepuasan = {
            0: "Sangat Tidak Puas",
            1: "Tidak Puas",
            2: "Cukup Puas",
            3: "Puas",
            4: "Sangat Puas"
        }
        teks_kepuasan = mapping_kepuasan[rating_idx]
        
        data_final = data_mentah.copy() 
        data_final["Kepuasan Pelanggan"] = teks_kepuasan
        
        sukses = save_to_google_sheets(data_final, kategori_laporan)
        
        if sukses:
            st.success(f"Terima kasih! Penilaian '{teks_kepuasan}' Anda telah direkam. Laporan berhasil dikirim! 🙏")
            st.session_state.buka_survei = False
            st.session_state.data_terpilih = None
            st.rerun()

def render_form_input():
    st.write("##")
    st.markdown("<h1 style='text-align: center;'>Pelayanan Publik Dinas Pendidikan Jawa Timur</h1>", unsafe_allow_html=True)
    st.write("##") 

    col1, col2, col3 = st.columns([1, 5, 1]) 
    
    with col2:
        st.markdown("<div style='padding: 10px;'>", unsafe_allow_html=True)

        # Navigasi Internal Form
        menu_form = option_menu(
            menu_title=None, 
            options=["Permohonan Informasi", "Aspirasi", "Pengaduan"], 
            icons=["info-circle", "chat-left-text", "exclamation-triangle"], 
            default_index=0,
            orientation="horizontal",
            styles={
                "container": {
                    "padding": "0px !important",        
                    "margin": "0px !important",        
                    "background-color": "transparent",       
                    "border-radius": "50px",          
                },
                "nav-link": {
                    "font-size": "20px", 
                    "text-align": "center", 
                    "margin": "0px", 
                    "border-radius": "50px",            # Agar saat hover/pindah sudutnya melengkung
                    "padding": "10px",
                    "text-shadow": "1px 1px 2px rgba(0,0,0,0.5)"
                },
                "nav-link-selected": {
                    "background-color": "#5d9ef3db",      
                    "border-radius": "0px",          
                },
            }
        )

        # State Manajemen untuk AI dan Pop-up Survei
        if 'tampilkan_ai' not in st.session_state:
            st.session_state.tampilkan_ai = False
            st.session_state.judul_ai = ""
        if 'buka_survei' not in st.session_state:
            st.session_state.buka_survei = False
            st.session_state.data_terpilih = None
            st.session_state.kategori_terpilih = ""

        with st.form("main_form", clear_on_submit=True):
            today = datetime.now().date()
            
            if menu_form == "Permohonan Informasi":
                st.date_input("Tanggal Laporan (Otomatis)", value=today, disabled=True)
                nama_pelapor = st.text_input("Nama Lengkap")
                jk = st.radio("Jenis Kelamin", ["Laki-laki", "Perempuan"], horizontal=True)
                wilayah = st.selectbox("Wilayah Asal", ["Surabaya", "Malang", "Sidoarjo", "Gresik", "Lainnya"])
                pekerjaan = st.text_input("Pekerjaan")
                no_telp = st.text_input("Nomor Telepon")
                judul = st.text_input("Judul Permohonan Informasi")
                isi = st.text_area("Deskripsi Informasi yang Dibutuhkan")
                lampiran = st.file_uploader("Upload Lampiran Pendukung", type=['png', 'jpg', 'pdf'])
                kategori = "Permohonan Informasi"

            elif menu_form == "Aspirasi":
                st.date_input("Tanggal Laporan (Otomatis)", value=today, disabled=True)
                nama_pelapor = st.text_input("Nama Lengkap")
                jk = st.radio("Jenis Kelamin", ["Laki-laki", "Perempuan"], horizontal=True)
                wilayah = st.selectbox("Wilayah Asal", ["Surabaya", "Malang", "Sidoarjo", "Gresik", "Lainnya"])
                pekerjaan = st.text_input("Pekerjaan")
                no_telp = st.text_input("Nomor Telepon")
                judul = st.text_input("Judul Aspirasi")
                isi = st.text_area("Deskripsi Aspirasi")
                lampiran = st.file_uploader("Upload Lampiran", type=['png', 'jpg', 'pdf'])
                kategori = "Aspirasi"

            else:
                st.date_input("Tanggal Laporan (Otomatis)", value=today, disabled=True)
                tgl_kejadian = st.date_input("Tanggal Kejadian", value=today)
                opsi_nama = st.radio("Metode Pelaporan", ["Nama Asli", "Anonim"], horizontal=True)
                nama_pelapor = st.text_input("Nama Pelapor") if opsi_nama == "Nama Asli" else "Anonim"
                wilayah = st.selectbox("Wilayah yang Dilaporkan", ["Surabaya", "Malang", "Sidoarjo", "Gresik", "Lainnya"])
                judul = st.text_input("Judul Laporan Pengaduan")
                isi = st.text_area("Deskripsi Laporan")
                lampiran = st.file_uploader("Upload Lampiran", type=['png', 'jpg', 'pdf'])
                kategori = "Pengaduan"

            st.write("---")
            submit = st.form_submit_button("Kirim Laporan", use_container_width=True)

            if submit:
                jk = locals().get('jk', "-")
                pekerjaan = locals().get('pekerjaan', "-")
                no_telp = locals().get('no_telp', "-")
                tgl_kejadian = str(locals().get('tgl_kejadian', "-"))

                data_simpan = {
                    "Tanggal Input": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Kategori": kategori,
                    "Nama Pelapor": nama_pelapor,
                    "Wilayah": wilayah,
                    "Judul": judul,
                    "Isi Laporan": isi,
                    "Jenis Kelamin": jk,
                    "Pekerjaan": pekerjaan,
                    "No Telp": no_telp,
                    "Tanggal Kejadian": str(tgl_kejadian), 
                    "Status": "Terkirim",
                    "Kepuasan Pelanggan": "-"
                }
                
                # Cek jika ada lampiran
                nama_file = lampiran.name if lampiran is not None else "Tidak ada lampiran"
                data_simpan["Lampiran"] = nama_file
                
                # Simpan data di memori session state terlebih dahulu
                st.session_state.data_terpilih = data_simpan
                st.session_state.kategori_terpilih = kategori
                
                if kategori == "Permohonan Informasi":
                    st.session_state.tampilkan_ai = True
                    st.session_state.judul_ai = judul
                    st.session_state.buka_survei = False
                else:
                    # Jika Aspirasi atau Pengaduan, langsung arahkan pemicu pop-up survei
                    st.session_state.buka_survei = True
                    
                st.rerun()

        # LOGIKA KHUSUS MENU INFORMASI (Similarity Check)
        if menu_form == "Permohonan Informasi" and st.session_state.tampilkan_ai:
            st.markdown("---")
            st.subheader("🤖 Jawaban Otomatis")
            
            judul_lower = st.session_state.judul_ai.lower()
            
            if "ijazah" in judul_lower or "legalisir" in judul_lower:
                jawaban = """
                Berikut adalah alur dan prosedur rekomendasi berdasarkan hasil analisis judul yang Anda ajukan:<br>
                1. Apabila wilayah pada <b>KTP dan Ijazah</b> pemohon berada dalam satu <b>daerah yang sama</b>, pemohon diarahkan untuk melakukan pengurusan secara langsung di <b>Kantor Cabang Dinas Pendidikan Wilayah Kabupaten/Kota setempat.</b> <br>
                2. Namun, apabila terdapat <b>perbedaan wilayah antara KTP dan Ijazah,</b> pemohon diberikan fleksibilitas untuk mengunjungi <b>satu Kantor Cabang Dinas Pendidikan Wilayah Kabupaten/Kota yang paling sesuai dengan domisili KTP atau lokasi penerbitan Ijazah saat ini.</b>
                """
            elif "ppdb" in judul_lower:
                jawaban = "Informasi PPDB 2026 dapat diakses melalui website resmi ppdb.jatimprov.go.id atau melalui cabang dinas wilayah setempat."
            elif "mutasi" in judul_lower:
                jawaban = "Proses mutasi siswa memerlukan surat keterangan pindah dari sekolah asal dan surat penerimaan dari sekolah tujuan yang disahkan oleh Dindik."
            else:
                jawaban = "Mohon maaf, asisten AI tidak menemukan jawaban otomatis yang spesifik untuk judul tersebut. Namun jangan khawatir, petugas kami akan segera meninjau dan memproses permohonan Anda."

            # Menggunakan Kotak Kustom dengan Background Pekat & Shadow Tajam 
            st.markdown(
                f"""
                <div style="
                    background-color: rgba(0, 0, 0, 0.75); 
                    padding: 20px; 
                    border-radius: 10px; 
                    border-left: 5px solid #5d9ef3;
                    margin-bottom: 20px;
                ">
                    <strong style="
                        color: white; 
                        font-size: 18px; 
                        text-shadow: 2px 2px 3px rgba(0,0,0,1);
                    ">
                        🙏 Terima Kasih Telah Menghubungi Dinas Pendidikan Provinsi Jawa Timur.
                    </strong>
                    <p style="
                        color: white; 
                        font-size: 15px; 
                        line-height: 1.6; 
                        margin-top: 10px; 
                        text-shadow: 2px 2px 4px rgba(0, 0, 0, 1), -1px -1px 0px rgba(0,0,0,1);
                        font-weight: 500;
                    ">
                        {jawaban}
                    </p>
                </div>
                """, 
                unsafe_allow_html=True
            )
            
            st.warning("⚠️ **Belum puas dengan jawaban template di atas?**")
            st.markdown("""
                Jika informasi prosedur di atas kurang jelas atau kasus Anda memerlukan penanganan khusus, 
                silakan hubungi layanan bantuan langsung melalui WhatsApp resmi kami: 
                
                👉 [**Hubungi Hotline Dindik Jatim (WhatsApp)**](https://wa.me/628123456789)
            """)
            
            st.write("##")
            btn_selesai = st.button("Saya Sudah Membaca & Lanjutkan ke Survei Kepuasan", use_container_width=True)
            if btn_selesai:
                st.session_state.tampilkan_ai = False  # Matikan tampilan AI
                st.session_state.buka_survei = True    # Nyalakan trigger pop-up survei
                st.rerun()
                
                # PEMICU DIALOG POP-UP SURVEI 
        if st.session_state.buka_survei and st.session_state.data_terpilih is not None:
            pop_up_survei(st.session_state.kategori_terpilih, st.session_state.data_terpilih)
    st.markdown("</div>", unsafe_allow_html=True)