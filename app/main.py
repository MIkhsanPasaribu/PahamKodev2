"""
Main Entry Point - PahamKode Streamlit App
Landing page dengan role-based routing

CATATAN:
- Session-based authentication dengan st.session_state
- Role routing: Admin → admin pages, Mahasiswa → mahasiswa pages
- Auto-redirect based on user role
"""

import streamlit as st
import logging
from datetime import datetime

from config import settings
from database.koneksi import dapatkan_database
from database.queries import DatabaseQueries

# Setup logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ==================== PAGE CONFIG ====================

st.set_page_config(
    page_title="PahamKode - Analisis Error Semantik",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/MIkhsanPasaribu/PahamKodev2',
        'Report a bug': 'https://github.com/MIkhsanPasaribu/PahamKodev2/issues',
        'About': '''
        # PahamKode
        
        Sistem AI untuk analisis semantik error pemrograman.
        Fokus pada **MENGAPA** error terjadi, bukan hanya **BAGAIMANA** memperbaiki.
        
        Version: 1.0.0
        '''
    }
)


# ==================== SESSION INITIALIZATION ====================

def inisialisasi_session_state():
    """Initialize session state variables"""
    
    # Authentication state
    if "pengguna" not in st.session_state:
        st.session_state.pengguna = None
    
    # Database connection
    if "db" not in st.session_state:
        try:
            st.session_state.db = dapatkan_database()
            logger.info("Database connection initialized")
        except Exception as e:
            logger.error(f"Failed to connect to database: {str(e)}")
            st.error("❌ Gagal koneksi ke database. Silakan coba lagi nanti.")
            st.stop()
    
    # Database queries instance
    if "queries" not in st.session_state:
        st.session_state.queries = DatabaseQueries(st.session_state.db)
    
    # UI state
    if "page" not in st.session_state:
        st.session_state.page = "landing"


# ==================== LANDING PAGE (Not Authenticated) ====================

def tampilkan_landing_page():
    """Tampilkan landing page untuk user yang belum login"""
    
    # Hero Section
    st.title("🧠 PahamKode")
    st.subheader("Analisis Semantik Error Pemrograman dengan AI")
    
    st.markdown("""
    ---
    
    ### Apa itu PahamKode?
    
    **PahamKode** adalah sistem berbasis AI yang menganalisis error pemrograman dari sudut pandang 
    **konseptual dan semantik**, bukan hanya sintaks.
    
    Kami fokus pada **MENGAPA** error terjadi, bukan hanya **BAGAIMANA** memperbaikinya.
    
    ---
    
    ### 🎯 Fitur Utama
    
    """)
    
    # Features in columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### 🔍 **Analisis Semantik**
        - Root cause analysis dari perspektif konseptual
        - Identifikasi miskonsepsi mahasiswa
        - Penjelasan mendalam tentang "mengapa" error terjadi
        
        #### 📊 **Pattern Mining**
        - Deteksi pola kesalahan berulang (≥3x)
        - Alert otomatis saat pattern terdeteksi
        - Rekomendasi fokus pembelajaran
        """)
    
    with col2:
        st.markdown("""
        #### 🎓 **Adaptive Explanation**
        - Penjelasan disesuaikan dengan Bloom's Taxonomy
        - Level kognitif: Remember → Understand → Apply → Analyze
        - Cocok untuk pemula hingga mahir
        
        #### 📈 **Personalized Learning**
        - Progress tracking per topik
        - Rekomendasi resources dipersonalisasi
        - Practice exercises sesuai kebutuhan
        """)
    
    # Call to Action
    st.markdown("### 🚀 Mulai Sekarang!")
    
    col_login, col_register = st.columns(2)
    
    with col_login:
        if st.button("🔐 Login", type="primary", use_container_width=True):
            st.session_state.page = "login"
            st.rerun()
    
    with col_register:
        if st.button("📝 Registrasi", use_container_width=True):
            st.session_state.page = "register"
            st.rerun()
    
    # Footer
    st.markdown("""
    ---
    
    <div style='text-align: center; color: gray;'>
    <small>
    PahamKode v1.0.0 | Memahami error dari perspektif konseptual 🧠<br>
    © 2024 - Built by M. Ikhsan Pasaribu
    </small>
    </div>
    """, unsafe_allow_html=True)


# ==================== ROLE-BASED ROUTING ====================

def tampilkan_dashboard_mahasiswa():
    """Redirect ke Mahasiswa Dashboard"""
    st.info("🏠 Redirecting ke Dashboard Mahasiswa...")
    st.markdown("""
    Halaman dashboard mahasiswa sedang loading...
    
    Silakan gunakan **sidebar** untuk navigasi ke fitur lain:
    - 🔍 Analisis Error
    - 📜 Riwayat Submisi
    - 📊 Pola Error
    - 📈 Progress Belajar
    """)


def tampilkan_dashboard_admin():
    """Redirect ke Admin Dashboard"""
    st.info("📊 Redirecting ke Dashboard Admin...")
    st.markdown("""
    Halaman dashboard admin sedang loading...
    
    Silakan gunakan **sidebar** untuk navigasi ke fitur admin:
    - 📊 Dashboard Analytics
    - 👥 Kelola Pengguna
    - 📈 Analitik Global
    - 🔍 Pola Global
    - 📚 Kelola Konten
    - ⚙️ Monitoring Sistem
    """)


# ==================== MAIN FUNCTION ====================

def main():
    """Main application entry point"""
    
    # Initialize session state
    inisialisasi_session_state()
    
    # Check authentication
    pengguna = st.session_state.pengguna
    
    if pengguna is None:
        # Not authenticated - show landing or auth pages
        if st.session_state.page == "landing":
            tampilkan_landing_page()
        elif st.session_state.page == "login":
            # Import here to avoid circular import
            from components.autentikasi import render_login_page
            render_login_page()
        elif st.session_state.page == "register":
            from components.autentikasi import render_register_page
            render_register_page()
    else:
        # Authenticated - route based on role
        role = pengguna.get("role", "mahasiswa")
        
        # Show sidebar with navigation
        from components.sidebar import render_sidebar
        render_sidebar()
        
        # Show appropriate dashboard based on role
        if role == "admin":
            tampilkan_dashboard_admin()
        else:
            tampilkan_dashboard_mahasiswa()


# ==================== ENTRY POINT ====================

if __name__ == "__main__":
    main()
