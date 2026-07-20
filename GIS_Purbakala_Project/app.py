import streamlit as st
from streamlit_folium import folium_static

from modules.data_loader import load_all_data, filter_by_period
from modules.map_builder import build_map
from modules.ui_components import render_header, render_sidebar

st.set_page_config(page_title="WebGIS Cagar Budaya", layout="wide")

render_header()

candi_gdf, fas_gdf, inti_gdf, penyangga_gdf, vib_500_gdf, vib_1000_gdf = load_all_data()

pilih_period = render_sidebar(candi_gdf)

# REVISI: fas_gdf sekarang ikut dimasukkan ke dalam fungsi filter
candi_f, fas_f, inti_f, peny_f, vib500_f, vib1000_f = filter_by_period(
    pilih_period, candi_gdf, fas_gdf, inti_gdf, penyangga_gdf, vib_500_gdf, vib_1000_gdf
)

# REVISI: Peta dirender menggunakan fas_f (Fasilitas yang sudah difilter secara spasial)
peta_folium = build_map(candi_f, fas_f, inti_f, peny_f, vib500_f, vib1000_f)

st.markdown("---")
folium_static(peta_folium, width=1100, height=650)