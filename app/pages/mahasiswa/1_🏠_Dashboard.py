"""
Mahasiswa - Dashboard

MAHASISWA FEATURE (NEW) 🟡
- Overview stats mahasiswa
- Recent activity feed
- Quick actions
- Progress summary
"""

import streamlit as st
import plotly.express as px
from datetime import datetime
import logging

from app.components.sidebar import render_sidebar
from app.services.analisis_service import hitung_statistik_mahasiswa
from app.services.autentikasi_service import is_mahasiswa
from app.utils.helpers import format_number, format_percentage, format_relative_time

logger = logging.getLogger(__name__)


# ==================== PAGE CONFIG ====================

st.set_page_config(
    page_title="Dashboard - PahamKode",
    page_icon="🏠",
    layout="wide"
)


# ==================== AUTHENTICATION CHECK ====================

if "pengguna" not in st.session_state or st.session_state.pengguna is None:
    st.error("❌ Anda harus login terlebih dahulu!")
    st.stop()

if not is_mahasiswa(st.session_state.pengguna):
    st.error("❌ Halaman ini hanya untuk Mahasiswa.")
    st.stop()


# ==================== SIDEBAR ====================

render_sidebar()


# ==================== MAIN PAGE ====================

st.title("🏠 Dashboard Mahasiswa")

pengguna = st.session_state.pengguna
queries = st.session_state.queries
id_mahasiswa = str(pengguna["_id"])

# Welcome message
st.markdown(f"### Selamat datang, **{pengguna.get('nama', 'Mahasiswa')}**! 👋")
st.caption(f"Tingkat Kemahiran: **{pengguna.get('tingkat_kemahiran', 'pemula').title()}**")

st.markdown("---")


# ==================== FETCH STATISTICS ====================

try:
    with st.spinner("Memuat statistik..."):
        stats = hitung_statistik_mahasiswa(queries, id_mahasiswa)
    
    
    # ==================== KEY METRICS ====================
    
    st.markdown("### 📊 Ringkasan Statistik")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Submisi",
            format_number(stats.get("total_submisi", 0)),
            delta=f"+{stats.get('submisi_minggu_ini', 0)} minggu ini"
        )
    
    with col2:
        rata_penguasaan = stats.get("rata_rata_penguasaan", 0)
        st.metric(
            "Rata-rata Penguasaan",
            f"{rata_penguasaan:.1f}%",
            delta=f"{stats.get('penguasaan_delta', 0):+.1f}%"
        )
    
    with col3:
        st.metric(
            "Pola Error Terdeteksi",
            format_number(stats.get("total_pola", 0))
        )
    
    with col4:
        st.metric(
            "Topik Dipelajari",
            format_number(stats.get("topik_dipelajari", 0))
        )
    
    st.markdown("---")
    
    
    # ==================== PROGRESS CHART ====================
    
    st.markdown("### 📈 Progress Belajar per Topik")
    
    progress_data = stats.get("progress_per_topik", [])
    
    if progress_data:
        import pandas as pd
        df_progress = pd.DataFrame(progress_data)
        
        # Bar chart - horizontal
        fig_progress = px.bar(
            df_progress,
            x="tingkat_penguasaan",
            y="topik",
            orientation="h",
            title="Tingkat Penguasaan per Topik",
            labels={"tingkat_penguasaan": "Penguasaan (%)", "topik": "Topik"},
            color="tingkat_penguasaan",
            color_continuous_scale="RdYlGn",
            range_color=[0, 100]
        )
        
        fig_progress.update_layout(yaxis={'categoryorder': 'total ascending'})
        
        st.plotly_chart(fig_progress, use_container_width=True)
    else:
        st.info("Belum ada data progress. Mulai dengan menganalisis error pertama Anda!")
    
    st.markdown("---")
    
    
    # ==================== RECENT ACTIVITY ====================
    
    st.markdown("### 📜 Aktivitas Terbaru")
    
    recent_activity = stats.get("recent_activity", [])
    
    if recent_activity:
        for activity in recent_activity[:10]:
            with st.container():
                col_time, col_content = st.columns([2, 8])
                
                with col_time:
                    st.caption(format_relative_time(activity.get("created_at", datetime.now())))
                
                with col_content:
                    st.markdown(f"""
                    **{activity.get('tipe_error', 'Error')}** - {activity.get('bahasa', 'Python')}
                    """)
                    
                    if activity.get("kesenjangan_konsep"):
                        st.caption(f"💡 {activity['kesenjangan_konsep'][:100]}...")
                
                st.markdown("---")
    else:
        st.info("Belum ada aktivitas. Mulai analisis error pertama Anda di halaman Analisis!")
    
    
    # ==================== TOP ERROR PATTERNS ====================
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔴 Top 3 Pola Error Anda")
        
        top_pola = stats.get("top_pola", [])
        
        if top_pola:
            for i, pola in enumerate(top_pola[:3], 1):
                st.markdown(f"""
                **{i}. {pola['jenis_kesalahan']}**
                
                Frekuensi: {pola['frekuensi']} kali
                """)
                
                if i < 3:
                    st.markdown("---")
        else:
            st.info("Belum ada pola terdeteksi.")
    
    with col2:
        st.markdown("### 📚 Topik yang Perlu Diperkuat")
        
        weak_topics = stats.get("weak_topics", [])
        
        if weak_topics:
            for i, topic in enumerate(weak_topics[:3], 1):
                st.markdown(f"""
                **{i}. {topic['topik']}**
                
                Penguasaan: {topic['tingkat_penguasaan']:.1f}% | 
                Errors: {topic['jumlah_error']}
                """)
                
                if i < 3:
                    st.markdown("---")
        else:
            st.success("✅ Semua topik sudah dikuasai dengan baik!")
    
    st.markdown("---")
    
    
    # ==================== QUICK ACTIONS ====================
    
    st.markdown("### ⚡ Quick Actions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🔍 Analisis Error", use_container_width=True):
            st.switch_page("pages/mahasiswa/2_🔍_Analisis.py")
    
    with col2:
        if st.button("📜 Lihat Riwayat", use_container_width=True):
            st.switch_page("pages/mahasiswa/3_📜_Riwayat.py")
    
    with col3:
        if st.button("📊 Lihat Pola", use_container_width=True):
            st.switch_page("pages/mahasiswa/4_📊_Pola.py")
    
    with col4:
        if st.button("📈 Lihat Progress", use_container_width=True):
            st.switch_page("pages/mahasiswa/5_📈_Progress.py")
    
    st.markdown("---")
    
    
    # ==================== TIPS & RECOMMENDATIONS ====================
    
    st.markdown("### 💡 Tips & Rekomendasi")
    
    recommendations = stats.get("recommendations", [])
    
    if recommendations:
        for rec in recommendations[:3]:
            st.info(rec)
    else:
        st.info("""
        **Mulai dengan Analisis Error!**
        
        Gunakan halaman Analisis untuk menganalisis error pemrograman Anda. Sistem akan memberikan
        penjelasan konseptual dan rekomendasi pembelajaran yang dipersonalisasi.
        """)


except Exception as e:
    logger.error(f"Error loading dashboard: {e}")
    st.error(f"❌ Error: {str(e)}")


# ==================== REFRESH ====================

st.markdown("---")

if st.button("🔄 Refresh Data", use_container_width=True):
    st.rerun()
