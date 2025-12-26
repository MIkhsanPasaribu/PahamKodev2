"""
Admin Dashboard - Analytics Overview

CRITICAL ADMIN FEATURE 🔴
Dashboard dengan statistik lengkap sistem
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import logging
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from components.sidebar import render_sidebar
from services.admin_service import ambil_dashboard_statistik
from services.autentikasi_service import require_admin
from utils.helpers import format_number, format_percentage, format_relative_time

logger = logging.getLogger(__name__)


# ==================== PAGE CONFIG ====================

st.set_page_config(
    page_title="Dashboard Admin - PahamKode",
    page_icon="📊",
    layout="wide"
)


# ==================== AUTHENTICATION CHECK ====================

# Check login
if "pengguna" not in st.session_state or st.session_state.pengguna is None:
    st.error("❌ Anda harus login terlebih dahulu!")
    st.stop()

# Check admin role
if not require_admin(st.session_state.pengguna):
    st.error("❌ Akses ditolak! Halaman ini hanya untuk Admin.")
    st.stop()


# ==================== SIDEBAR ====================

render_sidebar()


# ==================== MAIN PAGE ====================

st.title("📊 Dashboard Admin")
st.markdown("---")

# Get data
queries = st.session_state.queries

# Initialize stats to prevent unbound variable error
stats = None

with st.spinner("📊 Memuat statistik..."):
    try:
        stats = ambil_dashboard_statistik(queries)
    except Exception as e:
        logger.error(f"Error loading dashboard stats: {str(e)}")
        st.error(f"❌ Error memuat statistik: {str(e)}")
        st.stop()

# Ensure stats loaded successfully
if not stats:
    st.error("❌ Gagal memuat data dashboard.")
    st.stop()


# ==================== KEY METRICS ====================

st.subheader("📈 Metrik Utama")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="👥 Total Mahasiswa",
        value=format_number(stats.get("total_mahasiswa", 0), 0),
        delta=None
    )

with col2:
    st.metric(
        label="📝 Total Submisi",
        value=format_number(stats.get("total_submisi", 0), 0),
        delta=None
    )

with col3:
    ai_metrics = stats.get("ai_metrics", {})
    total_ai_requests = ai_metrics.get("total_request", 0)
    st.metric(
        label="🤖 AI Requests (7d)",
        value=format_number(total_ai_requests, 0),
        delta=None
    )

with col4:
    success_rate = ai_metrics.get("success_rate", 0)
    st.metric(
        label="✅ AI Success Rate",
        value=f"{success_rate:.1f}%",
        delta=None,
        delta_color="normal" if success_rate >= 95 else "inverse"
    )

st.markdown("---")


# ==================== PERTUMBUHAN MAHASISWA ====================

st.subheader("📈 Pertumbuhan Mahasiswa (30 Hari Terakhir)")

pertumbuhan = stats.get("pertumbuhan_mahasiswa", [])

if pertumbuhan:
    # Prepare data for chart
    dates = [p["_id"] for p in pertumbuhan]
    counts = [p["jumlah"] for p in pertumbuhan]
    
    fig = px.line(
        x=dates,
        y=counts,
        labels={"x": "Tanggal", "y": "Jumlah Registrasi"},
        title="Registrasi Mahasiswa Baru per Hari"
    )
    
    fig.update_traces(mode="lines+markers")
    fig.update_layout(hovermode="x unified")
    
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("ℹ️ Belum ada data pertumbuhan")


# ==================== TOP ERRORS ====================

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🔴 Top Errors Global")
    
    top_errors = stats.get("top_errors", [])
    
    if top_errors:
        # Display as table
        error_data = []
        for err in top_errors[:10]:
            error_data.append({
                "Error Type": err.get("tipe_error", "Unknown"),
                "Jumlah": err.get("jumlah", 0),
                "Mahasiswa Terdampak": err.get("jumlah_mahasiswa", 0)
            })
        
        st.dataframe(error_data, use_container_width=True, hide_index=True)
        
        # Chart
        error_types = [e.get("tipe_error", "Unknown") for e in top_errors[:5]]
        error_counts = [e.get("jumlah", 0) for e in top_errors[:5]]
        
        fig = px.bar(
            x=error_counts,
            y=error_types,
            orientation='h',
            labels={"x": "Jumlah Error", "y": "Tipe Error"},
            title="Top 5 Error Types"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("ℹ️ Belum ada data error")


with col_right:
    st.subheader("⚠️ Mahasiswa Perlu Bantuan")
    
    mahasiswa_kesulitan = stats.get("mahasiswa_perlu_bantuan", [])
    
    if mahasiswa_kesulitan:
        # Display as table
        mhs_data = []
        for mhs in mahasiswa_kesulitan[:10]:
            mhs_data.append({
                "Nama": mhs.get("nama") or mhs.get("email", "N/A"),
                "Total Error": mhs.get("total_error", 0),
                "Unique Errors": mhs.get("unique_error_count", 0)
            })
        
        st.dataframe(mhs_data, use_container_width=True, hide_index=True)
    else:
        st.info("ℹ️ Semua mahasiswa dalam kondisi baik")


st.markdown("---")


# ==================== POLA GLOBAL ====================

st.subheader("🔍 Pola Error Global")

pola_global = stats.get("pola_global", [])

if pola_global:
    pola_data = []
    for pola in pola_global[:10]:
        pola_data.append({
            "Jenis Kesalahan": pola.get("jenis_kesalahan", "Unknown"),
            "Total Frekuensi": pola.get("total_frekuensi", 0),
            "Jumlah Mahasiswa": pola.get("jumlah_mahasiswa", 0),
            "Rata-rata/Mahasiswa": round(
                pola.get("total_frekuensi", 0) / max(pola.get("jumlah_mahasiswa", 1), 1),
                2
            )
        })
    
    st.dataframe(pola_data, use_container_width=True, hide_index=True)
else:
    st.info("ℹ️ Belum ada pola terdeteksi")


st.markdown("---")


# ==================== TOPIK SULIT ====================

st.subheader("📚 Topik Paling Sulit")

topik_sulit = stats.get("topik_sulit", [])

if topik_sulit:
    # Prepare data
    topik_names = [t.get("nama", "Unknown") for t in topik_sulit[:10]]
    topik_errors = [t.get("total_error", 0) for t in topik_sulit[:10]]
    
    fig = px.bar(
        x=topik_errors,
        y=topik_names,
        orientation='h',
        labels={"x": "Total Error", "y": "Topik"},
        title="10 Topik dengan Error Terbanyak"
    )
    
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("ℹ️ Belum ada data topik")


st.markdown("---")


# ==================== AI & API METRICS ====================

col_ai, col_api = st.columns(2)

with col_ai:
    st.subheader("🤖 AI Performance (7 hari)")
    
    ai_stats = stats.get("ai_metrics", {})
    
    st.metric("Total Request", format_number(ai_stats.get("total_request", 0), 0))
    st.metric("Success Rate", f"{ai_stats.get('success_rate', 0):.1f}%")
    st.metric("Avg Response Time", f"{ai_stats.get('rata_rata_waktu_respons', 0):.2f}s")
    st.metric("Total Tokens", format_number(ai_stats.get("total_token", 0), 0))
    st.metric("Total Cost", f"${ai_stats.get('total_biaya', 0):.4f}")

with col_api:
    st.subheader("⚡ API Performance (7 hari)")
    
    api_stats = stats.get("api_metrics", {})
    
    st.metric("Total Request", format_number(api_stats.get("total_request", 0), 0))
    st.metric("Success Rate", f"{api_stats.get('success_rate', 0):.1f}%")
    st.metric("Avg Response Time", f"{api_stats.get('rata_rata_waktu', 0):.0f}ms")


st.markdown("---")


# ==================== REFRESH BUTTON ====================

if st.button("🔄 Refresh Dashboard", type="primary"):
    st.rerun()


# ==================== FOOTER ====================

st.markdown(f"""
<div style='text-align: center; color: gray; margin-top: 2rem;'>
<small>Dashboard diperbarui: {format_relative_time(datetime.now())}</small>
</div>
""", unsafe_allow_html=True)
