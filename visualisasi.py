import streamlit as st
import plotly.express as px
import pandas as pd

def render_visualisasi(df):
    st.write("##")
    st.markdown("<h2 style='text-align: center; color: white; text-shadow: 5px 5px 5px rgba(10.0,10.0,10.0,10.0);'>Statistik Laporan Dinas Pendidikan Jawa Timur</h2>", unsafe_allow_html=True)
    st.write("##")
    
    if df.empty:
        st.info("Belum ada data untuk ditampilkan.")
        return
    
    # FILTER DATA
    st.markdown("<h3 style='text-align: left; color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.8);'>🔍 Filter Data</h3>", unsafe_allow_html=True)
    c_filter, _ = st.columns([1, 3]) 
    with c_filter:
        list_tahun = sorted(df['Tahun'].unique())
        sel_tahun = st.selectbox(
            "Pilih Tahun", 
            list_tahun, 
            label_visibility="collapsed" 
        )

    df_filtered = df[df['Tahun'] == sel_tahun]
    st.divider()

    # METRIK UTAMA 
    st.markdown("<h3 style='text-align: left; color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.8);'>📊 Ringkasan Laporan</h3>", unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    
    total = len(df_filtered)
    pengaduan = len(df_filtered[df_filtered['Tipe'] == 'Pengaduan'])
    aspirasi = len(df_filtered[df_filtered['Tipe'] == 'Aspirasi'])
    info = len(df_filtered[df_filtered['Tipe'] == 'Permohonan Informasi'])

    m1.metric("Total Laporan", total)
    m2.metric("Pengaduan", pengaduan)
    m3.metric("Aspirasi", aspirasi)
    m4.metric("Informasi", info)

    tercepat_detik = pd.to_numeric(df_filtered['WAKTU RESPON'], errors='coerce').min()
    if pd.isna(tercepat_detik): 
        tercepat_detik = 0

    c_met1, c_met2 = st.columns(2)
    c_met1.info(f"✨ **Tingkat Kepuasan:** 87.9%")
    c_met2.info(f"⏳ **Durasi Respon Tercepat:** {int(tercepat_detik)} Detik")
    st.divider()

    # GRAFIK TREN KATEGORI 
    st.markdown("<h3 style='text-align: left; color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.8);'>📈 Tren Kategori Laporan</h3>", unsafe_allow_html=True)
    
    df_grouped = df_filtered.groupby(['Bulan', 'Tipe']).size().reset_index(name='Jumlah')
    bulan_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                   'July', 'August', 'September', 'October', 'November', 'December']

    fig_bar = px.bar(df_grouped, 
                     x='Bulan', 
                     y='Jumlah', 
                     color='Tipe', 
                     barmode='group', 
                     category_orders={"Bulan": bulan_order},
                     color_discrete_sequence=px.colors.qualitative.Pastel)
    
    # PERUBAHAN: Setel teks kontras tinggi & Efek kaca gelap tipis untuk grafik utama
    fig_bar.update_layout(
        paper_bgcolor='rgba(0,0,0,0.4)', # Lapisan hitam transparan di luar area chart
        plot_bgcolor='rgba(0,0,0,0.2)',  # Lapisan hitam transparan di dalam grid chart
        font=dict(family="Arial, sans-serif", size=13, color="white"), 
        xaxis=dict(
            title=dict(text="Bulan Laporan", font=dict(size=14, color="white")),
            tickfont=dict(color="white", size=12),
            gridcolor='rgba(255,255,255,0.1)' # Garis grid tipis transparan
        ),
        yaxis=dict(
            title=dict(text="Jumlah Laporan", font=dict(size=14, color="white")),
            tickfont=dict(color="white", size=12),
            gridcolor='rgba(255,255,255,0.1)'
        ),
        legend=dict(
            font=dict(color="white", size=11),
            bgcolor='rgba(0,0,0,0.6)', 
            bordercolor='rgba(255,255,255,0.3)',
            borderwidth=1
        )
    )
    # Memunculkan angka jumlah tebal berwarna putih di atas setiap batang diagram
    fig_bar.update_traces(
        texttemplate='%{y}',
        textposition='outside',
        textfont=dict(color='white', size=11, family='Arial-Bold')
    )
    st.plotly_chart(fig_bar, use_container_width=True)
    st.divider()

    # LAYOUT SEJAJAR (Gender & Sebaran Asal Daerah) 
    st.markdown("<h3 style='text-align: left; color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.8);'>👥 Demografi & Wilayah</h3>", unsafe_allow_html=True)
    col_kiri, col_kanan = st.columns(2) 

    with col_kiri:
        st.markdown("<p style='color: white; font-weight: bold;'>Proporsi Gender</p>", unsafe_allow_html=True)
        fig_pie_gender = px.pie(df_filtered, names='JENIS KELAMIN', hole=0.5,
                                color_discrete_sequence=px.colors.qualitative.Pastel)
        
        # Setel teks & background transparan gelap untuk Donut Chart
        fig_pie_gender.update_layout(
            paper_bgcolor='rgba(0,0,0,0.4)', 
            font=dict(family="Arial, sans-serif", size=13, color="white"),
            legend=dict(
                font=dict(color="white"),
                bgcolor='rgba(0,0,0,0.6)',
                bordercolor='rgba(255,255,255,0.2)',
                borderwidth=1
            )
        )
        # Menampilkan persentase di dalam potongan kue dengan warna teks putih tajam
        fig_pie_gender.update_traces(
            textinfo='percent+label',
            textfont=dict(color='white', size=12, family='Arial-Bold')
        )
        st.plotly_chart(fig_pie_gender, use_container_width=True)

    with col_kanan:
        st.markdown("<p style='color: white; font-weight: bold;'>Sebaran Asal Daerah</p>", unsafe_allow_html=True)
        
        df_wilayah = df_filtered['Wilayah'].value_counts().reset_index()
        df_wilayah.columns = ['Wilayah', 'Jumlah']
        
        fig_bar_wilayah = px.bar(
            df_wilayah, 
            x='Wilayah', 
            y='Jumlah',
            labels={'Jumlah': 'Total', 'Wilayah': 'Daerah'},
            color_discrete_sequence=['rgba(93, 158, 243, 0.86)'] # PERBAIKAN DI SINI
        )
        
        # Setel teks & background transparan gelap untuk Bar Chart Wilayah
        fig_bar_wilayah.update_layout(
            paper_bgcolor='rgba(0,0,0,0.4)', 
            plot_bgcolor='rgba(0,0,0,0.2)', 
            font=dict(family="Arial, sans-serif", size=13, color="white"),
            xaxis=dict(
                title=dict(font=dict(size=14, color="white")),
                tickfont=dict(color="white", size=11),
                gridcolor='rgba(255,255,255,0.1)'
            ),
            yaxis=dict(
                title=dict(font=dict(size=14, color="white")),
                tickfont=dict(color="white", size=11),
                gridcolor='rgba(255,255,255,0.1)'
            )
        )
        # Memunculkan nilai angka di atas diagram wilayah
        fig_bar_wilayah.update_traces(
            texttemplate='%{y}',
            textposition='outside',
            textfont=dict(color='white', size=11, family='Arial-Bold')
        )
        st.plotly_chart(fig_bar_wilayah, use_container_width=True)

    st.divider()

    # BAGIAN DOWNLOAD 
    col_kosong, col_kosong, col_download = st.columns([1.5, 7, 1.5])
    with col_download:
        st.markdown('<div class="download-container">', unsafe_allow_html=True)
        if st.button("📥 Download Data", key="btn-download", use_container_width=True):
            st.toast("Data hanya bisa diakses oleh admin. Silakan hubungi administrator untuk mendapatkan akses penuh.")
        st.markdown('</div>', unsafe_allow_html=True)