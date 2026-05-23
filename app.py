import streamlit as st
from turtle import color
from streamlit_option_menu import option_menu
from data_handler import load_all_data
from form_input import render_form_input
from visualisasi import render_visualisasi
import base64

# KONFIGURASI HALAMAN
st.set_page_config(page_title="Sistem Pelayanan Publik Dindik Jatim", layout="wide")

# mengubah gambar lokal ke Base64
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

bin_str = get_base64('bg.jpg')

# CSS CUSTOM
st.markdown(f"""
    <style>
    .main .block-container {{
    background-color: transparent !important;
    }}
    
    /*Foto Background*/
    .stApp {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        background-repeat: no-repeat;
    }}

    /*memberikan lapisan warna tipis di atas foto sebelum elemen lain*/
    .stApp::before {{
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.2); /* Gelapkan foto sedikit (20%) */
        z-index: -1;
    }}

    /* Menghilangkan background putih di SEMUA kontainer kolum dan form */
    [data-testid="stVerticalBlock"] > div, 
    [data-testid="stColumn"], 
    .stForm, 
    div[data-testid="stExpander"] {{
        background-color: transparent !important;
        background: transparent !important;
    }}

    /* Memberikan efek kaca hanya pada bingkai terluar form */
    .stForm {{
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(10px) saturate(180%) !important;
        border-radius: 20px !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        padding: 30px !important;
    }}

    /* Menghilangkan background putih pada navigasi iframe */
    iframe[title="streamlit_option_menu.option_menu"] {{
        background-color: transparent !important;
    }}

    /* Menyesuaikan warna teks agar terlihat di atas foto */
    h1, h2, Markdown, [data-testid="stMetricLabel"] {{
        color: white !important;
        font-size: 50px !important;    
        font-weight: bold;  
        text-shadow: 5px 5px 5px rgba(10.0,10.0,10.0,10.0);
    }}

    /* Menyesuaikan warna teks agar terlihat di atas foto */
    h3, .stMarkdown, [data-testid="stMetricLabel"] {{
        color: white !important;
        font-size: 30px !important;    
        font-weight: bold;  
        text-shadow: 5px 5px 5px rgba(10.0,10.0,10.0,10.0);
    }}

    /* Mengatur warna dan ukuran teks judul di atas kotak input */
    [data-testid="stWidgetLabel"] p {{
        color: white !important;       
        font-size: 21px !important;   
        font-weight: bold;            
        text-shadow: 1px 1px 2px rgba(0,0,0,1.0);
    }}

    /* Mengatur teks di DALAM kotak input */
    .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {{
        color: black !important;      
        font-size: 20px !important;  
    }}

    /* Mengatur warna teks di samping tombol radio */
    div[data-testid="stMarkdownContainer"] p {{
        color: white !important;
        font-size: 21px !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,1.0);
    }}

    /* Mengatur warna lingkaran saat dipilih */
    div[data-testid="stRadioButton"] label span[data-baseweb="radio"] div {{
        background-color: #1a73e8 !important; 
    }}

    /* Membuat Input Form tetap bersih */
    .stTextInput>div>div, .stTextArea>div>div {{
        background-color: rgba(255, 255, 255, 0.8) !important;
        color: black !important;
    }}
    
    /* Menyejajarkan elemen di Header secara vertikal */
    [data-testid="stHorizontalBlock"] {{
        align-items: center;
    }}

    /* Ganti CSS Tombol Login di app.py */
    div[data-testid="stButton"] button {{
        background-color: #0080FF !important; 
        color: black !important;              
        border: none !important;
        height: 45px !important;
        border-radius: 10px !important;
        width: 100% !important;
    }}

    /* Ganti CSS Tombol Login di app.py */
    div[data-testid="stForm"] button {{
        background-color: #0080FF !important;
        color: black !important;             
        border: none !important;
        height: 45px !important;
        border-radius: 10px !important;
        width: 100% !important;
    }}

    /* Menghilangkan background blur besar yang menutupi seluruh halaman */
    div[data-testid="stVerticalBlockBorderWrapper"] {{
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }}

    /*button browser file tetap putih*/
    div[data-testid="stFileUploader"] button {{
        background-color: #ffffff !important;
        color: #31333F !important;
    }}

    /* Membuat label metrik dan angkanya berwarna putih agar kontras dengan background gelap */
    [data-testid="stMetricLabel"] p {{
        color: #1a73e8 !important; 
        font-size: 18px !important;
        font-weight: bold !important;
    }}

    [data-testid="stMetricValue"] {{
        color: white !important; /* Angka metrik putih */
        font-weight: bold !important;
    }}

    /* Menargetkan elemen toast */
    div[data-testid="stToast"] {{
        background-color: #0080FF !important; 
        color: white !important;             
        border-radius: 10px;
    }}

    /* Menargetkan teks judul/label metrik (seperti "Total Laporan", "Pengaduan") */
        [data-testid="stMetricLabel"]{{
        color: white !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8), -1px -1px 0px rgba(0, 0, 0, 0.8) !important;
        font-weight: bold !important;
    }}
    
    /* Menargetkan angka/nilai metrik (seperti jumlah total laporan) */
    [data-testid="stMetricValue"] {{
        color: white !important;
        text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.9), -1px -1px 0px rgba(0, 0, 0, 0.9) !important;
        font-weight: bold !important;
    }}

    </style>
    """, unsafe_allow_html=True)

# NAVIGASI UTAMA 
col_logo, col_menu, col_login = st.columns([1.5, 7, 1.5])

with col_logo:
    st.image("logo.jpg", width=300)

with col_menu:
    selected = option_menu(
        menu_title=None,
        options=["Dashboard Utama", "Data & Analisis"],
        icons=["house", "graph-up"],
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {
                "padding": "0!important",
                "background-color": "transparent",
            },
            "nav-link": {
                "font-size": "16px",
                "color": "#1a73e8",       
                "text-align": "center",
                "margin": "0px 30px",     # Jarak antar teks agar garis bawah tidak tabrakan
                "padding": "5px 0px",    
                "text-transform": "uppercase",
                "font-weight": "bold",
            },
            "nav-link-selected": {
                "background-color": "transparent",
                "color": "#1a73e8",
                "font-weight": "bold",
                "border-bottom": "3px solid #1a73e8",
                "border-radius": "0px"
            }
        }
    )

with col_login:
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    if st.button("Login", key="btn-login", use_container_width=True):
        st.toast("Fitur Login Admin segera hadir!")
    st.markdown('</div>', unsafe_allow_html=True)

df = load_all_data()

# LOGIKA HALAMAN
if df is not None:
    if selected == "Dashboard Utama":
        render_form_input()
    elif selected == "Data & Analisis":
        render_visualisasi(df)
else:
    st.error("Gagal memuat data. Pastikan file excel tersedia.")