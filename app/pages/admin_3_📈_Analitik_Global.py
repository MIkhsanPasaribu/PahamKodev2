"""
Admin - Analytics Global (Analitik Mendalam)

CRITICAL ADMIN FEATURE 🔴
- Analisis error per periode (hari/minggu/bulan)
- Top errors di seluruh sistem (drill-down)
- Error trends over time
- Topic difficulty ranking
- Mahasiswa performance distribution
- AI usage trends
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pandas as pd
import logging
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from components.sidebar import render_sidebar
from services.admin_service import ambil_analitik_global
from services.autentikasi_service import require_admin
from utils.helpers import format_number, format_percentage, format_datetime

logger = logging.getLogger(__name__)


# ==================== PAGE CONFIG ====================

st.set_page_config(
    page_title="Analitik Global - PahamKode",
    page_icon="📈",
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

st.title("📈 Analitik Global")
st.markdown("Analisis mendalam data sistem PahamKode")

queries = st.session_state.queries


# ==================== PERIOD SELECTOR ====================

st.markdown("### 📅 Periode Analisis")

col1, col2, col3 = st.columns([2, 2, 6])

with col1:
    period_type = st.selectbox(
        "Periode",
        options=["7_hari", "30_hari", "90_hari", "semua"],
        format_func=lambda x: {
            "7_hari": "7 Hari Terakhir",
            "30_hari": "30 Hari Terakhir",
            "90_hari": "90 Hari Terakhir",
            "semua": "Semua Data"
        }[x],
        key="period_selector"
    )

with col2:
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.rerun()

st.markdown("---")


# ==================== FETCH ANALYTICS DATA ====================

try:
    with st.spinner("Memuat data analitik..."):
        # Ensure period_type is str type
        periode: str = period_type if isinstance(period_type, str) else "30_hari"
        analytics = ambil_analitik_global(queries, periode)
    
    
    # ==================== KEY METRICS ====================
    
    st.markdown("### 📊 Metrik Utama")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Submisi",
            format_number(analytics.get("total_submisi", 0)),
            delta=f"+{analytics.get('submisi_delta', 0)}"
        )
    
    with col2:
        st.metric(
            "Unique Error Types",
            format_number(analytics.get("unique_error_types", 0))
        )
    
    with col3:
        st.metric(
            "Mahasiswa Aktif",
            format_number(analytics.get("mahasiswa_aktif", 0))
        )
    
    with col4:
        rata_penguasaan = analytics.get("rata_penguasaan_global", 0)
        st.metric(
            "Rata-rata Penguasaan",
            f"{rata_penguasaan:.1f}%",
            delta=f"{analytics.get('penguasaan_delta', 0):+.1f}%"
        )
    
    st.markdown("---")
    
    
    # ==================== ERROR TRENDS OVER TIME ====================
    
    st.markdown("### 📉 Tren Error Over Time")
    
    error_trends = analytics.get("error_trends", [])
    
    if error_trends:
        # Convert to DataFrame
        df_trends = pd.DataFrame(error_trends)
        
        # Create line chart
        fig_trends = px.line(
            df_trends,
            x="date",
            y="count",
            title="Submisi Error per Hari",
            labels={"date": "Tanggal", "count": "Jumlah Submisi"},
            markers=True
        )
        
        fig_trends.update_layout(
            hovermode="x unified",
            xaxis_title="Tanggal",
            yaxis_title="Jumlah Submisi"
        )
        
        st.plotly_chart(fig_trends, use_container_width=True)
    else:
        st.info("Tidak ada data tren untuk periode ini.")
    
    st.markdown("---")
    
    
    # ==================== TOP ERRORS WITH DRILL-DOWN ====================
    
    st.markdown("### 🔴 Top Error Types (Drill-Down)")
    
    top_errors = analytics.get("top_errors", [])
    
    if top_errors:
        # Top 10 errors table
        df_errors = pd.DataFrame(top_errors[:10])
        
        # Display table
        st.dataframe(
            df_errors,
            column_config={
                "tipe_error": st.column_config.TextColumn("Tipe Error", width="large"),
                "jumlah": st.column_config.NumberColumn("Total", format="%d"),
                "jumlah_mahasiswa": st.column_config.NumberColumn("Mahasiswa Terdampak", format="%d")
            },
            hide_index=True,
            use_container_width=True
        )
        
        # Bar chart - Top 10
        fig_errors = px.bar(
            df_errors,
            x="jumlah",
            y="tipe_error",
            orientation="h",
            title="Top 10 Error Types",
            labels={"jumlah": "Jumlah", "tipe_error": "Tipe Error"},
            color="jumlah",
            color_continuous_scale="Reds"
        )
        
        fig_errors.update_layout(yaxis={'categoryorder': 'total ascending'})
        
        st.plotly_chart(fig_errors, use_container_width=True)
        
        # Drill-down selector
        st.markdown("#### 🔍 Drill-Down Detail Error")
        
        selected_error = st.selectbox(
            "Pilih error type untuk detail",
            options=[e["tipe_error"] for e in top_errors],
            key="selected_error_drilldown"
        )
        
        if selected_error:
            # Find selected error data
            error_data = next((e for e in top_errors if e["tipe_error"] == selected_error), None)
            
            if error_data:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Total Occurrence", format_number(error_data.get("jumlah", 0)))
                
                with col2:
                    st.metric("Mahasiswa Terdampak", format_number(error_data.get("jumlah_mahasiswa", 0)))
                
                # Most common conceptual gaps
                if error_data.get("common_gaps"):
                    st.markdown("**Kesenjangan Konsep Umum:**")
                    for i, gap in enumerate(error_data["common_gaps"][:5], 1):
                        st.markdown(f"{i}. {gap}")
    else:
        st.info("Tidak ada data error untuk periode ini.")
    
    st.markdown("---")
    
    
    # ==================== TOPIC DIFFICULTY RANKING ====================
    
    st.markdown("### 📚 Topic Difficulty Ranking")
    
    topic_difficulty = analytics.get("topic_difficulty", [])
    
    if topic_difficulty:
        df_topics = pd.DataFrame(topic_difficulty[:15])
        
        # Bar chart - horizontal
        fig_topics = px.bar(
            df_topics,
            x="error_count",
            y="topik",
            orientation="h",
            title="Top 15 Topik Tersulit (berdasarkan jumlah error)",
            labels={"error_count": "Jumlah Error", "topik": "Topik"},
            color="error_count",
            color_continuous_scale="YlOrRd"
        )
        
        fig_topics.update_layout(yaxis={'categoryorder': 'total ascending'})
        
        st.plotly_chart(fig_topics, use_container_width=True)
        
        # Table view
        st.dataframe(
            df_topics,
            column_config={
                "topik": st.column_config.TextColumn("Topik", width="large"),
                "error_count": st.column_config.NumberColumn("Jumlah Error", format="%d"),
                "mahasiswa_count": st.column_config.NumberColumn("Mahasiswa Terdampak", format="%d"),
                "rata_penguasaan": st.column_config.NumberColumn("Rata-rata Penguasaan", format="%.1f%%")
            },
            hide_index=True,
            use_container_width=True
        )
    else:
        st.info("Tidak ada data topik untuk periode ini.")
    
    st.markdown("---")
    
    
    # ==================== MAHASISWA PERFORMANCE DISTRIBUTION ====================
    
    st.markdown("### 👥 Distribusi Performa Mahasiswa")
    
    performance_dist = analytics.get("performance_distribution", [])
    
    if performance_dist:
        df_perf = pd.DataFrame(performance_dist)
        
        # Histogram
        fig_perf = px.histogram(
            df_perf,
            x="tingkat_penguasaan_avg",
            nbins=20,
            title="Distribusi Rata-rata Tingkat Penguasaan Mahasiswa",
            labels={"tingkat_penguasaan_avg": "Rata-rata Penguasaan (%)", "count": "Jumlah Mahasiswa"},
            color_discrete_sequence=["#3b82f6"]
        )
        
        fig_perf.update_layout(
            xaxis_title="Rata-rata Penguasaan (%)",
            yaxis_title="Jumlah Mahasiswa",
            bargap=0.1
        )
        
        st.plotly_chart(fig_perf, use_container_width=True)
        
        # Statistics
        col1, col2, col3, col4 = st.columns(4)
        
        penguasaan_values = [p["tingkat_penguasaan_avg"] for p in performance_dist]
        
        with col1:
            st.metric("Rata-rata", f"{sum(penguasaan_values) / len(penguasaan_values):.1f}%")
        
        with col2:
            st.metric("Median", f"{sorted(penguasaan_values)[len(penguasaan_values)//2]:.1f}%")
        
        with col3:
            st.metric("Min", f"{min(penguasaan_values):.1f}%")
        
        with col4:
            st.metric("Max", f"{max(penguasaan_values):.1f}%")
    else:
        st.info("Tidak ada data distribusi performa.")
    
    st.markdown("---")
    
    
    # ==================== AI USAGE TRENDS ====================
    
    st.markdown("### 🤖 Tren Penggunaan AI")
    
    ai_usage = analytics.get("ai_usage_trends", [])
    
    if ai_usage:
        df_ai = pd.DataFrame(ai_usage)
        
        # Multi-line chart for AI metrics
        fig_ai = go.Figure()
        
        fig_ai.add_trace(go.Scatter(
            x=df_ai["date"],
            y=df_ai["total_requests"],
            mode='lines+markers',
            name='Total Requests',
            line=dict(color='#3b82f6')
        ))
        
        fig_ai.add_trace(go.Scatter(
            x=df_ai["date"],
            y=df_ai["success_count"],
            mode='lines+markers',
            name='Successful',
            line=dict(color='#10b981')
        ))
        
        fig_ai.update_layout(
            title="AI Service Usage Over Time",
            xaxis_title="Tanggal",
            yaxis_title="Jumlah Requests",
            hovermode="x unified",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig_ai, use_container_width=True)
        
        # AI Cost trends
        if any(d.get("total_cost") for d in ai_usage):
            fig_cost = px.line(
                df_ai,
                x="date",
                y="total_cost",
                title="AI Cost Over Time (USD)",
                labels={"date": "Tanggal", "total_cost": "Cost ($)"},
                markers=True
            )
            
            st.plotly_chart(fig_cost, use_container_width=True)
    else:
        st.info("Tidak ada data penggunaan AI.")
    
    st.markdown("---")
    
    
    # ==================== EXPORT DATA ====================
    
    st.markdown("### 📥 Export Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📄 Export ke CSV", use_container_width=True):
            # Combine all data for export
            export_data = {
                "period": period_type,
                "total_submisi": analytics.get("total_submisi", 0),
                "unique_errors": analytics.get("unique_error_types", 0),
                "mahasiswa_aktif": analytics.get("mahasiswa_aktif", 0),
                "rata_penguasaan": analytics.get("rata_penguasaan_global", 0)
            }
            
            df_export = pd.DataFrame([export_data])
            csv = df_export.to_csv(index=False)
            
            st.download_button(
                label="⬇️ Download CSV",
                data=csv,
                file_name=f"analytics_global_{period_type}_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
    
    with col2:
        st.info("Export PDF akan tersedia di versi mendatang.")


except Exception as e:
    logger.error(f"Error loading analytics: {e}")
    st.error(f"❌ Error: {str(e)}")
