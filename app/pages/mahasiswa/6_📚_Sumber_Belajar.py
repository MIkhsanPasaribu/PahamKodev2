"""
Mahasiswa - Sumber Belajar

MAHASISWA FEATURE (NEW) 🟡
- Access ke recommended resources
- Filter by topik & difficulty
- Video, artikel, tutorial
"""

import streamlit as st
import logging

from app.components.sidebar import render_sidebar
from app.services.autentikasi_service import is_mahasiswa
from app.utils.helpers import format_number

logger = logging.getLogger(__name__)


# ==================== PAGE CONFIG ====================

st.set_page_config(
    page_title="Sumber Belajar - PahamKode",
    page_icon="📚",
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

st.title("📚 Sumber Belajar")
st.markdown("Akses resources pembelajaran yang direkomendasikan berdasarkan progress Anda")

pengguna = st.session_state.pengguna
queries = st.session_state.queries
id_mahasiswa = str(pengguna["_id"])

st.markdown("---")


# ==================== HELPER FUNCTION ====================

def _display_resource_card(resource: dict) -> None:
    """Display a resource card"""
    with st.container():
        col_info, col_action = st.columns([8, 2])
        
        with col_info:
            # Title with type and difficulty badges
            tipe = resource.get("tipe", "N/A")
            tingkat = resource.get("tingkat_kesulitan", "pemula")
            
            tipe_color = {
                "video": "#ef4444",
                "artikel": "#3b82f6",
                "tutorial": "#10b981",
                "exercise": "#f59e0b",
                "quiz": "#8b5cf6",
                "dokumentasi": "#6b7280"
            }.get(tipe, "#6b7280")
            
            tingkat_color = {
                "pemula": "#10b981",
                "menengah": "#f59e0b",
                "mahir": "#ef4444"
            }.get(tingkat, "#10b981")
            
            st.markdown(f"""
            **{resource.get('judul', 'N/A')}** | 
            <span style="background-color:{tipe_color};color:white;padding:2px 8px;border-radius:4px;font-size:12px;">{tipe.upper()}</span> | 
            <span style="background-color:{tingkat_color};color:white;padding:2px 8px;border-radius:4px;font-size:12px;">{tingkat.upper()}</span>
            """, unsafe_allow_html=True)
            
            # Description
            st.caption(resource.get("deskripsi", "")[:200] + ("..." if len(resource.get("deskripsi", "")) > 200 else ""))
            
            # Topics
            if resource.get("topik_terkait"):
                topics_text = ", ".join(resource["topik_terkait"][:5])
                st.caption(f"📚 Topik: {topics_text}")
            
            # Duration & Language
            details = []
            if resource.get("durasi"):
                details.append(f"⏱️ {resource['durasi']} menit")
            if resource.get("bahasa"):
                details.append(f"🌐 {resource['bahasa']}")
            
            if details:
                st.caption(" | ".join(details))
        
        with col_action:
            url = resource.get("url", "#")
            if url and url != "#":
                st.link_button("🔗 Buka", url, use_container_width=True)
            else:
                st.button("📄 Lihat", disabled=True, use_container_width=True)
        
        st.markdown("---")


# ==================== FILTERS ====================

st.markdown("### 🔍 Filter Resources")

col1, col2, col3 = st.columns(3)

with col1:
    filter_tipe = st.selectbox(
        "Tipe Resource",
        options=["Semua", "video", "artikel", "tutorial", "exercise", "quiz", "dokumentasi"],
        key="filter_tipe"
    )

with col2:
    filter_tingkat = st.selectbox(
        "Tingkat Kesulitan",
        options=["Semua", "pemula", "menengah", "mahir"],
        key="filter_tingkat"
    )

with col3:
    filter_topik = st.text_input(
        "Cari Topik",
        placeholder="Ketik nama topik...",
        key="filter_topik"
    )

st.markdown("---")


# ==================== FETCH RESOURCES ====================

try:
    # Get all resources
    all_resources = queries.daftar_semua_sumber_daya()
    
    # Apply filters
    filtered_resources = all_resources
    
    if filter_tipe != "Semua":
        filtered_resources = [r for r in filtered_resources if r.get("tipe") == filter_tipe]
    
    if filter_tingkat != "Semua":
        filtered_resources = [r for r in filtered_resources if r.get("tingkat_kesulitan") == filter_tingkat]
    
    if filter_topik:
        search_lower = filter_topik.lower()
        filtered_resources = [
            r for r in filtered_resources
            if any(search_lower in str(t).lower() for t in r.get("topik_terkait", []))
            or search_lower in r.get("judul", "").lower()
        ]
    
    total = len(filtered_resources)
    
    st.markdown(f"**Menampilkan {total} dari {len(all_resources)} resources**")
    
    
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
        Berdasarkan progress Anda, kami merekomendasikan mempelajari:
        **{', '.join(weak_topics[:3])}**
        """)
        
        # Filter resources by weak topics
        recommended_resources = [
            r for r in all_resources
            if any(topic in r.get("topik_terkait", []) for topic in weak_topics)
        ]
        
        if recommended_resources:
            for resource in recommended_resources[:5]:
                _display_resource_card(resource)
        else:
            st.info("Belum ada resources untuk topik yang direkomendasikan.")
    else:
        st.success("✅ Semua topik sudah dikuasai dengan baik! Explore resources lainnya di bawah.")
    
    st.markdown("---")
    
    
    # ==================== TABS BY TYPE ====================
    
    st.markdown("### 📂 Semua Resources")
    
    # Create tabs
    tab_all, tab_video, tab_artikel, tab_tutorial, tab_exercise = st.tabs([
        "🌐 Semua",
        "🎥 Video",
        "📝 Artikel",
        "📖 Tutorial",
        "✏️ Exercise"
    ])
    
    with tab_all:
        if not filtered_resources:
            st.info("Tidak ada resources yang cocok dengan filter.")
        else:
            for resource in filtered_resources:
                _display_resource_card(resource)
    
    with tab_video:
        video_resources = [r for r in filtered_resources if r.get("tipe") == "video"]
        if not video_resources:
            st.info("Tidak ada video resources.")
        else:
            for resource in video_resources:
                _display_resource_card(resource)
    
    with tab_artikel:
        artikel_resources = [r for r in filtered_resources if r.get("tipe") == "artikel"]
        if not artikel_resources:
            st.info("Tidak ada artikel resources.")
        else:
            for resource in artikel_resources:
                _display_resource_card(resource)
    
    with tab_tutorial:
        tutorial_resources = [r for r in filtered_resources if r.get("tipe") == "tutorial"]
        if not tutorial_resources:
            st.info("Tidak ada tutorial resources.")
        else:
            for resource in tutorial_resources:
                _display_resource_card(resource)
    
    with tab_exercise:
        exercise_resources = [r for r in filtered_resources if r.get("tipe") == "exercise"]
        if not exercise_resources:
            st.info("Tidak ada exercise resources.")
        else:
            for resource in exercise_resources:
                _display_resource_card(resource)


except Exception as e:
    logger.error(f"Error loading resources: {e}")
    st.error(f"❌ Error: {str(e)}")


# ==================== REFRESH ====================

if st.button("🔄 Refresh Data", use_container_width=True):
    st.rerun()
