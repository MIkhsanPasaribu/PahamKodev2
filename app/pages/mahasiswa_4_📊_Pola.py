"""
Mahasiswa - Pola Error Personal

MAHASISWA FEATURE 🟡
- Personal error patterns
- Pattern analysis & recommendations
- Learning insights
"""

import streamlit as st
import plotly.express as px
from datetime import datetime
import pandas as pd
import logging
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from components.sidebar import render_sidebar
from services.autentikasi_service import is_mahasiswa
from utils.helpers import format_number, format_datetime, get_severity_color

logger = logging.getLogger(__name__)


# ==================== PAGE CONFIG ====================

st.set_page_config(
    page_title="Pola Error - PahamKode",
    page_icon="📊",
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

st.title("📊 Pola Error Personal")
st.markdown("Analisis pola kesalahan Anda untuk pembelajaran lebih efektif")

pengguna = st.session_state.pengguna
queries = st.session_state.queries
id_mahasiswa = str(pengguna["_id"])

st.markdown("---")


# ==================== FETCH PATTERNS ====================

try:
    pola_list = queries.ambil_pola_mahasiswa(id_mahasiswa)
    
    if not pola_list:
        st.info("""
        ### Belum Ada Pola Terdeteksi
        
        Pola error akan terdeteksi setelah Anda:
        - Menganalisis error minimal 3 kali
        - Mengalami error type yang sama ≥3 kali
        
        Mulai dengan menganalisis error di halaman **Analisis**!
        """)
        
        if st.button("🔍 Mulai Analisis Error", use_container_width=True):
            st.switch_page("pages/mahasiswa/2_🔍_Analisis.py")
        
        st.stop()
    
    
    # ==================== SUMMARY METRICS ====================
    
    st.markdown("### 📈 Ringkasan Pola")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Pola Terdeteksi", format_number(len(pola_list)))
    
    with col2:
        total_freq = sum(p.get("frekuensi", 0) for p in pola_list)
        st.metric("Total Occurrence", format_number(total_freq))
    
    with col3:
        avg_freq = total_freq / len(pola_list) if pola_list else 0
        st.metric("Rata-rata Frekuensi", f"{avg_freq:.1f}")
    
    st.markdown("---")
    
    
    # ==================== PATTERN VISUALIZATION ====================
    
    st.markdown("### 📊 Visualisasi Pola")
    
    # Sort by frequency
    sorted_pola = sorted(pola_list, key=lambda x: x.get("frekuensi", 0), reverse=True)
    
    # Create DataFrame for visualization
    df_pola = pd.DataFrame([
        {
            "jenis_kesalahan": p["jenis_kesalahan"],
            "frekuensi": p.get("frekuensi", 0)
        }
        for p in sorted_pola[:10]
    ])
    
    # Bar chart
    fig_pola = px.bar(
        df_pola,
        x="frekuensi",
        y="jenis_kesalahan",
        orientation="h",
        title="Top 10 Pola Error Anda",
        labels={"frekuensi": "Frekuensi", "jenis_kesalahan": "Jenis Kesalahan"},
        color="frekuensi",
        color_continuous_scale="Reds"
    )
    
    fig_pola.update_layout(yaxis={'categoryorder': 'total ascending'})
    
    st.plotly_chart(fig_pola, use_container_width=True)
    
    st.markdown("---")
    
    
    # ==================== PATTERN CARDS ====================
    
    st.markdown("### 🔍 Detail Pola")
    
    for i, pola in enumerate(sorted_pola, 1):
        # Determine severity based on frequency
        freq = pola.get("frekuensi", 0)
        severity = "tinggi" if freq >= 5 else "sedang" if freq >= 3 else "rendah"
        severity_color = get_severity_color(severity)
        
        with st.container():
            # Header with severity badge
            st.markdown(f"""
            <div style="background-color:{severity_color};color:white;padding:12px;border-radius:8px 8px 0 0;">
                <h3 style="margin:0;">#{i}. {pola['jenis_kesalahan']}</h3>
                <p style="margin:4px 0 0 0;">Frekuensi: {freq} kali | Severity: {severity.upper()}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Timeline
            col1, col2 = st.columns(2)
            
            with col1:
                if pola.get("kejadian_pertama"):
                    st.caption(f"**Pertama kali:** {format_datetime(pola['kejadian_pertama'], 'date')}")
            
            with col2:
                if pola.get("kejadian_terakhir"):
                    st.caption(f"**Terakhir kali:** {format_datetime(pola['kejadian_terakhir'], 'date')}")
            
            # Misconception description
            if pola.get("deskripsi_miskonsepsi"):
                st.markdown("#### 🧠 Deskripsi Miskonsepsi")
                st.info(pola["deskripsi_miskonsepsi"])
            
            # Recommended resources
            if pola.get("sumber_daya_direkomendasikan"):
                st.markdown("#### 📚 Sumber Daya yang Direkomendasikan")
                
                for resource in pola["sumber_daya_direkomendasikan"][:5]:
                    st.markdown(f"- {resource}")
                
                # Link to learning resources page
                if st.button(
                    "📖 Lihat Semua Resources",
                    key=f"resources_{i}",
                    use_container_width=True
                ):
                    st.switch_page("pages/mahasiswa/6_📚_Sumber_Belajar.py")
            
            st.markdown("---")
    
    
    # ==================== ACTIONABLE INSIGHTS ====================
    
    st.markdown("### 💡 Insights & Rekomendasi")
    
    # Generate insights based on patterns
    high_freq_patterns = [p for p in sorted_pola if p.get("frekuensi", 0) >= 5]
    
    if high_freq_patterns:
        st.warning(f"""
        ⚠️ **Perhatian!**
        
        Anda memiliki **{len(high_freq_patterns)} pola** dengan frekuensi tinggi (≥5 kali):
        {', '.join([p['jenis_kesalahan'] for p in high_freq_patterns[:3]])}
        
        **Rekomendasi:** Fokus mempelajari konsep-konsep terkait pola ini untuk mengurangi error serupa di masa depan.
        """)
    
    # Improvement suggestions
    st.success("""
    💪 **Tips Mengurangi Error Patterns:**
    
    1. **Review konsep dasar** topik yang sering error
    2. **Latihan coding** dengan fokus pada pola yang lemah
    3. **Baca dokumentasi** terkait error type yang sering muncul
    4. **Praktik debugging** secara sistematis
    5. **Konsultasi mentor** jika pola terus berulang
    """)


except Exception as e:
    logger.error(f"Error loading patterns: {e}")
    st.error(f"❌ Error: {str(e)}")


# ==================== REFRESH ====================

st.markdown("---")

if st.button("🔄 Refresh Data", use_container_width=True):
    st.rerun()
