"""
Admin - User Management (Kelola Pengguna)

CRITICAL ADMIN FEATURE 🔴
- View semua mahasiswa
- Search/filter mahasiswa
- View detail mahasiswa
- Suspend/activate mahasiswa
- Bulk operations
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import logging
from typing import List, Dict, Any
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from components.sidebar import render_sidebar
from services.admin_service import (
    ambil_daftar_mahasiswa, 
    suspend_mahasiswa,
    aktifkan_mahasiswa,
    ambil_detail_mahasiswa
)
from services.autentikasi_service import require_admin
from utils.helpers import (
    format_datetime,
    format_relative_time,
    format_number,
    get_status_color
)

logger = logging.getLogger(__name__)


# ==================== PAGE CONFIG ====================

st.set_page_config(
    page_title="Kelola Pengguna - PahamKode",
    page_icon="👥",
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


# ==================== SESSION STATE INITIALIZATION ====================

if "selected_mahasiswa_ids" not in st.session_state:
    st.session_state.selected_mahasiswa_ids = []

if "show_detail_modal" not in st.session_state:
    st.session_state.show_detail_modal = False

if "detail_mahasiswa_id" not in st.session_state:
    st.session_state.detail_mahasiswa_id = None


# ==================== MAIN PAGE ====================

st.title("👥 Kelola Pengguna")
st.markdown("Manajemen mahasiswa sistem PahamKode")

# Get queries instance from session state
queries = st.session_state.queries


# ==================== FILTERS & SEARCH ====================

st.markdown("### 🔍 Filter & Pencarian")

col1, col2, col3, col4 = st.columns([3, 2, 2, 1])

with col1:
    search_query = st.text_input(
        "Cari mahasiswa",
        placeholder="Ketik nama atau email...",
        key="search_mahasiswa"
    )

with col2:
    filter_status = st.selectbox(
        "Status",
        options=["Semua", "aktif", "suspended", "nonaktif"],
        key="filter_status"
    )

with col3:
    filter_tingkat = st.selectbox(
        "Tingkat Kemahiran",
        options=["Semua", "pemula", "menengah", "mahir"],
        key="filter_tingkat"
    )

with col4:
    per_page = st.selectbox(
        "Per Halaman",
        options=[10, 25, 50, 100],
        index=1,
        key="per_page"
    )

st.markdown("---")


# ==================== PAGINATION ====================

if "current_page" not in st.session_state:
    st.session_state.current_page = 0


# ==================== FETCH DATA ====================

try:
    # Prepare filters
    status_filter = None if filter_status == "Semua" else filter_status
    tingkat_filter = None if filter_tingkat == "Semua" else filter_tingkat
    search = search_query if search_query.strip() else None
    
    # Ensure per_page is int
    items_per_page: int = per_page if isinstance(per_page, int) else 50
    
    # Fetch mahasiswa list
    mahasiswa_list, total_count = ambil_daftar_mahasiswa(
        queries,
        page=st.session_state.current_page,
        per_page=items_per_page,
        filter_status=status_filter,
        filter_tingkat=tingkat_filter,
        search_query=search
    )
    
    # Calculate pagination info
    total_pages = (total_count + items_per_page - 1) // items_per_page
    start_idx = st.session_state.current_page * items_per_page + 1
    end_idx = min(start_idx + len(mahasiswa_list) - 1, total_count)
    
    # Display count
    st.markdown(f"**Menampilkan {start_idx}-{end_idx} dari {total_count} mahasiswa**")
    
    
    # ==================== BULK ACTIONS ====================
    
    st.markdown("### 🎯 Aksi Bulk")
    
    col1, col2, col3 = st.columns([2, 2, 6])
    
    with col1:
        if st.button("✅ Pilih Semua", use_container_width=True):
            st.session_state.selected_mahasiswa_ids = [m["_id"] for m in mahasiswa_list]
            st.rerun()
    
    with col2:
        if st.button("❌ Batalkan Pilihan", use_container_width=True):
            st.session_state.selected_mahasiswa_ids = []
            st.rerun()
    
    if len(st.session_state.selected_mahasiswa_ids) > 0:
        st.info(f"📌 {len(st.session_state.selected_mahasiswa_ids)} mahasiswa terpilih")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🚫 Suspend Mahasiswa Terpilih", use_container_width=True):
                with st.spinner("Memproses..."):
                    success_count = 0
                    for mahasiswa_id in st.session_state.selected_mahasiswa_ids:
                        try:
                            suspend_mahasiswa(queries, str(mahasiswa_id), "Bulk suspend oleh admin")
                            success_count += 1
                        except Exception as e:
                            logger.error(f"Error suspend {mahasiswa_id}: {e}")
                    
                    st.success(f"✅ Berhasil suspend {success_count} mahasiswa!")
                    st.session_state.selected_mahasiswa_ids = []
                    st.rerun()
        
        with col2:
            if st.button("✅ Aktifkan Mahasiswa Terpilih", use_container_width=True):
                with st.spinner("Memproses..."):
                    success_count = 0
                    for mahasiswa_id in st.session_state.selected_mahasiswa_ids:
                        try:
                            aktifkan_mahasiswa(queries, str(mahasiswa_id))
                            success_count += 1
                        except Exception as e:
                            logger.error(f"Error aktifkan {mahasiswa_id}: {e}")
                    
                    st.success(f"✅ Berhasil aktifkan {success_count} mahasiswa!")
                    st.session_state.selected_mahasiswa_ids = []
                    st.rerun()
    
    st.markdown("---")
    
    
    # ==================== MAHASISWA TABLE ====================
    
    st.markdown("### 📋 Daftar Mahasiswa")
    
    if not mahasiswa_list:
        st.info("Tidak ada mahasiswa yang cocok dengan filter.")
    else:
        # Display as cards for better UX
        for mahasiswa in mahasiswa_list:
            with st.container():
                col_check, col_info, col_actions = st.columns([1, 8, 3])
                
                with col_check:
                    # Checkbox for selection
                    mahasiswa_id = mahasiswa["_id"]
                    is_selected = mahasiswa_id in st.session_state.selected_mahasiswa_ids
                    
                    if st.checkbox(
                        "Pilih",
                        key=f"select_{mahasiswa_id}",
                        value=is_selected,
                        label_visibility="collapsed"
                    ):
                        if mahasiswa_id not in st.session_state.selected_mahasiswa_ids:
                            st.session_state.selected_mahasiswa_ids.append(mahasiswa_id)
                    else:
                        if mahasiswa_id in st.session_state.selected_mahasiswa_ids:
                            st.session_state.selected_mahasiswa_ids.remove(mahasiswa_id)
                
                with col_info:
                    # Status badge
                    status = mahasiswa.get("status", "aktif")
                    status_color = get_status_color(status)
                    
                    st.markdown(f"""
                    **{mahasiswa.get("nama", "N/A")}** | {mahasiswa.get("email", "N/A")}
                    
                    <span style="background-color:{status_color};color:white;padding:2px 8px;border-radius:4px;font-size:12px;font-weight:bold;">
                        {status.upper()}
                    </span>
                    """, unsafe_allow_html=True)
                    
                    st.caption(
                        f"Tingkat: {mahasiswa.get('tingkat_kemahiran', 'pemula').title()} | "
                        f"Total Submisi: {mahasiswa.get('total_submisi', 0)} | "
                        f"Bergabung: {format_relative_time(mahasiswa.get('created_at', datetime.now()))}"
                    )
                
                with col_actions:
                    # Action buttons
                    col_detail, col_action = st.columns(2)
                    
                    with col_detail:
                        if st.button("📄 Detail", key=f"detail_{mahasiswa_id}", use_container_width=True):
                            st.session_state.show_detail_modal = True
                            st.session_state.detail_mahasiswa_id = str(mahasiswa_id)
                            st.rerun()
                    
                    with col_action:
                        if status == "aktif":
                            if st.button("🚫 Suspend", key=f"suspend_{mahasiswa_id}", use_container_width=True):
                                with st.spinner("Memproses..."):
                                    suspend_mahasiswa(queries, str(mahasiswa_id), "Suspended oleh admin")
                                    st.success(f"✅ Mahasiswa {mahasiswa.get('nama')} berhasil di-suspend!")
                                    st.rerun()
                        else:
                            if st.button("✅ Aktifkan", key=f"activate_{mahasiswa_id}", use_container_width=True):
                                with st.spinner("Memproses..."):
                                    aktifkan_mahasiswa(queries, str(mahasiswa_id))
                                    st.success(f"✅ Mahasiswa {mahasiswa.get('nama')} berhasil diaktifkan!")
                                    st.rerun()
                
                st.markdown("---")
    
    
    # ==================== PAGINATION CONTROLS ====================
    
    if total_pages > 1:
        st.markdown("### 📄 Navigasi Halaman")
        
        col1, col2, col3, col4, col5 = st.columns([1, 1, 6, 1, 1])
        
        with col1:
            if st.button("⏮️ Awal", disabled=(st.session_state.current_page == 0)):
                st.session_state.current_page = 0
                st.rerun()
        
        with col2:
            if st.button("◀️ Sebelumnya", disabled=(st.session_state.current_page == 0)):
                st.session_state.current_page -= 1
                st.rerun()
        
        with col3:
            st.markdown(f"<div style='text-align:center;padding:8px;'>Halaman {st.session_state.current_page + 1} dari {total_pages}</div>", unsafe_allow_html=True)
        
        with col4:
            if st.button("Selanjutnya ▶️", disabled=(st.session_state.current_page >= total_pages - 1)):
                st.session_state.current_page += 1
                st.rerun()
        
        with col5:
            if st.button("Akhir ⏭️", disabled=(st.session_state.current_page >= total_pages - 1)):
                st.session_state.current_page = total_pages - 1
                st.rerun()


except Exception as e:
    logger.error(f"Error loading mahasiswa list: {e}")
    st.error(f"❌ Error: {str(e)}")


# ==================== DETAIL MODAL ====================

if st.session_state.show_detail_modal and st.session_state.detail_mahasiswa_id:
    try:
        detail = ambil_detail_mahasiswa(queries, st.session_state.detail_mahasiswa_id)
        
        if not detail:
            st.error("Mahasiswa tidak ditemukan!")
        else:
            # Info Umum
            st.markdown("### 👤 Informasi Umum")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Nama:** {detail.get('nama', 'N/A')}")
                st.markdown(f"**Email:** {detail.get('email', 'N/A')}")
                st.markdown(f"**Tingkat Kemahiran:** {detail.get('tingkat_kemahiran', 'pemula').title()}")
            
            with col2:
                status_color = get_status_color(detail.get('status', 'aktif'))
                st.markdown(f"**Status:** <span style='background-color:{status_color};color:white;padding:4px 12px;border-radius:4px;'>{detail.get('status', 'aktif').upper()}</span>", unsafe_allow_html=True)
                st.markdown(f"**Bergabung:** {format_datetime(detail.get('created_at', datetime.now()), 'date')}")
                st.markdown(f"**ID:** `{detail.get('_id')}`")
            
            st.markdown("---")
            
            # Statistik
            st.markdown("### 📈 Statistik")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Submisi", format_number(detail.get("total_submisi", 0)))
            
            with col2:
                st.metric("Pola Error", format_number(detail.get("total_pola", 0)))
            
            with col3:
                st.metric("Rata-rata Penguasaan", f"{detail.get('rata_rata_penguasaan', 0):.1f}%")
            
            with col4:
                st.metric("Topik Dipelajari", format_number(detail.get("total_topik", 0)))
            
            st.markdown("---")
            
            # Top Errors
            if detail.get("top_errors"):
                st.markdown("### 🔴 Top 5 Error Types")
                for i, error in enumerate(detail["top_errors"][:5], 1):
                    st.markdown(f"{i}. **{error['tipe_error']}**: {error['jumlah']} kali")
            
            # Recent Activity
            if detail.get("recent_submisi"):
                st.markdown("### 📜 Aktivitas Terbaru (5 Terakhir)")
                for submisi in detail["recent_submisi"]:
                    st.caption(
                        f"🔹 {submisi.get('tipe_error', 'N/A')} - "
                        f"{format_relative_time(submisi.get('created_at', datetime.now()))}"
                    )
            
            # Close button
            if st.button("Tutup", use_container_width=True):
                st.session_state.show_detail_modal = False
                st.session_state.detail_mahasiswa_id = None
                st.rerun()
    
    except Exception as e:
        logger.error(f"Error showing detail: {e}")
        st.error(f"❌ Error: {str(e)}")


# ==================== REFRESH BUTTON ====================

st.markdown("---")

if st.button("🔄 Refresh Data", use_container_width=True):
    st.rerun()
