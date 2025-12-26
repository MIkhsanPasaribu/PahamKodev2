"""
Mahasiswa - Riwayat Submisi

MAHASISWA FEATURE 🟡
- History submisi error
- Filter & search
- View full analysis details
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import logging
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from components.sidebar import render_sidebar
from services.autentikasi_service import is_mahasiswa
from utils.helpers import format_datetime, format_relative_time, get_severity_color

logger = logging.getLogger(__name__)


# ==================== PAGE CONFIG ====================

st.set_page_config(
    page_title="Riwayat - PahamKode",
    page_icon="📜",
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

st.title("📜 Riwayat Submisi")
st.markdown("Lihat riwayat analisis error Anda")

pengguna = st.session_state.pengguna
queries = st.session_state.queries
id_mahasiswa = str(pengguna["_id"])

st.markdown("---")


# ==================== FILTERS ====================

st.markdown("### 🔍 Filter & Pencarian")

col1, col2, col3, col4 = st.columns(4)

with col1:
    filter_bahasa = st.selectbox(
        "Bahasa",
        options=["Semua", "python", "javascript", "java", "cpp", "csharp"],
        format_func=lambda x: x.title() if x != "Semua" else x,
        key="filter_bahasa"
    )

with col2:
    filter_level = st.selectbox(
        "Bloom Level",
        options=["Semua", "Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"],
        key="filter_level"
    )

with col3:
    date_range = st.selectbox(
        "Periode",
        options=["7_hari", "30_hari", "90_hari", "semua"],
        format_func=lambda x: {
            "7_hari": "7 Hari Terakhir",
            "30_hari": "30 Hari Terakhir",
            "90_hari": "90 Hari Terakhir",
            "semua": "Semua"
        }[x],
        key="date_range"
    )

with col4:
    per_page = st.selectbox(
        "Per Halaman",
        options=[10, 25, 50],
        index=0,
        key="per_page"
    )

# Search box
search_query = st.text_input(
    "Cari error type atau kesenjangan konsep",
    placeholder="Ketik untuk mencari...",
    key="search_query"
)

st.markdown("---")


# ==================== PAGINATION ====================

if "history_page" not in st.session_state:
    st.session_state.history_page = 0


# ==================== FETCH HISTORY ====================

try:
    # Ensure types are safe
    periode: str = date_range if isinstance(date_range, str) else "semua"
    items_per_page: int = per_page if isinstance(per_page, int) else 10
    
    # Calculate date filter
    start_date = None
    if periode != "semua":
        days = {"7_hari": 7, "30_hari": 30, "90_hari": 90}.get(periode, 30)
        start_date = datetime.now() - timedelta(days=days)
    
    # Fetch from database
    skip = st.session_state.history_page * items_per_page
    riwayat = queries.ambil_riwayat_submisi(id_mahasiswa, limit=items_per_page, skip=skip)
    
    # Apply filters
    filtered_riwayat = riwayat
    
    if filter_bahasa != "Semua":
        filtered_riwayat = [r for r in filtered_riwayat if r.get("bahasa") == filter_bahasa]
    
    if filter_level != "Semua":
        filtered_riwayat = [r for r in filtered_riwayat if r.get("level_bloom") == filter_level]
    
    if start_date:
        filtered_riwayat = [r for r in filtered_riwayat if r.get("created_at") >= start_date]
    
    if search_query:
        search_lower = search_query.lower()
        filtered_riwayat = [
            r for r in filtered_riwayat
            if search_lower in r.get("tipe_error", "").lower()
            or search_lower in r.get("kesenjangan_konsep", "").lower()
        ]
    
    # Count total
    total_count = len(filtered_riwayat)
    
    st.markdown(f"**Menampilkan {total_count} submisi**")
    
    
    # ==================== DISPLAY HISTORY ====================
    
    if not filtered_riwayat:
        st.info("Tidak ada riwayat yang cocok dengan filter.")
    else:
        for submisi in filtered_riwayat:
            with st.expander(
                f"🔹 {submisi.get('tipe_error', 'Unknown Error')} - {submisi.get('bahasa', 'N/A').title()} "
                f"({format_relative_time(submisi.get('created_at', datetime.now()))})"
            ):
                # Metadata
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"**Tanggal:** {format_datetime(submisi.get('created_at', datetime.now()), 'full')}")
                
                with col2:
                    level = submisi.get("level_bloom", "N/A")
                    st.markdown(f"**Bloom Level:** {level}")
                
                with col3:
                    bahasa = submisi.get("bahasa", "N/A")
                    st.markdown(f"**Bahasa:** {bahasa.title()}")
                
                st.markdown("---")
                
                # Error details
                st.markdown("#### 🎯 Penyebab Utama")
                st.info(submisi.get("penyebab_utama", "N/A"))
                
                st.markdown("#### 🧠 Kesenjangan Konsep")
                st.warning(submisi.get("kesenjangan_konsep", "N/A"))
                
                # Code snippet
                if submisi.get("kode"):
                    st.markdown("#### 💻 Kode")
                    st.code(submisi["kode"][:500] + ("..." if len(submisi["kode"]) > 500 else ""), language=bahasa)
                
                # Error message
                if submisi.get("pesan_error"):
                    st.markdown("#### ❌ Error Message")
                    st.code(submisi["pesan_error"][:300] + ("..." if len(submisi["pesan_error"]) > 300 else ""))
                
                # Full explanation (NO nested expander - display directly)
                st.markdown("#### 📖 Penjelasan Lengkap")
                penjelasan = submisi.get("penjelasan", "N/A")
                if len(penjelasan) > 500:
                    st.markdown(penjelasan[:500] + "...")
                    st.caption("ℹ️ Penjelasan dipotong untuk tampilan. Lihat detail lengkap di halaman Analisis.")
                else:
                    st.markdown(penjelasan)
                
                # Fix suggestion (NO nested expander - display directly)
                if submisi.get("saran_perbaikan"):
                    st.markdown("#### 💡 Saran Perbaikan")
                    saran = submisi["saran_perbaikan"]
                    if len(saran) > 400:
                        st.code(saran[:400] + "...", language=bahasa)
                        st.caption("ℹ️ Saran dipotong untuk tampilan.")
                    else:
                        st.code(saran, language=bahasa)
                
                # Related topics
                if submisi.get("topik_terkait"):
                    st.markdown("**Topik Terkait:**")
                    st.markdown(", ".join(submisi["topik_terkait"][:5]))


except Exception as e:
    logger.error(f"Error loading history: {e}")
    st.error(f"❌ Error: {str(e)}")


# ==================== PAGINATION CONTROLS ====================

st.markdown("---")

col1, col2, col3 = st.columns([1, 8, 1])

with col1:
    if st.button("◀️ Sebelumnya", disabled=(st.session_state.history_page == 0), key="riwayat_btn_prev"):
        st.session_state.history_page -= 1
        st.rerun()

with col2:
    st.markdown(f"<div style='text-align:center;padding:8px;'>Halaman {st.session_state.history_page + 1}</div>", unsafe_allow_html=True)

with col3:
    if st.button("Selanjutnya ▶️", key="riwayat_btn_next"):
        st.session_state.history_page += 1
        st.rerun()
