"""
Mahasiswa - Latihan (Exercises)

MAHASISWA FEATURE (NEW) 🟡
- Practice exercises
- Filter by topik & difficulty
- Track completion
"""

import streamlit as st
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
    page_title="Latihan - PahamKode",
    page_icon="✏️",
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

st.title("✏️ Latihan & Exercises")
st.markdown("Practice exercises untuk memperkuat pemahaman Anda")

pengguna = st.session_state.pengguna
queries = st.session_state.queries
id_mahasiswa = str(pengguna["_id"])

st.markdown("---")


# ==================== HELPER FUNCTION ====================

def _display_exercise_card(exercise: dict, id_mahasiswa: str) -> None:
    """Display an exercise card"""
    with st.container():
        # Header
        judul = exercise.get("judul", "N/A")
        topik = exercise.get("topik", "N/A")
        tingkat = exercise.get("tingkat_kesulitan", "pemula")
        
        tingkat_color = {
            "pemula": "#10b981",
            "menengah": "#f59e0b",
            "mahir": "#ef4444"
        }.get(tingkat, "#10b981")
        
        st.markdown(f"""
        **{judul}** | 
        Topik: {topik} | 
        <span style="background-color:{tingkat_color};color:white;padding:2px 8px;border-radius:4px;font-size:12px;">{tingkat.upper()}</span>
        """, unsafe_allow_html=True)
        
        # Description
        if exercise.get("deskripsi"):
            st.caption(exercise["deskripsi"][:200] + ("..." if len(exercise.get("deskripsi", "")) > 200 else ""))
        
        # Expandable details
        with st.expander("📝 Lihat Detail Exercise"):
            # Instructions
            if exercise.get("instruksi"):
                st.markdown("#### 📋 Instruksi")
                st.info(exercise["instruksi"])
            
            # Starter code (if available)
            if exercise.get("kode_pemula"):
                st.markdown("#### 💻 Kode Pemula")
                st.code(exercise["kode_pemula"], language="python")
            
            # Test cases (if available)
            if exercise.get("test_cases"):
                st.markdown("#### ✅ Test Cases")
                for i, test in enumerate(exercise["test_cases"], 1):
                    st.markdown(f"{i}. {test}")
            
            # Estimated time
            if exercise.get("estimasi_waktu"):
                st.caption(f"⏱️ Estimasi: {exercise['estimasi_waktu']} menit")
            
            # Points/Rewards
            if exercise.get("poin_belajar"):
                st.caption(f"🎯 Poin: {exercise['poin_belajar']}")
            
            # Start exercise button
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🚀 Mulai Exercise", key=f"start_{exercise.get('_id')}", use_container_width=True):
                    st.info("""
                    **Exercise Mode belum tersedia.**
                    
                    Untuk saat ini, Anda dapat:
                    1. Copy kode pemula di atas
                    2. Kerjakan di IDE favorit Anda
                    3. Jika ada error, analisis di halaman Analisis
                    """)
            
            with col2:
                if st.button("📖 Resources", key=f"resources_{exercise.get('_id')}", use_container_width=True):
                    st.switch_page("pages/mahasiswa/6_📚_Sumber_Belajar.py")
        
        st.markdown("---")


# ==================== FILTERS ====================

st.markdown("### 🔍 Filter Exercises")

col1, col2 = st.columns(2)

with col1:
    filter_tingkat = st.selectbox(
        "Tingkat Kesulitan",
        options=["Semua", "pemula", "menengah", "mahir"],
        key="filter_tingkat"
    )

with col2:
    filter_topik = st.text_input(
        "Cari Topik",
        placeholder="Ketik nama topik...",
        key="filter_topik"
    )

st.markdown("---")


# ==================== FETCH EXERCISES ====================

try:
    # Get all exercises
    all_exercises = queries.daftar_semua_exercises()
    
    # Apply filters
    filtered_exercises = all_exercises
    
    if filter_tingkat != "Semua":
        filtered_exercises = [e for e in filtered_exercises if e.get("tingkat_kesulitan") == filter_tingkat]
    
    if filter_topik:
        search_lower = filter_topik.lower()
        filtered_exercises = [
            e for e in filtered_exercises
            if search_lower in e.get("topik", "").lower()
            or search_lower in e.get("judul", "").lower()
        ]
    
    total = len(filtered_exercises)
    
    st.markdown(f"**Menampilkan {total} dari {len(all_exercises)} exercises**")
    
    
    # ==================== RECOMMENDED SECTION ====================
    
    st.markdown("### ⭐ Direkomendasikan untuk Anda")
    
    # Get weak topics from progress
    progress_list = queries.ambil_progress_mahasiswa(id_mahasiswa)
    weak_topics = [
        p["topik"]
        for p in progress_list
        if p.get("tingkat_penguasaan", 0) < 60
    ]
    
    if weak_topics:
        st.info(f"""
        Berdasarkan progress Anda, kami merekomendasikan latihan untuk:
        **{', '.join(weak_topics[:3])}**
        """)
        
        # Filter exercises by weak topics
        recommended_exercises = [
            e for e in all_exercises
            if e.get("topik") in weak_topics
        ]
        
        if recommended_exercises:
            for exercise in recommended_exercises[:3]:
                _display_exercise_card(exercise, id_mahasiswa)
        else:
            st.info("Belum ada exercises untuk topik yang direkomendasikan.")
    else:
        st.success("✅ Semua topik sudah dikuasai dengan baik! Explore exercises lainnya di bawah.")
    
    st.markdown("---")
    
    
    # ==================== ALL EXERCISES ====================
    
    st.markdown("### 📂 Semua Exercises")
    
    if not filtered_exercises:
        st.info("Tidak ada exercises yang cocok dengan filter.")
    else:
        for exercise in filtered_exercises:
            _display_exercise_card(exercise, id_mahasiswa)


except Exception as e:
    logger.error(f"Error loading exercises: {e}")
    st.error(f"❌ Error: {str(e)}")


# ==================== INFO SECTION ====================

st.markdown("---")

st.info("""
### 💡 Cara Menggunakan Exercises

1. **Pilih exercise** sesuai tingkat kesulitan dan topik
2. **Baca instruksi** dengan teliti
3. **Kerjakan exercise** di IDE favorit Anda
4. **Jika ada error**, gunakan halaman **Analisis** untuk mendapat penjelasan konseptual
5. **Track progress** Anda di halaman **Progress**

**Tips:**
- Mulai dari level **pemula** jika baru belajar topik
- Kerjakan exercise secara **konsisten** untuk hasil maksimal
- Jangan ragu untuk **coba-coba** dan **belajar dari error**
""")


# ==================== REFRESH ====================

if st.button("🔄 Refresh Data", use_container_width=True):
    st.rerun()
