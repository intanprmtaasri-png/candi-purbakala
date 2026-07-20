import streamlit as st

def render_header():
    """Menampilkan judul dan ringkasan eksekutif"""
    st.title("Peta Interaktif Zonasi Konservasi dan Aksesibilitas Wisata Edukasi Situs Purbakala")
    st.markdown("""
    **Ringkasan Eksekutif:**
    Kawasan penyangga candi di Jawa Timur saat ini menghadapi ancaman serius dari ekspansi permukiman dan aktivitas pariwisata massal. 
    Peta ini memvisualisasikan delineasi zonasi arkeologis untuk memitigasi risiko kerusakan struktur dari getaran, mengamankan zona inti, 
    serta merencanakan tata letak fasilitas wisata edukasi agar selaras dengan prinsip pelestarian cagar budaya.
    """)

def render_sidebar(candi_gdf):
    """Menampilkan sidebar untuk filter dan mengembalikan nilai filter yang dipilih pengguna"""
    st.sidebar.header("Konfigurasi Peta")
    periodisasi_list = ["Semua"] + list(candi_gdf['Periodisasi'].unique())
    pilih_period = st.sidebar.selectbox("Filter Periodisasi Candi:", periodisasi_list)
    
    return pilih_period