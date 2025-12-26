"""
Admin - Kelola Konten (Content Management)

CRITICAL ADMIN FEATURE 🔴
- Manage sumber daya pembelajaran (resources)
- Tambah/edit topik pembelajaran
- Atur difficulty level per topik
- Upload materi referensi
- Manage exercises
"""

import streamlit as st
from datetime import datetime
import logging
from typing import Optional
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from components.sidebar import render_sidebar
from services.admin_service import (
    ambil_semua_sumber_daya,
    tambah_sumber_daya,
    update_sumber_daya,
    hapus_sumber_daya,
    ambil_semua_topik,
    tambah_topik,
    update_topik,
    hapus_topik,
    ambil_semua_exercises,
    tambah_exercise,
    update_exercise,
    hapus_exercise
)
from services.autentikasi_service import require_admin
from utils.helpers import format_datetime, format_number

logger = logging.getLogger(__name__)


# ==================== PAGE CONFIG ====================

st.set_page_config(
    page_title="Kelola Konten - PahamKode",
    page_icon="📚",
    layout="wide"
)


# ==================== AUTHENTICATION CHECK ====================

if "pengguna" not in st.session_state or st.session_state.pengguna is None:
    st.error("❌ Anda harus login terlebih dahulu!")
    st.stop()

if not require_admin(st.session_state.pengguna):
    st.error("❌ Akses ditolak! Halaman ini hanya untuk Admin.")
    st.stop()


# ==================== SIDEBAR ====================

render_sidebar()


# ==================== MAIN PAGE ====================

st.title("📚 Kelola Konten")
st.markdown("Manajemen sumber daya pembelajaran, topik, dan exercises")

queries = st.session_state.queries


# ==================== TABS ====================

tab_resources, tab_topics, tab_exercises = st.tabs([
    "📖 Sumber Daya",
    "📚 Topik Pembelajaran",
    "✏️ Exercises"
])


# ==================== TAB 1: SUMBER DAYA ====================

