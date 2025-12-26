"""
Mahasiswa - Progress Belajar

MAHASISWA FEATURE 🟡
- Learning progress per topik
- Mastery level tracking
- Improvement trends
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import pandas as pd
import logging
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from components.sidebar import render_sidebar
from services.autentikasi_service import is_mahasiswa
from utils.helpers import format_number

logger = logging.getLogger(__name__)


# ==================== PAGE CONFIG ====================

st.set_page_config(
    page_title="Progress - PahamKode",
    page_icon="📈",
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

st.title("📈 Progress Belajar")
st.markdown("Lacak perkembangan pembelajaran Anda per topik")

pengguna = st.session_state.pengguna
queries = st.session_state.queries
id_mahasiswa = str(pengguna["_id"])

st.markdown("---")


# ==================== FETCH PROGRESS DATA ====================

try:
    progress_list = queries.ambil_progress_mahasiswa(id_mahasiswa)
    
    if not progress_list:
        st.info("""
        ### Belum Ada Data Progress
        
        Data progress akan muncul setelah Anda menganalisis error dan sistem melacak pembelajaran Anda.
        
        Mulai dengan menganalisis error di halaman **Analisis**!
        """)
        
        if st.button("🔍 Mulai Analisis Error", use_container_width=True, key="progress_btn_start"):
            st.switch_page("pages/mahasiswa_2_🔍_Analisis.py")
        
        st.stop()
    
    
    # ==================== OVERALL STATISTICS ====================
    
    st.markdown("### 📊 Statistik Keseluruhan")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Topik Dipelajari", format_number(len(progress_list)))
    
    with col2:
        avg_penguasaan = sum(p.get("tingkat_penguasaan", 0) for p in progress_list) / len(progress_list)
        st.metric("Rata-rata Penguasaan", f"{avg_penguasaan:.1f}%")
    
    with col3:
        total_errors = sum(p.get("jumlah_error_di_topik", 0) for p in progress_list)
        st.metric("Total Error di Semua Topik", format_number(total_errors))
    
    with col4:
        improving = len([p for p in progress_list if p.get("tren_perbaikan") == "membaik"])
        st.metric("Topik yang Membaik", format_number(improving))
    
    st.markdown("---")
    
    
    # ==================== PROGRESS VISUALIZATION ====================
    
    st.markdown("### 📊 Visualisasi Progress")
    
    # Create DataFrame
    df_progress = pd.DataFrame([
        {
            "topik": p["topik"],
            "tingkat_penguasaan": p.get("tingkat_penguasaan", 0),
            "jumlah_error": p.get("jumlah_error_di_topik", 0),
            "tren": p.get("tren_perbaikan", "stagnan")
        }
        for p in progress_list
    ])
    
    # Sort by penguasaan
    df_progress = df_progress.sort_values("tingkat_penguasaan", ascending=True)
    
    # Bar chart - Color-coded by mastery level
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
    
    st.markdown("---")
    
    
    # ==================== FILTER & SORT ====================
    
    st.markdown("### 🔍 Filter & Sort")
    
    col1, col2 = st.columns(2)
    
    with col1:
        filter_tren = st.selectbox(
            "Filter Tren",
            options=["Semua", "membaik", "stagnan", "menurun"],
            key="filter_tren"
        )
    
    with col2:
        sort_by = st.selectbox(
            "Urutkan Berdasarkan",
            options=["penguasaan_asc", "penguasaan_desc", "error_count_asc", "error_count_desc"],
            format_func=lambda x: {
                "penguasaan_asc": "Penguasaan (Rendah ke Tinggi)",
                "penguasaan_desc": "Penguasaan (Tinggi ke Rendah)",
                "error_count_asc": "Error Count (Sedikit ke Banyak)",
                "error_count_desc": "Error Count (Banyak ke Sedikit)"
            }[x],
            key="sort_by"
        )
    
    # Apply filters
    filtered_progress = progress_list
    
    if filter_tren != "Semua":
        filtered_progress = [p for p in filtered_progress if p.get("tren_perbaikan") == filter_tren]
    
    # Apply sorting
    if sort_by == "penguasaan_asc":
        filtered_progress = sorted(filtered_progress, key=lambda x: x.get("tingkat_penguasaan", 0))
    elif sort_by == "penguasaan_desc":
        filtered_progress = sorted(filtered_progress, key=lambda x: x.get("tingkat_penguasaan", 0), reverse=True)
    elif sort_by == "error_count_asc":
        filtered_progress = sorted(filtered_progress, key=lambda x: x.get("jumlah_error_di_topik", 0))
    else:  # error_count_desc
        filtered_progress = sorted(filtered_progress, key=lambda x: x.get("jumlah_error_di_topik", 0), reverse=True)
    
    st.markdown(f"*Menampilkan {len(filtered_progress)} dari {len(progress_list)} topik*")
    
    st.markdown("---")
    
    
    # ==================== PROGRESS CARDS ====================
    
    st.markdown("### 📚 Detail Progress per Topik")
    
    for progress in filtered_progress:
        topik = progress["topik"]
        penguasaan = progress.get("tingkat_penguasaan", 0)
        error_count = progress.get("jumlah_error_di_topik", 0)
        tren = progress.get("tren_perbaikan", "stagnan")
        
        # Determine color based on mastery level
        if penguasaan >= 80:
            card_color = "#10b981"  # Green
            mastery_label = "Mahir ✅"
        elif penguasaan >= 60:
            card_color = "#3b82f6"  # Blue
            mastery_label = "Menengah 📘"
        elif penguasaan >= 40:
            card_color = "#f59e0b"  # Orange
            mastery_label = "Pemula 📙"
        else:
            card_color = "#ef4444"  # Red
            mastery_label = "Perlu Perhatian ⚠️"
        
        # Trend emoji
        tren_emoji = {
            "membaik": "⬆️",
            "stagnan": "➡️",
            "menurun": "⬇️"
        }.get(tren, "➡️")
        
        with st.container():
            # Header
            st.markdown(f"""
            <div style="background-color:{card_color};color:white;padding:12px;border-radius:8px 8px 0 0;">
                <h3 style="margin:0;">{topik}</h3>
                <p style="margin:4px 0 0 0;">{mastery_label}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                # Progress bar
                st.metric("Tingkat Penguasaan", f"{penguasaan:.1f}%")
                st.progress(penguasaan / 100)
            
            with col2:
                st.metric("Jumlah Error", format_number(error_count))
            
            with col3:
                st.metric("Tren", f"{tren_emoji} {tren.title()}")
            
            # Last error date
            if progress.get("tanggal_error_terakhir"):
                from app.utils.helpers import format_relative_time
                st.caption(f"Error terakhir: {format_relative_time(progress['tanggal_error_terakhir'])}")
            
            # Action buttons
            col_action1, col_action2 = st.columns(2)
            
            with col_action1:
                if st.button("📖 Lihat Resources", key=f"resources_{topik}", use_container_width=True):
                    st.switch_page("pages/mahasiswa_6_📚_Sumber_Belajar.py")
            
            with col_action2:
                if st.button("✏️ Latihan", key=f"exercise_{topik}", use_container_width=True):
                    st.switch_page("pages/mahasiswa_7_✏️_Latihan.py")
            
            st.markdown("---")
    
    
    # ==================== INSIGHTS ====================
    
    st.markdown("### 💡 Insights & Rekomendasi")
    
    # Find weak topics (penguasaan < 60%)
    weak_topics = [p for p in progress_list if p.get("tingkat_penguasaan", 0) < 60]
    
    if weak_topics:
        st.warning(f"""
        ⚠️ **Topik yang Perlu Diperkuat:**
        
        Anda memiliki **{len(weak_topics)} topik** dengan penguasaan < 60%:
        {', '.join([p['topik'] for p in weak_topics[:5]])}
        
        **Rekomendasi:** Fokus mempelajari topik-topik ini untuk meningkatkan kemampuan.
        """)
    else:
        st.success("🎉 Selamat! Semua topik dikuasai dengan baik (≥60%)!")
    
    # Find improving topics
    improving_topics = [p for p in progress_list if p.get("tren_perbaikan") == "membaik"]
    
    if improving_topics:
        st.success(f"""
        ✅ **Progress Positif!**
        
        **{len(improving_topics)} topik** menunjukkan tren perbaikan:
        {', '.join([p['topik'] for p in improving_topics[:5]])}
        
        Pertahankan momentum belajar Anda!
        """)


except Exception as e:
    logger.error(f"Error loading progress: {e}")
    st.error(f"❌ Error: {str(e)}")


# ==================== REFRESH ====================

st.markdown("---")

if st.button("🔄 Refresh Data", use_container_width=True, key="progress_btn_refresh"):
    st.rerun()
