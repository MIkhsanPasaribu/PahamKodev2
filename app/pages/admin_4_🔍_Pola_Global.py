"""
Admin - Pola Global (Pattern Insights)

CRITICAL ADMIN FEATURE 🔴
- Pola kesalahan paling umum di semua mahasiswa
- Miskonsepsi yang paling sering muncul
- Topik yang paling sulit
- Rekomendasi kurikulum berdasarkan data
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
from services.admin_service import ambil_pola_insights
from services.autentikasi_service import require_admin
from utils.helpers import format_number, get_severity_color

logger = logging.getLogger(__name__)


# ==================== PAGE CONFIG ====================

st.set_page_config(
    page_title="Pola Global - PahamKode",
    page_icon="🔍",
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

st.title("🔍 Pola Global & Pattern Insights")
st.markdown("Analisis pola kesalahan dan miskonsepsi di seluruh sistem")

queries = st.session_state.queries


# ==================== FETCH PATTERN INSIGHTS ====================

try:
    with st.spinner("Menganalisis pola global..."):
        insights = ambil_pola_insights(queries)
    
    
    # ==================== SUMMARY METRICS ====================
    
    st.markdown("### 📊 Ringkasan Pola")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Pola Unik",
            format_number(insights.get("total_unique_patterns", 0))
        )
    
    with col2:
        st.metric(
            "Total Occurrence",
            format_number(insights.get("total_pattern_occurrences", 0))
        )
    
    with col3:
        st.metric(
            "Mahasiswa Terdampak",
            format_number(insights.get("total_affected_students", 0))
        )
    
    with col4:
        severity_high = insights.get("high_severity_count", 0)
        st.metric(
            "Pola Severity Tinggi",
            format_number(severity_high),
            delta="⚠️" if severity_high > 0 else None
        )
    
    st.markdown("---")
    
    
    # ==================== MOST COMMON PATTERNS ====================
    
    st.markdown("### 🔴 Pola Kesalahan Paling Umum")
    
    common_patterns = insights.get("common_patterns", [])
    
    if common_patterns:
        # Display top patterns with severity indicators
        for i, pattern in enumerate(common_patterns[:10], 1):
            with st.container():
                col_rank, col_info, col_metrics = st.columns([1, 6, 3])
                
                with col_rank:
                    st.markdown(f"### #{i}")
                
                with col_info:
                    jenis = pattern["jenis_kesalahan"]
                    severity = pattern.get("severity", "sedang")
                    severity_color = get_severity_color(severity)
                    
                    st.markdown(f"""
                    <div style="background-color:{severity_color};color:white;padding:8px 12px;border-radius:6px;display:inline-block;font-weight:bold;margin-bottom:8px;">
                        {severity.upper()}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"**{jenis}**")
                    
                    # Misconception description
                    deskripsi = pattern.get("deskripsi_sample", "N/A")
                    with st.expander("📝 Deskripsi Miskonsepsi"):
                        st.markdown(deskripsi)
                    
                    # Recommendations
                    recommendations = pattern.get("recommendations", [])
                    if recommendations:
                        st.markdown("**💡 Rekomendasi:**")
                        for rec in recommendations[:3]:
                            st.markdown(f"- {rec}")
                
                with col_metrics:
                    st.metric("Total Frekuensi", format_number(pattern["total_frekuensi"]))
                    st.metric("Mahasiswa", format_number(pattern["jumlah_mahasiswa"]))
                    st.metric("Avg per Mahasiswa", f"{pattern['avg_freq_per_student']:.1f}")
                
                st.markdown("---")
        
        # Visualization - Top 15
        df_patterns = pd.DataFrame(common_patterns[:15])
        
        fig_patterns = px.bar(
            df_patterns,
            x="total_frekuensi",
            y="jenis_kesalahan",
            orientation="h",
            title="Top 15 Pola Kesalahan (by Frequency)",
            labels={"total_frekuensi": "Total Frekuensi", "jenis_kesalahan": "Jenis Kesalahan"},
            color="severity",
            color_discrete_map={"rendah": "#10b981", "sedang": "#f59e0b", "tinggi": "#ef4444"}
        )
        
        fig_patterns.update_layout(yaxis={'categoryorder': 'total ascending'})
        
        st.plotly_chart(fig_patterns, use_container_width=True)
    else:
        st.info("Tidak ada data pola untuk saat ini.")
    
    st.markdown("---")
    
    
    # ==================== MOST FREQUENT MISCONCEPTIONS ====================
    
    st.markdown("### 🧠 Miskonsepsi Paling Sering Muncul")
    
    misconceptions = insights.get("frequent_misconceptions", [])
    
    if misconceptions:
        # Group by misconception category
        st.markdown("#### Kategori Miskonsepsi:")
        
        # Create cards for each misconception
        for i, misc in enumerate(misconceptions[:8], 1):
            with st.expander(f"{i}. {misc['category']} ({format_number(misc['count'])} occurrence)"):
                st.markdown(f"**Deskripsi:** {misc['description']}")
                st.markdown(f"**Mahasiswa Terdampak:** {format_number(misc['affected_students'])}")
                
                if misc.get("related_topics"):
                    st.markdown("**Topik Terkait:**")
                    for topic in misc["related_topics"][:5]:
                        st.markdown(f"- {topic}")
                
                if misc.get("suggested_resources"):
                    st.markdown("**Sumber Daya yang Direkomendasikan:**")
                    for resource in misc["suggested_resources"][:3]:
                        st.markdown(f"- {resource}")
    else:
        st.info("Tidak ada data miskonsepsi.")
    
    st.markdown("---")
    
    
    # ==================== MOST DIFFICULT TOPICS ====================
    
    st.markdown("### 📚 Topik Paling Sulit")
    
    difficult_topics = insights.get("difficult_topics", [])
    
    if difficult_topics:
        df_topics = pd.DataFrame(difficult_topics[:12])
        
        # Create metrics grid
        cols = st.columns(3)
        
        for idx, topic in enumerate(difficult_topics[:12]):
            with cols[idx % 3]:
                with st.container():
                    st.markdown(f"""
                    <div style="border:2px solid #ef4444;border-radius:8px;padding:12px;margin-bottom:12px;">
                        <h4 style="margin:0;color:#ef4444;">#{idx+1} {topic['topik']}</h4>
                        <p style="margin:8px 0 0 0;font-size:14px;">
                            <b>{format_number(topic['error_count'])}</b> errors | 
                            <b>{format_number(topic['mahasiswa_count'])}</b> mahasiswa | 
                            Avg penguasaan: <b>{topic['avg_penguasaan']:.1f}%</b>
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Bar chart visualization
        fig_topics = px.bar(
            df_topics,
            x="error_count",
            y="topik",
            orientation="h",
            title="Topik Tersulit (berdasarkan Error Count)",
            labels={"error_count": "Jumlah Error", "topik": "Topik"},
            color="avg_penguasaan",
            color_continuous_scale="RdYlGn_r"
        )
        
        fig_topics.update_layout(yaxis={'categoryorder': 'total ascending'})
        
        st.plotly_chart(fig_topics, use_container_width=True)
        
        # Detailed table
        st.dataframe(
            df_topics,
            column_config={
                "topik": st.column_config.TextColumn("Topik", width="large"),
                "error_count": st.column_config.NumberColumn("Jumlah Error", format="%d"),
                "mahasiswa_count": st.column_config.NumberColumn("Mahasiswa Terdampak", format="%d"),
                "avg_penguasaan": st.column_config.NumberColumn("Rata-rata Penguasaan", format="%.1f%%")
            },
            hide_index=True,
            use_container_width=True
        )
    else:
        st.info("Tidak ada data topik sulit.")
    
    st.markdown("---")
    
    
    # ==================== CURRICULUM RECOMMENDATIONS ====================
    
    st.markdown("### 🎓 Rekomendasi Kurikulum")
    
    curriculum_recommendations = insights.get("curriculum_recommendations", [])
    
    if curriculum_recommendations:
        st.markdown("""
        Berdasarkan analisis pola kesalahan global, berikut rekomendasi untuk perbaikan kurikulum:
        """)
        
        for i, rec in enumerate(curriculum_recommendations, 1):
            priority = rec.get("priority", "medium")
            priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(priority, "🟡")
            
            with st.expander(f"{priority_emoji} {i}. {rec['title']} (Priority: {priority.upper()})"):
                st.markdown(f"**Kategori:** {rec['category']}")
                st.markdown(f"**Deskripsi:** {rec['description']}")
                
                if rec.get("rationale"):
                    st.markdown(f"**Alasan:** {rec['rationale']}")
                
                if rec.get("action_items"):
                    st.markdown("**Action Items:**")
                    for action in rec["action_items"]:
                        st.markdown(f"- {action}")
                
                if rec.get("expected_impact"):
                    st.markdown(f"**Expected Impact:** {rec['expected_impact']}")
                
                # Related topics/patterns
                if rec.get("related_patterns"):
                    st.markdown(f"**Related Patterns:** {', '.join(rec['related_patterns'][:5])}")
    else:
        st.info("Tidak ada rekomendasi kurikulum saat ini.")
    
    st.markdown("---")
    
    
    # ==================== PATTERN EVOLUTION TIMELINE ====================
    
    st.markdown("### 📅 Evolusi Pola Over Time")
    
    pattern_evolution = insights.get("pattern_evolution", [])
    
    if pattern_evolution:
        df_evolution = pd.DataFrame(pattern_evolution)
        
        # Line chart showing pattern frequency over time
        fig_evolution = px.line(
            df_evolution,
            x="month",
            y="frequency",
            color="pattern_type",
            title="Evolusi Pola Kesalahan per Bulan",
            labels={"month": "Bulan", "frequency": "Frekuensi", "pattern_type": "Tipe Pola"},
            markers=True
        )
        
        fig_evolution.update_layout(
            hovermode="x unified",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig_evolution, use_container_width=True)
    else:
        st.info("Data evolusi pola tidak tersedia.")
    
    st.markdown("---")
    
    
    # ==================== ACTIONABLE INSIGHTS ====================
    
    st.markdown("### 💡 Actionable Insights")
    
    actionable_insights = insights.get("actionable_insights", [])
    
    if actionable_insights:
        # Display insights as cards
        cols = st.columns(2)
        
        for idx, insight in enumerate(actionable_insights):
            with cols[idx % 2]:
                st.info(f"""
                **{insight['title']}**
                
                {insight['description']}
                
                **Recommended Action:** {insight['action']}
                """)
    else:
        # Generate default insights
        st.info("""
        **🔍 Fokus pada Pola Frekuensi Tinggi**
        
        Prioritaskan untuk menangani pola dengan severity tinggi dan frekuensi tinggi terlebih dahulu.
        """)
        
        st.info("""
        **📚 Perkuat Materi Topik Sulit**
        
        Tambahkan resources tambahan untuk topik dengan error count tertinggi.
        """)
    
    st.markdown("---")
    
    
    # ==================== REFRESH & EXPORT ====================
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.rerun()
    
    with col2:
        if st.button("📥 Export Report", use_container_width=True):
            st.info("Export functionality akan tersedia di versi mendatang.")


except Exception as e:
    logger.error(f"Error loading pattern insights: {e}")
    st.error(f"❌ Error: {str(e)}")
