"""
Sidebar Component - Navigation & User Info

CATATAN:
- Role-based menu (Admin vs Mahasiswa)
- User profile display
- Logout button
"""

import streamlit as st
import logging
from datetime import datetime

from app.components.autentikasi import handle_logout

logger = logging.getLogger(__name__)


# ==================== SIDEBAR RENDERER ====================

def render_sidebar():
    """Render sidebar dengan navigation & user info"""
    
    with st.sidebar:
        # User info section
        pengguna = st.session_state.pengguna
        
        if pengguna:
            # Profile header
            st.markdown("### 👤 Profile")
            
            nama = pengguna.get("nama") or pengguna.get("email", "User")
            email = pengguna.get("email", "")
            role = pengguna.get("role", "mahasiswa")
            tingkat = pengguna.get("tingkat_kemahiran", "pemula")
            
            # Display profile info
            st.markdown(f"""
            **Nama:** {nama}  
            **Email:** {email}  
            **Role:** {'🔧 Admin' if role == 'admin' else '🎓 Mahasiswa'}  
            """)
            
            if role == "mahasiswa":
                st.markdown(f"**Level:** {tingkat.title()}")
            
            st.markdown("---")
            
            # Navigation based on role
            if role == "admin":
                render_admin_navigation()
            else:
                render_mahasiswa_navigation()
            
            st.markdown("---")
            
            # Logout button
            if st.button("🚪 Logout", use_container_width=True, type="secondary"):
                handle_logout()
        
        # Footer
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center;'>
        <small>PahamKode v1.0.0<br>© 2024</small>
        </div>
        """, unsafe_allow_html=True)


# ==================== ADMIN NAVIGATION ====================

def render_admin_navigation():
    """Render navigation menu untuk Admin"""
    
    st.markdown("### 🔧 Admin Menu")
    
    # Dashboard
    if st.button("📊 Dashboard", use_container_width=True):
        st.switch_page("pages/admin/1_📊_Dashboard_Admin.py")
    
    # User Management
    if st.button("👥 Kelola Pengguna", use_container_width=True):
        st.switch_page("pages/admin/2_👥_Kelola_Pengguna.py")
    
    # Analytics
    if st.button("📈 Analitik Global", use_container_width=True):
        st.switch_page("pages/admin/3_📈_Analitik_Global.py")
    
    # Patterns
    if st.button("🔍 Pola Global", use_container_width=True):
        st.switch_page("pages/admin/4_🔍_Pola_Global.py")
    
    # Content Management
    if st.button("📚 Kelola Konten", use_container_width=True):
        st.switch_page("pages/admin/5_📚_Kelola_Konten.py")
    
    # System Monitoring
    if st.button("⚙️ Monitoring Sistem", use_container_width=True):
        st.switch_page("pages/admin/6_⚙️_Monitoring_Sistem.py")


# ==================== MAHASISWA NAVIGATION ====================

def render_mahasiswa_navigation():
    """Render navigation menu untuk Mahasiswa"""
    
    st.markdown("### 🎓 Mahasiswa Menu")
    
    # Dashboard
    if st.button("🏠 Dashboard", use_container_width=True):
        st.switch_page("pages/mahasiswa/1_🏠_Dashboard.py")
    
    # Analisis Error
    if st.button("🔍 Analisis Error", use_container_width=True):
        st.switch_page("pages/mahasiswa/2_🔍_Analisis.py")
    
    # Riwayat
    if st.button("📜 Riwayat", use_container_width=True):
        st.switch_page("pages/mahasiswa/3_📜_Riwayat.py")
    
    # Pola Error
    if st.button("📊 Pola Error", use_container_width=True):
        st.switch_page("pages/mahasiswa/4_📊_Pola.py")
    
    # Progress
    if st.button("📈 Progress Belajar", use_container_width=True):
        st.switch_page("pages/mahasiswa/5_📈_Progress.py")
    
    # Sumber Belajar
    if st.button("📚 Sumber Belajar", use_container_width=True):
        st.switch_page("pages/mahasiswa/6_📚_Sumber_Belajar.py")
    
    # Latihan
    if st.button("✏️ Latihan", use_container_width=True):
        st.switch_page("pages/mahasiswa/7_✏️_Latihan.py")
    
    # Export
    if st.button("📄 Export", use_container_width=True):
        st.switch_page("pages/mahasiswa/8_📄_Export.py")


# ==================== HELPER FUNCTIONS ====================

def get_current_page_name() -> str:
    """Get current page name for highlighting active menu"""
    try:
        import os
        current_file = os.path.basename(__file__)
        return current_file
    except:
        return ""
