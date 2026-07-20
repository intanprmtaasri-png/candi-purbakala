import streamlit as st
import geopandas as gpd
import os

@st.cache_data
def load_all_data():
    """Memuat seluruh file GeoJSON dari folder 'data' dan menyimpannya di cache."""
    # Path absolut berdasarkan lokasi file ini (modules/data_loader.py)
    # Supaya path selalu benar baik dijalankan di lokal maupun di Streamlit Cloud
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(BASE_DIR, "..", "data")

    candi = gpd.read_file(os.path.join(data_dir, 'Situs_candi.geojson'))
    fasilitas = gpd.read_file(os.path.join(data_dir, 'fasilitas_informasi.geojson'))
    inti = gpd.read_file(os.path.join(data_dir, 'zona_inti.geojson'))
    penyangga = gpd.read_file(os.path.join(data_dir, 'Zona_penyangga.geojson'))
    vib_500 = gpd.read_file(os.path.join(data_dir, 'zona_vibrasi500.geojson'))
    vib_1000 = gpd.read_file(os.path.join(data_dir, 'zona_vibrasi1000.geojson'))
    
    return candi, fasilitas, inti, penyangga, vib_500, vib_1000

def filter_by_period(pilihan, candi, fasilitas, inti, penyangga, vib_500, vib_1000):
    """Menerapkan filter berdasarkan periodisasi candi beserta fasilitasnya secara spasial."""
    if pilihan == "Semua":
        return candi, fasilitas, inti, penyangga, vib_500, vib_1000
        
    # 1. Filter dataset utama candi
    candi_filtered = candi[candi['Periodisasi'] == pilihan]
    
    # 2. Filter dataset zonasi agar mengikuti candi
    inti_filtered = inti[inti['Nama_Candi'].isin(candi_filtered['Nama_Candi'])]
    penyangga_filtered = penyangga[penyangga['Nama_Candi'].isin(candi_filtered['Nama_Candi'])]
    vib_500_filtered = vib_500[vib_500['Nama_Candi'].isin(candi_filtered['Nama_Candi'])]
    vib_1000_filtered = vib_1000[vib_1000['Nama_Candi'].isin(candi_filtered['Nama_Candi'])]
    
    # 3. SPATIAL FILTER: Ambil fasilitas yang berpotongan (intersects) dengan zona getaran 1KM candi yang terfilter
    if not vib_1000_filtered.empty:
        fasilitas_filtered = gpd.sjoin(fasilitas, vib_1000_filtered[['geometry']], how='inner', predicate='intersects')
        # Hapus duplikasi jika posisinya menumpuk pada batas poligon yang bersinggungan
        fasilitas_filtered = fasilitas_filtered.drop_duplicates(subset=['Nama_Fasilitas'])
    else:
        # Jika hasil filter kosong (misal tidak ada situs), kosongkan juga fasilitasnya
        fasilitas_filtered = fasilitas.iloc[0:0] 
    
    return candi_filtered, fasilitas_filtered, inti_filtered, penyangga_filtered, vib_500_filtered, vib_1000_filtered
