import folium

def style_vib1000(feature):
    return {'fillColor': '#D3D3D3', 'color': 'black', 'weight': 1, 'fillOpacity': 0.3, 'dashArray': '4'}

def style_vib500(feature):
    return {'fillColor': '#808080', 'color': 'black', 'weight': 1, 'fillOpacity': 0.4, 'dashArray': '4'}

def style_penyangga(feature):
    return {'fillColor': 'orange', 'color': 'orange', 'weight': 1.5, 'fillOpacity': 0.5}

def style_inti(feature):
    return {'fillColor': 'red', 'color': 'darkred', 'weight': 2, 'fillOpacity': 0.6}

def build_map(candi_gdf, fas_gdf, inti_gdf, penyangga_gdf, vib_500_gdf, vib_1000_gdf):
    """Merakit peta Folium dengan seluruh layernya."""
    # Inisialisasi Peta
    # Inisialisasi Peta (Matikan tiles bawaan dengan tiles=None)
    m = folium.Map(location=[-7.8, 112.5], zoom_start=9, tiles=None)

    # Tambahkan basemap secara eksplisit agar namanya bisa kita atur
    folium.TileLayer(
        tiles='CartoDB positron',
        name='Tampilan Medan', 
        control=True
    ).add_to(m)

    folium.TileLayer(
        tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
        attr='Google',
        name='Citra Satelit Google',
        control=True
    ).add_to(m)

    # ==========================================
    # REVISI 1: PENGATURAN VISIBILITAS LAYER AWAL
    # ==========================================
    # Layer yang diset show=False akan mati (un-checked) saat web pertama dibuka.
    fg_vib1000 = folium.FeatureGroup(name="Buffer Getaran 1KM (Abu Terang)", show=False)
    fg_vib500 = folium.FeatureGroup(name="Buffer Getaran 500m (Abu Gelap)", show=False)
    fg_penyangga = folium.FeatureGroup(name="Zonasi Penyangga 200m (Oranye)", show=False) 
    fg_fasilitas = folium.FeatureGroup(name="Fasilitas & Pos Pantau", show=False)
    
    # Hanya Zona Inti dan Fasilitas yang menyala di awal
    fg_inti = folium.FeatureGroup(name="Zonasi Inti 50m (Merah)", show=True)

    # Render Poligon Zonasi
    folium.GeoJson(vib_1000_gdf, style_function=style_vib1000).add_to(fg_vib1000)
    folium.GeoJson(vib_500_gdf, style_function=style_vib500).add_to(fg_vib500)
    folium.GeoJson(penyangga_gdf, style_function=style_penyangga).add_to(fg_penyangga)
    folium.GeoJson(inti_gdf, style_function=style_inti).add_to(fg_inti)

    # Render Titik Candi & Pop-up
    for _, row in candi_gdf.iterrows():
        html_candi = f"""
        <b>{row['Nama_Candi']}</b><br>
        Abad: {row['Abad']}<br>
        Dinasti: {row['Dinasti']}<br>
        Status: {row['Status']}<br>
        Risiko: {row['Risiko']}
        """
        folium.CircleMarker(
            location=[row.geometry.y, row.geometry.x],
            radius=6, color='black', weight=1, fill=True, fill_color='red', fill_opacity=1,
            popup=folium.Popup(html_candi, max_width=250)
        ).add_to(fg_inti)

    # Render Titik Fasilitas & Pop-up
    for _, row in fas_gdf.iterrows():
        warna_ikon = 'green' if row['Kategori'] == 'Pusat Informasi' else 'blue'
        ikon = 'info-sign' if row['Kategori'] == 'Pusat Informasi' else 'eye-open'
        
        html_fas = f"""
        <b>{row['Nama_Fasilitas']}</b><br>
        Kapasitas: {row['Kapasitas']}<br>
        Layanan: {row['Layanan']}
        """
        folium.Marker(
            location=[row.geometry.y, row.geometry.x],
            icon=folium.Icon(color=warna_ikon, icon=ikon),
            popup=folium.Popup(html_fas, max_width=250)
        ).add_to(fg_fasilitas)

    # Gabungkan layer ke peta
    fg_vib1000.add_to(m)
    fg_vib500.add_to(m)
    fg_penyangga.add_to(m)
    fg_inti.add_to(m)
    fg_fasilitas.add_to(m)

    # Tambahkan Layer Control di pojok kanan atas
    folium.LayerControl(collapsed=False).add_to(m)
    
    return m