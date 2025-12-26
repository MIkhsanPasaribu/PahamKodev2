"""
Services Package - Business Logic Layer

CATATAN:
- AI Service: LangChain + GitHub Models integration
- Analisis Service: Main error analysis orchestration
- Autentikasi Service: Session-based auth
- Admin Service: Admin operations & analytics
"""

# AI Service
from .ai_service import (
    analisis_error_semantik as ai_analisis_error_semantik,
    HasilAnalisis,
    dapatkan_llm,
    hitung_token_estimasi,
    hitung_biaya_estimasi
)

# Analisis Service
from .analisis_service import (
    proses_analisis_error,
    format_hasil_analisis,
    ambil_rekomendasi_belajar,
    hitung_statistik_mahasiswa
)

# Autentikasi Service
from .autentikasi_service import (
    registrasi_pengguna,
    login_pengguna,
    logout_pengguna,
    hash_password,
    verify_password,
    is_admin,
    is_mahasiswa,
    require_login,
    require_admin,
    update_profil_mahasiswa,
    ubah_password
)

# Admin Service
from .admin_service import (
    ambil_daftar_mahasiswa,
    suspend_mahasiswa,
    aktifkan_mahasiswa,
    ambil_dashboard_statistik,
    ambil_analitik_global,
    ambil_pola_insights,
    kelola_sumber_daya,
    kelola_topik,
    kelola_exercise,
    ambil_system_health
)

__all__ = [
    # AI Service
    'ai_analisis_error_semantik',
    'HasilAnalisis',
    'dapatkan_llm',
    'hitung_token_estimasi',
    'hitung_biaya_estimasi',
    # Analisis Service
    'proses_analisis_error',
    'format_hasil_analisis',
    'ambil_rekomendasi_belajar',
    'hitung_statistik_mahasiswa',
    # Autentikasi Service
    'registrasi_pengguna',
    'login_pengguna',
    'logout_pengguna',
    'hash_password',
    'verify_password',
    'is_admin',
    'is_mahasiswa',
    'require_login',
    'require_admin',
    'update_profil_mahasiswa',
    'ubah_password',
    # Admin Service
    'ambil_daftar_mahasiswa',
    'suspend_mahasiswa',
    'aktifkan_mahasiswa',
    'ambil_dashboard_statistik',
    'ambil_analitik_global',
    'ambil_pola_insights',
    'kelola_sumber_daya',
    'kelola_topik',
    'kelola_exercise',
    'ambil_system_health',
]
