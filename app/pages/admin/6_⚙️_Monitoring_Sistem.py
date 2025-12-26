"""
Admin - Monitoring Sistem (System Health)

CRITICAL ADMIN FEATURE 🔴
- AI model performance metrics
- API response times
- Error rates & failures
- Database health
- System status monitoring
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
from services.admin_service import ambil_system_health
from services.autentikasi_service import require_admin
from utils.helpers import format_number, format_percentage

logger = logging.getLogger(__name__)


# ==================== PAGE CONFIG ====================

st.set_page_config(
    page_title="Monitoring Sistem - PahamKode",
    page_icon="⚙️",
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


# ==================== SESSION STATE ====================

if "auto_refresh" not in st.session_state:
    st.session_state.auto_refresh = False


# ==================== MAIN PAGE ====================

st.title("⚙️ Monitoring Sistem")
st.markdown("Real-time system health & performance monitoring")

queries = st.session_state.queries


# ==================== HEADER CONTROLS ====================

col1, col2, col3 = st.columns([2, 2, 6])

with col1:
    if st.button("🔄 Refresh Now", use_container_width=True):
        st.rerun()

with col2:
    auto_refresh = st.checkbox(
        "Auto-refresh (30s)",
        value=st.session_state.auto_refresh,
        key="auto_refresh_checkbox"
    )
    
    if auto_refresh != st.session_state.auto_refresh:
        st.session_state.auto_refresh = auto_refresh
        st.rerun()

st.markdown("---")


# ==================== FETCH SYSTEM HEALTH ====================

try:
    with st.spinner("Checking system health..."):
        health = ambil_system_health(queries)
    
    
    # ==================== OVERALL HEALTH INDICATOR ====================
    
    overall_status = health.get("overall_status", "unknown")
    status_emoji = {
        "healthy": "✅",
        "warning": "⚠️",
        "critical": "🔴",
        "unknown": "❓"
    }.get(overall_status, "❓")
    
    status_color = {
        "healthy": "#10b981",
        "warning": "#f59e0b",
        "critical": "#ef4444",
        "unknown": "#6b7280"
    }.get(overall_status, "#6b7280")
    
    st.markdown(f"""
    <div style="background-color:{status_color};color:white;padding:20px;border-radius:12px;text-align:center;margin-bottom:20px;">
        <h2 style="margin:0;">{status_emoji} System Status: {overall_status.upper()}</h2>
        <p style="margin:8px 0 0 0;">Last checked: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    
    # ==================== DATABASE STATUS ====================
    
    st.markdown("### 🗄️ Database Health")
    
    db_health = health.get("database", {})
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        db_status = db_health.get("status", "unknown")
        st.metric(
            "Status",
            db_status.upper(),
            delta="✅" if db_status == "connected" else "❌"
        )
    
    with col2:
        ping_time = db_health.get("ping_time_ms", 0)
        st.metric(
            "Ping Time",
            f"{ping_time:.2f} ms",
            delta="Good" if ping_time < 100 else "Slow"
        )
    
    with col3:
        st.metric(
            "Total Collections",
            format_number(db_health.get("total_collections", 0))
        )
    
    with col4:
        st.metric(
            "Total Documents",
            format_number(db_health.get("total_documents", 0))
        )
    
    # Database collections detail
    if db_health.get("collections"):
        with st.expander("📊 Collections Details"):
            for coll in db_health["collections"]:
                st.markdown(f"""
                **{coll['name']}**: {format_number(coll['count'])} documents | 
                Size: {coll.get('size_mb', 0):.2f} MB
                """)
    
    st.markdown("---")
    
    
    # ==================== AI SERVICE STATUS ====================
    
    st.markdown("### 🤖 AI Service Performance")
    
    ai_health = health.get("ai_service", {})
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        ai_status = ai_health.get("status", "unknown")
        status_emoji = "✅" if ai_status == "healthy" else "⚠️" if ai_status == "degraded" else "❌"
        st.metric(
            "Status",
            ai_status.upper(),
            delta=status_emoji
        )
    
    with col2:
        success_rate = ai_health.get("success_rate_24h", 0)
        st.metric(
            "Success Rate (24h)",
            format_percentage(success_rate, 100),
            delta="Good" if success_rate >= 95 else "Low"
        )
    
    with col3:
        avg_response = ai_health.get("avg_response_time_ms", 0)
        st.metric(
            "Avg Response Time",
            f"{avg_response:.0f} ms",
            delta="Fast" if avg_response < 2000 else "Slow"
        )
    
    with col4:
        st.metric(
            "Total Requests (24h)",
            format_number(ai_health.get("total_requests_24h", 0))
        )
    
    with col5:
        st.metric(
            "Total Tokens (24h)",
            format_number(ai_health.get("total_tokens_24h", 0))
        )
    
    # AI Performance Chart (last 24 hours)
    if ai_health.get("performance_24h"):
        st.markdown("#### 📈 AI Performance (Last 24 Hours)")
        
        import pandas as pd
        df_ai_perf = pd.DataFrame(ai_health["performance_24h"])
        
        fig_ai = go.Figure()
        
        fig_ai.add_trace(go.Scatter(
            x=df_ai_perf["hour"],
            y=df_ai_perf["success_rate"],
            mode='lines+markers',
            name='Success Rate (%)',
            line=dict(color='#10b981'),
            yaxis='y'
        ))
        
        fig_ai.add_trace(go.Scatter(
            x=df_ai_perf["hour"],
            y=df_ai_perf["avg_response_time"],
            mode='lines+markers',
            name='Avg Response Time (ms)',
            line=dict(color='#3b82f6'),
            yaxis='y2'
        ))
        
        fig_ai.update_layout(
            xaxis=dict(title="Hour"),
            yaxis=dict(title="Success Rate (%)", side="left"),
            yaxis2=dict(title="Response Time (ms)", side="right", overlaying="y"),
            hovermode="x unified",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig_ai, use_container_width=True)
    
    # AI Cost tracking
    if ai_health.get("total_cost_24h"):
        st.info(f"💰 AI Cost (24h): ${ai_health['total_cost_24h']:.4f}")
    
    st.markdown("---")
    
    
    # ==================== API SERVICE STATUS ====================
    
    st.markdown("### 🌐 API Service Performance")
    
    api_health = health.get("api_service", {})
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        api_status = api_health.get("status", "unknown")
        st.metric(
            "Status",
            api_status.upper(),
            delta="✅" if api_status == "healthy" else "❌"
        )
    
    with col2:
        api_success_rate = api_health.get("success_rate_24h", 0)
        st.metric(
            "Success Rate (24h)",
            format_percentage(api_success_rate, 100),
            delta="Good" if api_success_rate >= 98 else "Low"
        )
    
    with col3:
        api_avg_response = api_health.get("avg_response_time_ms", 0)
        st.metric(
            "Avg Response Time",
            f"{api_avg_response:.0f} ms",
            delta="Fast" if api_avg_response < 500 else "Slow"
        )
    
    with col4:
        st.metric(
            "Total Requests (24h)",
            format_number(api_health.get("total_requests_24h", 0))
        )
    
    # API Error breakdown
    if api_health.get("error_breakdown"):
        with st.expander("❌ Error Breakdown (24h)"):
            for error in api_health["error_breakdown"]:
                st.markdown(f"""
                **{error['type']}**: {format_number(error['count'])} ({format_percentage(error['count'], api_health['total_requests_24h'])})
                """)
    
    st.markdown("---")
    
    
    # ==================== SYSTEM ALERTS ====================
    
    alerts = health.get("alerts", [])
    
    if alerts:
        st.markdown("### 🚨 System Alerts")
        
        for alert in alerts:
            severity = alert.get("severity", "info")
            
            if severity == "critical":
                st.error(f"🔴 **{alert['title']}**: {alert['message']}")
            elif severity == "warning":
                st.warning(f"⚠️ **{alert['title']}**: {alert['message']}")
            else:
                st.info(f"ℹ️ **{alert['title']}**: {alert['message']}")
        
        st.markdown("---")
    
    
    # ==================== RECENT ERRORS ====================
    
    st.markdown("### 🔍 Recent System Errors (Last 1 Hour)")
    
    recent_errors = health.get("recent_errors", [])
    
    if recent_errors:
        for error in recent_errors[:10]:
            with st.expander(f"❌ {error['timestamp']} - {error['type']}"):
                st.markdown(f"**Message:** {error['message']}")
                st.markdown(f"**Component:** {error.get('component', 'Unknown')}")
                if error.get("details"):
                    st.code(error["details"])
    else:
        st.success("✅ No errors in the last hour!")
    
    st.markdown("---")
    
    
    # ==================== SYSTEM RESOURCES ====================
    
    st.markdown("### 💻 System Resources")
    
    resources = health.get("system_resources", {})
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        cpu_usage = resources.get("cpu_usage_percent", 0)
        st.metric(
            "CPU Usage",
            f"{cpu_usage:.1f}%",
            delta="High" if cpu_usage > 80 else "Normal"
        )
    
    with col2:
        memory_usage = resources.get("memory_usage_percent", 0)
        st.metric(
            "Memory Usage",
            f"{memory_usage:.1f}%",
            delta="High" if memory_usage > 80 else "Normal"
        )
    
    with col3:
        disk_usage = resources.get("disk_usage_percent", 0)
        st.metric(
            "Disk Usage",
            f"{disk_usage:.1f}%",
            delta="High" if disk_usage > 80 else "Normal"
        )
    
    st.markdown("---")
    
    
    # ==================== UPTIME & STATISTICS ====================
    
    st.markdown("### 📊 System Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "System Uptime",
            health.get("uptime", "Unknown")
        )
    
    with col2:
        st.metric(
            "App Version",
            health.get("app_version", "1.0.0")
        )
    
    with col3:
        st.metric(
            "Active Users (Now)",
            format_number(health.get("active_users_now", 0))
        )
    
    with col4:
        st.metric(
            "Total Users",
            format_number(health.get("total_users", 0))
        )


except Exception as e:
    logger.error(f"Error loading system health: {e}")
    st.error(f"❌ Error: {str(e)}")


# ==================== AUTO REFRESH ====================

if st.session_state.auto_refresh:
    import time
    time.sleep(30)
    st.rerun()