with tab_resources:
    st.markdown("### 📖 Manage Sumber Daya")
    
    # Add New Resource Button
    if st.button("➕ Tambah Sumber Daya Baru", key="add_resource_btn"):
        st.session_state.show_resource_form = True
        st.session_state.edit_resource_id = None
    
    # Add/Edit Form
    if st.session_state.get("show_resource_form", False):
        with st.form("form_resource"):
            st.markdown("#### ➕ Form Sumber Daya")
            
            # Check if editing
            edit_id = st.session_state.get("edit_resource_id")
            edit_data = None
            
            if edit_id:
                # Fetch existing data
                all_resources = ambil_semua_sumber_daya(queries)
                edit_data = next((r for r in all_resources if str(r["_id"]) == edit_id), None)
            
            col1, col2 = st.columns(2)
            
            with col1:
                judul = st.text_input(
                    "Judul *",
                    value=edit_data.get("judul", "") if edit_data else "",
                    key="resource_judul"
                )
                
                tipe = st.selectbox(
                    "Tipe *",
                    options=["video", "artikel", "tutorial", "exercise", "quiz", "dokumentasi"],
                    index=["video", "artikel", "tutorial", "exercise", "quiz", "dokumentasi"].index(
                        edit_data.get("tipe", "video")
                    ) if edit_data else 0,
                    key="resource_tipe"
                )
                
                tingkat_kesulitan = st.selectbox(
                    "Tingkat Kesulitan *",
                    options=["pemula", "menengah", "mahir"],
                    index=["pemula", "menengah", "mahir"].index(
                        edit_data.get("tingkat_kesulitan", "pemula")
                    ) if edit_data else 0,
                    key="resource_tingkat"
                )
            
            with col2:
                url = st.text_input(
                    "URL *",
                    value=edit_data.get("url", "") if edit_data else "",
                    key="resource_url",
                    placeholder="https://..."
                )
                
                durasi = st.number_input(
                    "Durasi (menit)",
                    min_value=0,
                    value=edit_data.get("durasi", 0) if edit_data else 0,
                    key="resource_durasi"
                )
                
                bahasa = st.selectbox(
                    "Bahasa",
                    options=["Indonesia", "English"],
                    index=["Indonesia", "English"].index(
                        edit_data.get("bahasa", "Indonesia")
                    ) if edit_data else 0,
                    key="resource_bahasa"
                )
            
            deskripsi = st.text_area(
                "Deskripsi *",
                value=edit_data.get("deskripsi", "") if edit_data else "",
                key="resource_deskripsi",
                height=100
            )
            
            topik_terkait = st.text_input(
                "Topik Terkait (pisahkan dengan koma)",
                value=", ".join(edit_data.get("topik_terkait", [])) if edit_data else "",
                key="resource_topik",
                placeholder="Python Basics, Variables, Data Types"
            )
            
            col_submit, col_cancel = st.columns(2)
            
            with col_submit:
                submit = st.form_submit_button(
                    "💾 Simpan" if edit_id else "➕ Tambah",
                    use_container_width=True
                )
            
            with col_cancel:
                cancel = st.form_submit_button("❌ Batal", use_container_width=True)
            
            if submit:
                if not all([judul, tipe, tingkat_kesulitan, url, deskripsi]):
                    st.error("Semua field bertanda * wajib diisi!")
                else:
                    try:
                        topik_list = [t.strip() for t in topik_terkait.split(",") if t.strip()]
                        
                        data_resource = {
                            "judul": judul,
                            "deskripsi": deskripsi,
                            "tipe": tipe,
                            "url": url,
                            "topik_terkait": topik_list,
                            "tingkat_kesulitan": tingkat_kesulitan,
                            "durasi": durasi if durasi > 0 else None,
                            "bahasa": bahasa
                        }
                        
                        if edit_id:
                            # Update existing
                            update_sumber_daya(queries, edit_id, data_resource)
                            st.success("✅ Sumber daya berhasil diupdate!")
                        else:
                            # Add new
                            tambah_sumber_daya(queries, data_resource)
                            st.success("✅ Sumber daya baru berhasil ditambahkan!")
                        
                        st.session_state.show_resource_form = False
                        st.session_state.edit_resource_id = None
                        st.rerun()
                    
                    except Exception as e:
                        logger.error(f"Error saving resource: {e}")
                        st.error(f"❌ Error: {str(e)}")
            
            if cancel:
                st.session_state.show_resource_form = False
                st.session_state.edit_resource_id = None
                st.rerun()
    
    st.markdown("---")
    
    # List existing resources
    try:
        resources = ambil_semua_sumber_daya(queries)
        
        if not resources:
            st.info("Belum ada sumber daya. Tambahkan yang pertama!")
        else:
            st.markdown(f"**Total: {len(resources)} sumber daya**")
            
            # Filter
            col_filter1, col_filter2 = st.columns(2)
            
            with col_filter1:
                filter_tipe = st.selectbox(
                    "Filter Tipe",
                    options=["Semua", "video", "artikel", "tutorial", "exercise", "quiz", "dokumentasi"],
                    key="filter_resource_tipe"
                )
            
            with col_filter2:
                filter_tingkat = st.selectbox(
                    "Filter Tingkat",
                    options=["Semua", "pemula", "menengah", "mahir"],
                    key="filter_resource_tingkat"
                )
            
            # Apply filters
            filtered_resources = resources
            if filter_tipe != "Semua":
                filtered_resources = [r for r in filtered_resources if r.get("tipe") == filter_tipe]
            if filter_tingkat != "Semua":
                filtered_resources = [r for r in filtered_resources if r.get("tingkat_kesulitan") == filter_tingkat]
            
            st.markdown(f"*Menampilkan {len(filtered_resources)} dari {len(resources)} sumber daya*")
            
            # Display resources
            for resource in filtered_resources:
                with st.container():
                    col_info, col_actions = st.columns([8, 2])
                    
                    with col_info:
                        st.markdown(f"""
                        **{resource.get('judul', 'N/A')}** | 
                        <span style="background-color:#3b82f6;color:white;padding:2px 8px;border-radius:4px;font-size:12px;">{resource.get('tipe', 'N/A').upper()}</span> | 
                        <span style="background-color:#10b981;color:white;padding:2px 8px;border-radius:4px;font-size:12px;">{resource.get('tingkat_kesulitan', 'pemula').upper()}</span>
                        """, unsafe_allow_html=True)
                        
                        st.caption(resource.get("deskripsi", "")[:200] + ("..." if len(resource.get("deskripsi", "")) > 200 else ""))
                        
                        if resource.get("topik_terkait"):
                            st.caption(f"Topik: {', '.join(resource.get('topik_terkait', [])[:5])}")
                    
                    with col_actions:
                        if st.button("✏️ Edit", key=f"edit_resource_{resource['_id']}", use_container_width=True):
                            st.session_state.show_resource_form = True
                            st.session_state.edit_resource_id = str(resource["_id"])
                            st.rerun()
                        
                        if st.button("🗑️ Hapus", key=f"delete_resource_{resource['_id']}", use_container_width=True):
                            try:
                                hapus_sumber_daya(queries, str(resource["_id"]))
                                st.success("✅ Sumber daya berhasil dihapus!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ Error: {str(e)}")
                    
                    st.markdown("---")
    
    except Exception as e:
        logger.error(f"Error loading resources: {e}")
        st.error(f"❌ Error: {str(e)}")


