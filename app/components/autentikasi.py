"""
Autentikasi Components - Login & Register Forms

CATATAN:
- Menggunakan st.session_state untuk session management
- Terintegrasi dengan autentikasi_service
- Auto-redirect setelah login berhasil
"""

import streamlit as st
import logging
from datetime import datetime

from app.services.autentikasi_service import (
    login_pengguna,
    registrasi_pengguna
)

logger = logging.getLogger(__name__)


# ==================== LOGIN PAGE ====================

def render_login_page():
    """Render halaman login"""
    
    st.title("🔐 Login ke PahamKode")
    st.markdown("---")
    
    # Info message
    st.info("ℹ️ Masukkan email dan password Anda untuk login")
    
    # Login form
    with st.form("form_login", clear_on_submit=False):
        email = st.text_input(
            "📧 Email",
            placeholder="contoh@email.com",
            help="Email yang Anda gunakan saat registrasi"
        )
        
        password = st.text_input(
            "🔒 Password",
            type="password",
            placeholder="Masukkan password Anda",
            help="Minimal 6 karakter"
        )
        
        col_submit, col_back = st.columns([3, 1])
        
        with col_submit:
            submit = st.form_submit_button(
                "🚀 Login",
                type="primary",
                use_container_width=True
            )
        
        with col_back:
            back = st.form_submit_button(
                "← Kembali",
                use_container_width=True
            )
        
        if back:
            st.session_state.page = "landing"
            st.rerun()
        
        if submit:
            # Validasi input
            if not email or not password:
                st.error("❌ Email dan password harus diisi!")
                return
            
            # Attempt login
            with st.spinner("🔄 Memproses login..."):
                queries = st.session_state.queries
                success, user_data, message = login_pengguna(
                    queries=queries,
                    email=email,
                    password=password
                )
            
            if success:
                # Save user to session
                st.session_state.pengguna = user_data
                st.success(f"✅ {message}")
                
                # Log successful login
                role = user_data.get("role", "mahasiswa")
                logger.info(f"Login successful: {email} (Role: {role})")
                
                # Redirect based on role
                st.balloons()
                st.rerun()
            else:
                st.error(f"❌ {message}")
                logger.warning(f"Login failed: {email}")
    
    # Link to register
    st.markdown("---")
    st.markdown("**Belum punya akun?**")
    
    if st.button("📝 Registrasi Akun Baru", use_container_width=True):
        st.session_state.page = "register"
        st.rerun()
    
    # Help section
    with st.expander("❓ Butuh Bantuan?"):
        st.markdown("""
        **Lupa Password?**
        - Hubungi administrator untuk reset password
        
        **Tidak bisa login?**
        - Pastikan email dan password sudah benar
        - Cek koneksi internet Anda
        - Jika masih gagal, hubungi support
        
        **Akun tersuspend?**
        - Hubungi administrator untuk informasi lebih lanjut
        """)


# ==================== REGISTER PAGE ====================

def render_register_page():
    """Render halaman registrasi"""
    
    st.title("📝 Registrasi Akun Baru")
    st.markdown("---")
    
    # Info message
    st.info("ℹ️ Buat akun untuk mulai menggunakan PahamKode")
    
    # Register form
    with st.form("form_register", clear_on_submit=True):
        nama = st.text_input(
            "👤 Nama Lengkap",
            placeholder="Nama lengkap Anda",
            help="Nama akan ditampilkan di dashboard"
        )
        
        email = st.text_input(
            "📧 Email",
            placeholder="contoh@email.com",
            help="Gunakan email aktif yang valid"
        )
        
        password = st.text_input(
            "🔒 Password",
            type="password",
            placeholder="Minimal 6 karakter",
            help="Buat password yang kuat"
        )
        
        password_konfirmasi = st.text_input(
            "🔒 Konfirmasi Password",
            type="password",
            placeholder="Ketik ulang password Anda"
        )
        
        # Disclaimer
        st.markdown("""
        <small>
        Dengan mendaftar, Anda menyetujui untuk menggunakan PahamKode 
        sebagai tool pembelajaran pemrograman.
        </small>
        """, unsafe_allow_html=True)
        
        col_submit, col_back = st.columns([3, 1])
        
        with col_submit:
            submit = st.form_submit_button(
                "✅ Daftar Sekarang",
                type="primary",
                use_container_width=True
            )
        
        with col_back:
            back = st.form_submit_button(
                "← Kembali",
                use_container_width=True
            )
        
        if back:
            st.session_state.page = "landing"
            st.rerun()
        
        if submit:
            # Validasi input
            if not all([nama, email, password, password_konfirmasi]):
                st.error("❌ Semua field harus diisi!")
                return
            
            if password != password_konfirmasi:
                st.error("❌ Password tidak cocok! Pastikan kedua password sama.")
                return
            
            # Attempt registration
            with st.spinner("🔄 Membuat akun..."):
                queries = st.session_state.queries
                success, message = registrasi_pengguna(
                    queries=queries,
                    email=email,
                    password=password,
                    nama=nama,
                    role="mahasiswa"
                )
            
            if success:
                st.success(f"✅ {message}")
                logger.info(f"Registration successful: {email}")
                
                # Show next steps
                st.info("🎉 Akun berhasil dibuat! Silakan login untuk melanjutkan.")
                
                st.balloons()
                
                # Auto-redirect to login after 2 seconds
                import time
                time.sleep(2)
                st.session_state.page = "login"
                st.rerun()
            else:
                st.error(f"❌ {message}")
                logger.warning(f"Registration failed: {email}")
    
    # Link to login
    st.markdown("---")
    st.markdown("**Sudah punya akun?**")
    
    if st.button("🔐 Login Sekarang", use_container_width=True):
        st.session_state.page = "login"
        st.rerun()


# ==================== LOGOUT FUNCTION ====================

def handle_logout():
    """Handle user logout"""
    
    # Get user email for logging
    email = st.session_state.pengguna.get("email", "Unknown") if st.session_state.pengguna else "Unknown"
    
    # Clear session state
    st.session_state.pengguna = None
    st.session_state.page = "landing"
    
    # Log logout
    logger.info(f"User logged out: {email}")
    
    # Show success message
    st.success("👋 Logout berhasil! Sampai jumpa!")
    
    # Rerun to redirect to landing
    st.rerun()
