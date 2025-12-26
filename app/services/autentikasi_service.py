"""
Autentikasi Service - Session-based Authentication dengan Streamlit

CATATAN:
- Menggunakan st.session_state untuk session management
- bcrypt untuk password hashing
- Role-based access control (mahasiswa, admin)
"""

import logging
import bcrypt
from typing import Optional, Dict, Any, Tuple
from datetime import datetime

from database.queries import DatabaseQueries
from database.models import Pengguna

logger = logging.getLogger(__name__)


# ==================== PASSWORD UTILITIES ====================

def hash_password(password: str) -> str:
    """
    Hash password menggunakan bcrypt
    
    Args:
        password: Plain text password
    
    Returns:
        Hashed password string
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(password: str, password_hash: str) -> bool:
    """
    Verify password terhadap hash
    
    Args:
        password: Plain text password untuk diverifikasi
        password_hash: Stored hash dari database
    
    Returns:
        True jika password cocok, False jika tidak
    """
    try:
        return bcrypt.checkpw(
            password.encode('utf-8'),
            password_hash.encode('utf-8')
        )
    except Exception as e:
        logger.error(f"Error verify password: {str(e)}")
        return False


# ==================== AUTHENTICATION FUNCTIONS ====================

def registrasi_pengguna(
    queries: DatabaseQueries,
    email: str,
    password: str,
    nama: Optional[str] = None,
    role: str = "mahasiswa"
) -> Tuple[bool, str]:
    """
    Registrasi user baru (mahasiswa atau admin)
    
    Args:
        queries: DatabaseQueries instance
        email: User email (unique identifier)
        password: Plain text password
        nama: User full name
        role: User role ("mahasiswa" atau "admin")
    
    Returns:
        Tuple of (success: bool, message: str)
    """
    try:
        # 1. Validasi email format
        if not email or "@" not in email:
            return False, "Email tidak valid!"
        
        # 2. Check jika email sudah terdaftar
        existing_user = queries.cari_pengguna_by_email(email)
        if existing_user:
            return False, "Email sudah terdaftar! Silakan login."
        
        # 3. Validasi password strength
        if not password or len(password) < 6:
            return False, "Password harus minimal 6 karakter!"
        
        # 4. Hash password
        password_hash = hash_password(password)
        
        # 5. Create Pengguna object
        pengguna = Pengguna(
            email=email,
            nama=nama,
            password_hash=password_hash,
            role=role,
            status="aktif",
            tingkat_kemahiran="pemula",
            created_at=datetime.now()
        )
        
        # 6. Save ke database
        id_pengguna = queries.buat_pengguna(pengguna.to_dict())
        
        logger.info(f"User baru terdaftar: {email} (ID: {id_pengguna})")
        
        return True, f"Registrasi berhasil! Selamat datang, {nama or email}!"
        
    except Exception as e:
        logger.error(f"Error registrasi: {str(e)}", exc_info=True)
        return False, f"Error registrasi: {str(e)}"


def login_pengguna(
    queries: DatabaseQueries,
    email: str,
    password: str
) -> Tuple[bool, Optional[Dict[str, Any]], str]:
    """
    Login user dan return user data
    
    Args:
        queries: DatabaseQueries instance
        email: User email
        password: Plain text password
    
    Returns:
        Tuple of (success: bool, user_data: dict or None, message: str)
    """
    try:
        # 1. Validasi input
        if not email or not password:
            return False, None, "Email dan password harus diisi!"
        
        # 2. Find user by email
        pengguna = queries.cari_pengguna_by_email(email)
        
        if not pengguna:
            logger.warning(f"Login failed - user not found: {email}")
            return False, None, "Email atau password salah!"
        
        # 3. Check user status
        if pengguna.get("status") == "suspended":
            logger.warning(f"Login blocked - suspended user: {email}")
            return False, None, "Akun Anda telah ditangguhkan. Hubungi admin."
        
        if pengguna.get("status") == "nonaktif":
            logger.warning(f"Login blocked - inactive user: {email}")
            return False, None, "Akun Anda tidak aktif."
        
        # 4. Verify password
        password_hash = pengguna.get("password_hash", "")
        
        if not verify_password(password, password_hash):
            logger.warning(f"Login failed - wrong password for: {email}")
            return False, None, "Email atau password salah!"
        
        # 5. Update last login
        queries.update_last_login(str(pengguna["_id"]))
        
        # 6. Remove password hash dari return data (security)
        user_data = {
            "_id": pengguna["_id"],
            "email": pengguna["email"],
            "nama": pengguna.get("nama"),
            "role": pengguna.get("role", "mahasiswa"),
            "status": pengguna.get("status", "aktif"),
            "tingkat_kemahiran": pengguna.get("tingkat_kemahiran", "pemula"),
            "created_at": pengguna.get("created_at"),
            "last_login": datetime.now()
        }
        
        logger.info(f"Login successful: {email} (Role: {user_data['role']})")
        
        return True, user_data, f"Selamat datang kembali, {user_data.get('nama') or email}!"
        
    except Exception as e:
        logger.error(f"Error login: {str(e)}", exc_info=True)
        return False, None, f"Error login: {str(e)}"


def logout_pengguna() -> Tuple[bool, str]:
    """
    Logout user (clear session state)
    
    NOTE: Actual session clearing dilakukan di Streamlit component,
    function ini hanya untuk logging purposes
    
    Returns:
        Tuple of (success: bool, message: str)
    """
    try:
        logger.info("User logged out")
        return True, "Logout berhasil! Sampai jumpa!"
    except Exception as e:
        logger.error(f"Error logout: {str(e)}")
        return False, "Error logout"


# ==================== AUTHORIZATION HELPERS ====================

def is_admin(user_data: Optional[Dict[str, Any]]) -> bool:
    """
    Check apakah user adalah admin
    
    Args:
        user_data: User data dari session state
    
    Returns:
        True jika admin, False jika bukan
    """
    if not user_data:
        return False
    
    return user_data.get("role") == "admin"


def is_mahasiswa(user_data: Optional[Dict[str, Any]]) -> bool:
    """
    Check apakah user adalah mahasiswa
    
    Args:
        user_data: User data dari session state
    
    Returns:
        True jika mahasiswa, False jika bukan
    """
    if not user_data:
        return False
    
    return user_data.get("role") == "mahasiswa"


def require_login(user_data: Optional[Dict[str, Any]]) -> bool:
    """
    Check apakah user sudah login
    
    Args:
        user_data: User data dari session state
    
    Returns:
        True jika sudah login, False jika belum
    """
    return user_data is not None


def require_admin(user_data: Optional[Dict[str, Any]]) -> bool:
    """
    Check apakah user adalah admin (untuk protected admin pages)
    
    Args:
        user_data: User data dari session state
    
    Returns:
        True jika admin, False jika bukan
    """
    return is_admin(user_data)


# ==================== PROFILE MANAGEMENT ====================

def update_profil_mahasiswa(
    queries: DatabaseQueries,
    id_mahasiswa: str,
    nama: Optional[str] = None,
    tingkat_kemahiran: Optional[str] = None
) -> Tuple[bool, str]:
    """
    Update profil mahasiswa
    
    Args:
        queries: DatabaseQueries instance
        id_mahasiswa: Student ID
        nama: New name (optional)
        tingkat_kemahiran: New proficiency level (optional)
    
    Returns:
        Tuple of (success: bool, message: str)
    """
    try:
        mahasiswa = queries.cari_pengguna_by_id(id_mahasiswa)
        
        if not mahasiswa:
            return False, "Mahasiswa tidak ditemukan!"
        
        # Update fields
        from bson import ObjectId
        
        update_data: Dict[str, Any] = {}
        if nama:
            update_data["nama"] = nama
        if tingkat_kemahiran:
            update_data["tingkat_kemahiran"] = tingkat_kemahiran
        
        if not update_data:
            return False, "Tidak ada data yang diupdate!"
        
        # Update in database
        from pymongo.database import Database
        queries.db.users.update_one(
            {"_id": ObjectId(id_mahasiswa)},
            {"$set": update_data}
        )
        
        logger.info(f"Profil updated: {id_mahasiswa}")
        
        return True, "Profil berhasil diperbarui!"
        
    except Exception as e:
        logger.error(f"Error update profil: {str(e)}")
        return False, f"Error update profil: {str(e)}"


def ubah_password(
    queries: DatabaseQueries,
    id_pengguna: str,
    password_lama: str,
    password_baru: str
) -> Tuple[bool, str]:
    """
    Ubah password user
    
    Args:
        queries: DatabaseQueries instance
        id_pengguna: User ID
        password_lama: Old password untuk verifikasi
        password_baru: New password
    
    Returns:
        Tuple of (success: bool, message: str)
    """
    try:
        # 1. Get user
        pengguna = queries.cari_pengguna_by_id(id_pengguna)
        
        if not pengguna:
            return False, "User tidak ditemukan!"
        
        # 2. Verify password lama
        if not verify_password(password_lama, pengguna["password_hash"]):
            return False, "Password lama salah!"
        
        # 3. Validasi password baru
        if not password_baru or len(password_baru) < 6:
            return False, "Password baru harus minimal 6 karakter!"
        
        # 4. Hash password baru
        password_hash_baru = hash_password(password_baru)
        
        # 5. Update di database
        from bson import ObjectId
        queries.db.users.update_one(
            {"_id": ObjectId(id_pengguna)},
            {"$set": {"password_hash": password_hash_baru}}
        )
        
        logger.info(f"Password changed: {id_pengguna}")
        
        return True, "Password berhasil diubah!"
        
    except Exception as e:
        logger.error(f"Error ubah password: {str(e)}")
        return False, f"Error ubah password: {str(e)}"