# ==================== TAB 2: TOPIK PEMBELAJARAN ====================

with tab_topics:
    st.markdown("### 📚 Manage Topik Pembelajaran")
    
    # Add New Topic Button
    if st.button("➕ Tambah Topik Baru", key="add_topic_btn"):
        st.session_state.show_topic_form = True
        st.session_state.edit_topic_id = None
    
    # Add/Edit Form
    if st.session_state.get("show_topic_form", False):
        with st.form("form_topic"):
            st.markdown("#### ➕ Form Topik")
            
            edit_id = st.session_state.get("edit_topic_id")
            edit_data = None
            
            if edit_id:
                all_topics = ambil_semua_topik(queries)
                edit_data = next((t for t in all_topics if str(t["_id"]) == edit_id), None)
            
            col1, col2 = st.columns(2)
            
            with col1:
                nama = st.text_input(
                    "Nama Topik *",
                    value=edit_data.get("nama", "") if edit_data else "",
                    key="topic_nama"
                )
                
                kategori = st.selectbox(
                    "Kategori *",
                    options=["dasar", "lanjutan", "expert"],
                    index=["dasar", "lanjutan", "expert"].index(
                        edit_data.get("kategori", "dasar")
                    ) if edit_data else 0,
                    key="topic_kategori"
                )
            
            with col2:
                tingkat_kesulitan = st.selectbox(
                    "Tingkat Kesulitan *",
                    options=["pemula", "menengah", "mahir"],
                    index=["pemula", "menengah", "mahir"].index(
                        edit_data.get("tingkat_kesulitan", "pemula")
                    ) if edit_data else 0,
                    key="topic_tingkat"
                )
                
                estimasi_durasi = st.number_input(
                    "Estimasi Durasi Belajar (jam)",
                    min_value=0,
                    value=edit_data.get("estimasi_durasi", 0) if edit_data else 0,
                    key="topic_durasi"
                )
            
            deskripsi = st.text_area(
                "Deskripsi *",
                value=edit_data.get("deskripsi", "") if edit_data else "",
                key="topic_deskripsi",
                height=100
            )
            
            prerequisite = st.text_input(
                "Prerequisite (pisahkan dengan koma)",
                value=", ".join(edit_data.get("prerequisite", [])) if edit_data else "",
                key="topic_prerequisite",
                placeholder="Variables, Data Types"
            )
            
            tujuan_pembelajaran = st.text_area(
                "Tujuan Pembelajaran",
                value=edit_data.get("tujuan_pembelajaran", "") if edit_data else "",
                key="topic_tujuan",
                height=80,
                placeholder="Setelah mempelajari topik ini, mahasiswa akan mampu..."
            )
            
            col_submit, col_cancel = st.columns(2)
            
            with col_submit:
                submit = st.form_submit_button(
                    "💾 Simpan" if edit_id else "➕ Tambah",
                    use_container_width=True
                )
            
            with col_cancel:
                cancel = st.form_submit_button("❌ Batal", use_container_width=True)
            
            if submit:
                if not all([nama, kategori, tingkat_kesulitan, deskripsi]):
                    st.error("Semua field bertanda * wajib diisi!")
                else:
                    try:
                        prereq_list = [p.strip() for p in prerequisite.split(",") if p.strip()]
                        
                        data_topic = {
                            "nama": nama,
                            "deskripsi": deskripsi,
                            "kategori": kategori,
                            "tingkat_kesulitan": tingkat_kesulitan,
                            "prerequisite": prereq_list,
                            "tujuan_pembelajaran": tujuan_pembelajaran,
                            "estimasi_durasi": estimasi_durasi if estimasi_durasi > 0 else None
                        }
                        
                        if edit_id:
                            update_topik(queries, edit_id, data_topic)
                            st.success("✅ Topik berhasil diupdate!")
                        else:
                            tambah_topik(queries, data_topic)
                            st.success("✅ Topik baru berhasil ditambahkan!")
                        
                        st.session_state.show_topic_form = False
                        st.session_state.edit_topic_id = None
                        st.rerun()
                    
                    except Exception as e:
                        logger.error(f"Error saving topic: {e}")
                        st.error(f"❌ Error: {str(e)}")
            
            if cancel:
                st.session_state.show_topic_form = False
                st.session_state.edit_topic_id = None
                st.rerun()
    
    st.markdown("---")
    
    # List existing topics
    try:
        topics = ambil_semua_topik(queries)
        
        if not topics:
            st.info("Belum ada topik. Tambahkan yang pertama!")
        else:
            st.markdown(f"**Total: {len(topics)} topik**")
            
            # Filter
            filter_kategori = st.selectbox(
                "Filter Kategori",
                options=["Semua", "dasar", "lanjutan", "expert"],
                key="filter_topic_kategori"
            )
            
            # Apply filter
            filtered_topics = topics
            if filter_kategori != "Semua":
                filtered_topics = [t for t in filtered_topics if t.get("kategori") == filter_kategori]
            
            st.markdown(f"*Menampilkan {len(filtered_topics)} dari {len(topics)} topik*")
            
            # Display topics
            for topic in filtered_topics:
                with st.container():
                    col_info, col_actions = st.columns([8, 2])
                    
                    with col_info:
                        st.markdown(f"""
                        **{topic.get('nama', 'N/A')}** | 
                        <span style="background-color:#f59e0b;color:white;padding:2px 8px;border-radius:4px;font-size:12px;">{topic.get('kategori', 'dasar').upper()}</span> | 
                        <span style="background-color:#8b5cf6;color:white;padding:2px 8px;border-radius:4px;font-size:12px;">{topic.get('tingkat_kesulitan', 'pemula').upper()}</span>
                        """, unsafe_allow_html=True)
                        
                        st.caption(topic.get("deskripsi", "")[:200] + ("..." if len(topic.get("deskripsi", "")) > 200 else ""))
                        
                        if topic.get("prerequisite"):
                            st.caption(f"Prerequisite: {', '.join(topic.get('prerequisite', []))}")
                    
                    with col_actions:
                        if st.button("✏️ Edit", key=f"edit_topic_{topic['_id']}", use_container_width=True):
                            st.session_state.show_topic_form = True
                            st.session_state.edit_topic_id = str(topic["_id"])
                            st.rerun()
                        
                        if st.button("🗑️ Hapus", key=f"delete_topic_{topic['_id']}", use_container_width=True):
                            try:
                                hapus_topik(queries, str(topic["_id"]))
                                st.success("✅ Topik berhasil dihapus!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ Error: {str(e)}")
                    
                    st.markdown("---")
    
    except Exception as e:
        logger.error(f"Error loading topics: {e}")
        st.error(f"❌ Error: {str(e)}")


# ==================== TAB 3: EXERCISES ====================

with tab_exercises:
    st.markdown("### ✏️ Manage Exercises")
    
    st.info("Exercise management dengan code editor akan tersedia di versi mendatang.")
    
    # List existing exercises
    try:
        exercises = ambil_semua_exercises(queries)
        
        if not exercises:
            st.info("Belum ada exercise.")
        else:
            st.markdown(f"**Total: {len(exercises)} exercises**")
            
            for exercise in exercises[:10]:  # Show first 10
                with st.expander(f"📝 {exercise.get('judul', 'N/A')}"):
                    st.markdown(f"**Topik:** {exercise.get('topik', 'N/A')}")
                    st.markdown(f"**Tingkat:** {exercise.get('tingkat_kesulitan', 'pemula')}")
                    st.markdown(f"**Deskripsi:** {exercise.get('deskripsi', '')}")
    
    except Exception as e:
        logger.error(f"Error loading exercises: {e}")
        st.error(f"❌ Error: {str(e)}")
