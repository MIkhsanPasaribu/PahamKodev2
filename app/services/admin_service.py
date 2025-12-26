"""
Admin Service - Business Logic untuk Admin Operations

CATATAN:
- User management (suspend, activate, view all mahasiswa)
- Analytics & monitoring (global patterns, top errors, AI usage)
- Content management (resources, topics, exercises)
- System health monitoring
"""

import logging
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta

from database.queries import DatabaseQueries
from database.models import SumberDaya, TopikPembelajaran, Exercise

logger = logging.getLogger(__name__)


# ==================== USER MANAGEMENT ====================

def ambil_daftar_mahasiswa(
    queries: DatabaseQueries,
    page: int = 0,
    per_page: int = 50,
    filter_status: Optional[str] = None,
    filter_tingkat: Optional[str] = None,
    search_query: Optional[str] = None
) -> Tuple[List[Dict[str, Any]], int]:
    """
    Ambil daftar mahasiswa dengan pagination, filter, dan search
    
    Args:
        queries: DatabaseQueries instance
        page: Current page number (0-indexed)
        per_page: Items per page
        filter_status: Filter by status (aktif, suspended, nonaktif)
        filter_tingkat: Filter by tingkat_kemahiran
        search_query: Search by nama or email
    
    Returns:
        Tuple of (list_mahasiswa, total_count)
    """
    try:
        skip = page * per_page
        
        mahasiswa_list = queries.daftar_semua_mahasiswa(
            skip=skip,
            limit=per_page,
            filter_status=filter_status,
            filter_tingkat=filter_tingkat,
            search_query=search_query
        )
        
        total_count = queries.hitung_total_mahasiswa()
        
        # Enhance dengan statistik tambahan untuk setiap mahasiswa
        enhanced_list = []
        for mhs in mahasiswa_list:
            id_mhs = str(mhs["_id"])
            
            # Get statistik error
            total_submisi = queries.hitung_total_submisi(id_mhs)
            pola_count = len(queries.ambil_pola_mahasiswa(id_mhs))
            rata_penguasaan = queries.hitung_rata_rata_penguasaan(id_mhs)
            
            enhanced_list.append({
                **mhs,
                "total_submisi": total_submisi,
                "pola_count": pola_count,
                "rata_penguasaan": rata_penguasaan
            })
        
        return enhanced_list, total_count
        
    except Exception as e:
        logger.error(f"Error ambil daftar mahasiswa: {str(e)}")
        return [], 0


def suspend_mahasiswa(
    queries: DatabaseQueries,
    id_mahasiswa: str,
    alasan: Optional[str] = None
) -> Tuple[bool, str]:
    """
    Suspend mahasiswa account
    
    Args:
        queries: DatabaseQueries instance
        id_mahasiswa: Student ID to suspend
        alasan: Reason for suspension (optional, for logging)
    
    Returns:
        Tuple of (success: bool, message: str)
    """
    try:
        success = queries.update_status_pengguna(id_mahasiswa, "suspended")
        
        if success:
            logger.warning(f"Mahasiswa suspended: {id_mahasiswa}. Alasan: {alasan or 'N/A'}")
            return True, "Mahasiswa berhasil ditangguhkan."
        else:
            return False, "Gagal suspend mahasiswa."
        
    except Exception as e:
        logger.error(f"Error suspend mahasiswa: {str(e)}")
        return False, f"Error: {str(e)}"


def aktifkan_mahasiswa(
    queries: DatabaseQueries,
    id_mahasiswa: str
) -> Tuple[bool, str]:
    """
    Aktifkan kembali mahasiswa account
    
    Args:
        queries: DatabaseQueries instance
        id_mahasiswa: Student ID to activate
    
    Returns:
        Tuple of (success: bool, message: str)
    """
    try:
        success = queries.update_status_pengguna(id_mahasiswa, "aktif")
        
        if success:
            logger.info(f"Mahasiswa activated: {id_mahasiswa}")
            return True, "Mahasiswa berhasil diaktifkan kembali."
        else:
            return False, "Gagal aktifkan mahasiswa."
        
    except Exception as e:
        logger.error(f"Error aktifkan mahasiswa: {str(e)}")
        return False, f"Error: {str(e)}"


# ==================== ANALYTICS & MONITORING ====================

def ambil_dashboard_statistik(queries: DatabaseQueries) -> Dict[str, Any]:
    """
    Ambil statistik lengkap untuk Admin Dashboard
    
    Returns:
        Dictionary dengan berbagai metrik untuk dashboard
    """
    try:
        # 1. User statistics
        total_mahasiswa = queries.hitung_total_mahasiswa()
        
        # 2. Error statistics
        total_submisi = queries.hitung_total_submisi()
        
        # 3. Growth (last 30 days)
        pertumbuhan = queries.pertumbuhan_mahasiswa(days=30)
        
        # 4. Top errors
        top_errors = queries.top_errors_global(limit=10)
        
        # 5. Global patterns
        pola_global = queries.ambil_pola_global(limit=10)
        
        # 6. Mahasiswa dengan kesulitan terbanyak
        mahasiswa_kesulitan = queries.mahasiswa_dengan_kesulitan_terbanyak(limit=5)
        
        # 7. Topik paling sulit
        topik_sulit = queries.topik_paling_sulit(limit=10)
        
        # 8. AI metrics (last 7 days)
        start_date = datetime.now() - timedelta(days=7)
        ai_stats = queries.ambil_statistik_ai(start_date=start_date)
        
        # 9. API metrics (last 7 days)
        api_stats = queries.ambil_statistik_api(start_date=start_date)
        
        return {
            "total_mahasiswa": total_mahasiswa,
            "total_submisi": total_submisi,
            "pertumbuhan_mahasiswa": pertumbuhan,
            "top_errors": top_errors,
            "pola_global": pola_global,
            "mahasiswa_perlu_bantuan": mahasiswa_kesulitan,
            "topik_sulit": topik_sulit,
            "ai_metrics": ai_stats,
            "api_metrics": api_stats,
            "timestamp": datetime.now()
        }
        
    except Exception as e:
        logger.error(f"Error ambil dashboard stats: {str(e)}")
        return {}


def ambil_analitik_global(
    queries: DatabaseQueries,
    periode: str = "7d"
) -> Dict[str, Any]:
    """
    Ambil analitik global dengan berbagai metrik
    
    Args:
        queries: DatabaseQueries instance
        periode: Time period ("7d", "30d", "90d", "all")
    
    Returns:
        Dictionary dengan detailed analytics
    """
    try:
        # Parse periode
        days_map = {
            "7d": 7,
            "30d": 30,
            "90d": 90,
            "all": None
        }
        days = days_map.get(periode)
        start_date = datetime.now() - timedelta(days=days) if days else None
        
        # 1. Top errors with details
        top_errors = queries.top_errors_global(limit=20)
        
        # 2. Global patterns dengan insights
        pola_global = queries.ambil_pola_global(limit=20)
        
        # 3. Topik difficulty ranking
        topik_ranking = queries.topik_paling_sulit(limit=20)
        
        # 4. Mahasiswa performance distribution
        # (implementation depends on business requirements)
        
        # 5. AI usage trends
        ai_stats = queries.ambil_statistik_ai(start_date=start_date)
        
        return {
            "periode": periode,
            "top_errors": top_errors,
            "pola_global": pola_global,
            "topik_ranking": topik_ranking,
            "ai_usage": ai_stats,
            "generated_at": datetime.now()
        }
        
    except Exception as e:
        logger.error(f"Error ambil analitik global: {str(e)}")
        return {}


def ambil_pola_insights(queries: DatabaseQueries) -> Dict[str, Any]:
    """
    Ambil insights mendalam tentang pola error global
    
    Returns:
        Dictionary dengan pattern insights dan rekomendasi
    """
    try:
        # 1. Get global patterns
        pola_global = queries.ambil_pola_global(limit=20)
        
        # 2. Analyze patterns untuk insights
        insights = []
        
        for pola in pola_global:
            jenis = pola.get("jenis_kesalahan", "Unknown")
            total_freq = pola.get("total_frekuensi", 0)
            jumlah_mhs = pola.get("jumlah_mahasiswa", 0)
            
            # Calculate severity
            avg_freq_per_student = total_freq / jumlah_mhs if jumlah_mhs > 0 else 0
            
            severity = "Rendah"
            if avg_freq_per_student >= 5:
                severity = "Tinggi"
            elif avg_freq_per_student >= 3:
                severity = "Sedang"
            
            # Recommendations based on severity
            rekomendasi = []
            if severity == "Tinggi":
                rekomendasi.append("Buat tutorial khusus untuk topik ini")
                rekomendasi.append("Tambahkan lebih banyak contoh di materi")
                rekomendasi.append("Pertimbangkan session review untuk mahasiswa")
            elif severity == "Sedang":
                rekomendasi.append("Tambahkan practice exercises untuk topik ini")
                rekomendasi.append("Tingkatkan kejelasan penjelasan konsep")
            
            insights.append({
                "jenis_kesalahan": jenis,
                "total_frekuensi": total_freq,
                "jumlah_mahasiswa_terdampak": jumlah_mhs,
                "rata_rata_per_mahasiswa": round(avg_freq_per_student, 2),
                "severity": severity,
                "rekomendasi": rekomendasi,
                "deskripsi_sample": pola.get("deskripsi_sample")
            })
        
        return {
            "insights": insights,
            "total_patterns": len(insights),
            "generated_at": datetime.now()
        }
        
    except Exception as e:
        logger.error(f"Error ambil pola insights: {str(e)}")
        return {}


# ==================== CONTENT MANAGEMENT ====================

def kelola_sumber_daya(
    queries: DatabaseQueries,
    action: str,
    id_admin: str,
    data: Optional[Dict[str, Any]] = None,
    id_sumber: Optional[str] = None
) -> Tuple[bool, str]:
    """
    CRUD operations untuk learning resources
    
    Args:
        queries: DatabaseQueries instance
        action: "create", "update", "delete", "list"
        id_admin: Admin ID (for audit trail)
        data: Resource data (for create/update)
        id_sumber: Resource ID (for update/delete)
    
    Returns:
        Tuple of (success: bool, message: str)
    """
    try:
        if action == "create":
            if not data:
                return False, "Data sumber daya tidak boleh kosong!"
            
            # Create SumberDaya object
            from bson import ObjectId
            
            sumber = SumberDaya(
                judul=data["judul"],
                deskripsi=data.get("deskripsi"),
                tipe=data.get("tipe", "artikel"),
                url=data.get("url"),
                konten=data.get("konten"),
                topik_terkait=data.get("topik_terkait", []),
                tingkat_kesulitan=data.get("tingkat_kesulitan", "pemula"),
                durasi=data.get("durasi"),
                dibuat_oleh=ObjectId(id_admin),
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            
            id_baru = queries.buat_sumber_daya(sumber.to_dict())
            logger.info(f"Sumber daya baru: {id_baru}")
            
            return True, f"Sumber daya berhasil dibuat! (ID: {id_baru})"
        
        elif action == "update":
            if not id_sumber or not data:
                return False, "ID dan data harus disediakan!"
            
            success = queries.update_sumber_daya(id_sumber, data)
            
            if success:
                logger.info(f"Sumber daya updated: {id_sumber}")
                return True, "Sumber daya berhasil diperbarui!"
            else:
                return False, "Gagal update sumber daya."
        
        elif action == "delete":
            if not id_sumber:
                return False, "ID sumber daya harus disediakan!"
            
            success = queries.hapus_sumber_daya(id_sumber)
            
            if success:
                logger.info(f"Sumber daya deleted: {id_sumber}")
                return True, "Sumber daya berhasil dihapus!"
            else:
                return False, "Gagal hapus sumber daya."
        
        else:
            return False, f"Action tidak dikenal: {action}"
        
    except Exception as e:
        logger.error(f"Error kelola sumber daya: {str(e)}")
        return False, f"Error: {str(e)}"


def kelola_topik(
    queries: DatabaseQueries,
    action: str,
    data: Optional[Dict[str, Any]] = None,
    id_topik: Optional[str] = None
) -> Tuple[bool, str]:
    """
    CRUD operations untuk topik pembelajaran
    
    Args:
        queries: DatabaseQueries instance
        action: "create", "update", "delete", "list"
        data: Topic data (for create/update)
        id_topik: Topic ID (for update/delete)
    
    Returns:
        Tuple of (success: bool, message: str)
    """
    try:
        if action == "create":
            if not data:
                return False, "Data topik tidak boleh kosong!"
            
            topik = TopikPembelajaran(
                nama=data["nama"],
                deskripsi=data.get("deskripsi"),
                kategori=data.get("kategori", "dasar"),
                tingkat_kesulitan=data.get("tingkat_kesulitan", "pemula"),
                prerequisite=data.get("prerequisite", []),
                tujuan_pembelajaran=data.get("tujuan_pembelajaran", []),
                estimasi_waktu=data.get("estimasi_waktu"),
                total_error=0,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            
            id_baru = queries.buat_topik(topik.to_dict())
            logger.info(f"Topik baru: {id_baru}")
            
            return True, f"Topik berhasil dibuat! (ID: {id_baru})"
        
        elif action == "update":
            if not id_topik or not data:
                return False, "ID dan data harus disediakan!"
            
            success = queries.update_topik(id_topik, data)
            
            if success:
                logger.info(f"Topik updated: {id_topik}")
                return True, "Topik berhasil diperbarui!"
            else:
                return False, "Gagal update topik."
        
        elif action == "delete":
            if not id_topik:
                return False, "ID topik harus disediakan!"
            
            success = queries.hapus_topik(id_topik)
            
            if success:
                logger.info(f"Topik deleted: {id_topik}")
                return True, "Topik berhasil dihapus!"
            else:
                return False, "Gagal hapus topik."
        
        else:
            return False, f"Action tidak dikenal: {action}"
        
    except Exception as e:
        logger.error(f"Error kelola topik: {str(e)}")
        return False, f"Error: {str(e)}"


def kelola_exercise(
    queries: DatabaseQueries,
    action: str,
    id_admin: str,
    data: Optional[Dict[str, Any]] = None,
    id_exercise: Optional[str] = None
) -> Tuple[bool, str]:
    """
    CRUD operations untuk exercises
    
    Args:
        queries: DatabaseQueries instance
        action: "create", "update", "delete", "list"
        id_admin: Admin ID (for audit trail)
        data: Exercise data (for create/update)
        id_exercise: Exercise ID (for update/delete)
    
    Returns:
        Tuple of (success: bool, message: str)
    """
    try:
        if action == "create":
            if not data:
                return False, "Data exercise tidak boleh kosong!"
            
            from bson import ObjectId
            
            exercise = Exercise(
                judul=data["judul"],
                deskripsi=data["deskripsi"],
                topik=data["topik"],
                tingkat_kesulitan=data.get("tingkat_kesulitan", "pemula"),
                instruksi=data.get("instruksi", ""),
                kode_pemula=data.get("kode_pemula"),
                solusi_referensi=data.get("solusi_referensi", ""),
                test_cases=data.get("test_cases", []),
                poin_belajar=data.get("poin_belajar", []),
                estimasi_waktu=data.get("estimasi_waktu"),
                dibuat_oleh=ObjectId(id_admin),
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            
            id_baru = queries.buat_exercise(exercise.to_dict())
            logger.info(f"Exercise baru: {id_baru}")
            
            return True, f"Exercise berhasil dibuat! (ID: {id_baru})"
        
        elif action == "update":
            if not id_exercise or not data:
                return False, "ID dan data harus disediakan!"
            
            success = queries.update_exercise(id_exercise, data)
            
            if success:
                logger.info(f"Exercise updated: {id_exercise}")
                return True, "Exercise berhasil diperbarui!"
            else:
                return False, "Gagal update exercise."
        
        elif action == "delete":
            if not id_exercise:
                return False, "ID exercise harus disediakan!"
            
            success = queries.hapus_exercise(id_exercise)
            
            if success:
                logger.info(f"Exercise deleted: {id_exercise}")
                return True, "Exercise berhasil dihapus!"
            else:
                return False, "Gagal hapus exercise."
        
        else:
            return False, f"Action tidak dikenal: {action}"
        
    except Exception as e:
        logger.error(f"Error kelola exercise: {str(e)}")
        return False, f"Error: {str(e)}"


# ==================== SYSTEM MONITORING ====================

def ambil_system_health(queries: DatabaseQueries) -> Dict[str, Any]:
    """
    Check system health untuk monitoring dashboard
    
    Returns:
        Dictionary dengan berbagai health metrics
    """
    try:
        # 1. Database connection test
        try:
            queries.db.command("ping")
            db_status = "Healthy"
        except:
            db_status = "Error"
        
        # 2. AI metrics (last 24h)
        start_date = datetime.now() - timedelta(hours=24)
        ai_stats = queries.ambil_statistik_ai(start_date=start_date)
        
        ai_health = "Healthy"
        if ai_stats.get("success_rate", 0) < 90:
            ai_health = "Warning"
        if ai_stats.get("success_rate", 0) < 70:
            ai_health = "Critical"
        
        # 3. API metrics (last 24h)
        api_stats = queries.ambil_statistik_api(start_date=start_date)
        
        api_health = "Healthy"
        if api_stats.get("success_rate", 0) < 95:
            api_health = "Warning"
        if api_stats.get("success_rate", 0) < 85:
            api_health = "Critical"
        
        # 4. Overall health
        overall_health = "Healthy"
        if db_status != "Healthy" or ai_health == "Critical" or api_health == "Critical":
            overall_health = "Critical"
        elif ai_health == "Warning" or api_health == "Warning":
            overall_health = "Warning"
        
        return {
            "overall_health": overall_health,
            "database": {
                "status": db_status
            },
            "ai_service": {
                "status": ai_health,
                "metrics": ai_stats
            },
            "api_service": {
                "status": api_health,
                "metrics": api_stats
            },
            "checked_at": datetime.now()
        }
        
    except Exception as e:
        logger.error(f"Error check system health: {str(e)}")
        return {
            "overall_health": "Error",
            "error": str(e)
        }


# ==================== CONTENT MANAGEMENT CRUD ====================

def ambil_semua_sumber_daya(queries: DatabaseQueries) -> List[Dict[str, Any]]:
    """
    Ambil semua sumber daya pembelajaran
    
    Returns:
        List of sumber daya documents
    """
    try:
        return queries.ambil_semua_sumber_daya()
    except Exception as e:
        logger.error(f"Error ambil semua sumber daya: {str(e)}")
        return []


def tambah_sumber_daya(queries: DatabaseQueries, data: Dict[str, Any]) -> Optional[str]:
    """
    Tambah sumber daya baru
    
    Args:
        queries: DatabaseQueries instance
        data: Sumber daya data (judul, deskripsi, url, kategori, tags)
    
    Returns:
        Inserted ID as string, or None if failed
    """
    try:
        result = queries.tambah_sumber_daya(data)
        return str(result) if result else None
    except Exception as e:
        logger.error(f"Error tambah sumber daya: {str(e)}")
        return None


def update_sumber_daya(queries: DatabaseQueries, id_sumber: str, data: Dict[str, Any]) -> bool:
    """
    Update sumber daya
    
    Args:
        queries: DatabaseQueries instance
        id_sumber: ID sumber daya
        data: Updated data
    
    Returns:
        True if success, False otherwise
    """
    try:
        return queries.update_sumber_daya(id_sumber, data)
    except Exception as e:
        logger.error(f"Error update sumber daya: {str(e)}")
        return False


def hapus_sumber_daya(queries: DatabaseQueries, id_sumber: str) -> bool:
    """
    Hapus sumber daya
    
    Args:
        queries: DatabaseQueries instance
        id_sumber: ID sumber daya
    
    Returns:
        True if success, False otherwise
    """
    try:
        return queries.hapus_sumber_daya(id_sumber)
    except Exception as e:
        logger.error(f"Error hapus sumber daya: {str(e)}")
        return False


def ambil_semua_topik(queries: DatabaseQueries) -> List[Dict[str, Any]]:
    """
    Ambil semua topik pembelajaran
    
    Returns:
        List of topik documents
    """
    try:
        return queries.ambil_semua_topik()
    except Exception as e:
        logger.error(f"Error ambil semua topik: {str(e)}")
        return []


def tambah_topik(queries: DatabaseQueries, data: Dict[str, Any]) -> Optional[str]:
    """
    Tambah topik baru
    
    Args:
        queries: DatabaseQueries instance
        data: Topik data (nama, deskripsi, kategori, difficulty, prerequisites)
    
    Returns:
        Inserted ID as string, or None if failed
    """
    try:
        result = queries.tambah_topik(data)
        return str(result) if result else None
    except Exception as e:
        logger.error(f"Error tambah topik: {str(e)}")
        return None


def update_topik(queries: DatabaseQueries, id_topik: str, data: Dict[str, Any]) -> bool:
    """
    Update topik
    
    Args:
        queries: DatabaseQueries instance
        id_topik: ID topik
        data: Updated data
    
    Returns:
        True if success, False otherwise
    """
    try:
        return queries.update_topik(id_topik, data)
    except Exception as e:
        logger.error(f"Error update topik: {str(e)}")
        return False


def hapus_topik(queries: DatabaseQueries, id_topik: str) -> bool:
    """
    Hapus topik
    
    Args:
        queries: DatabaseQueries instance
        id_topik: ID topik
    
    Returns:
        True if success, False otherwise
    """
    try:
        return queries.hapus_topik(id_topik)
    except Exception as e:
        logger.error(f"Error hapus topik: {str(e)}")
        return False


def ambil_semua_exercises(queries: DatabaseQueries) -> List[Dict[str, Any]]:
    """
    Ambil semua exercises
    
    Returns:
        List of exercise documents
    """
    try:
        return queries.ambil_semua_exercises()
    except Exception as e:
        logger.error(f"Error ambil semua exercises: {str(e)}")
        return []


def tambah_exercise(queries: DatabaseQueries, data: Dict[str, Any]) -> Optional[str]:
    """
    Tambah exercise baru
    
    Args:
        queries: DatabaseQueries instance
        data: Exercise data (judul, deskripsi, soal, jawaban_contoh, difficulty, topik_terkait)
    
    Returns:
        Inserted ID as string, or None if failed
    """
    try:
        result = queries.tambah_exercise(data)
        return str(result) if result else None
    except Exception as e:
        logger.error(f"Error tambah exercise: {str(e)}")
        return None


def update_exercise(queries: DatabaseQueries, id_exercise: str, data: Dict[str, Any]) -> bool:
    """
    Update exercise
    
    Args:
        queries: DatabaseQueries instance
        id_exercise: ID exercise
        data: Updated data
    
    Returns:
        True if success, False otherwise
    """
    try:
        return queries.update_exercise(id_exercise, data)
    except Exception as e:
        logger.error(f"Error update exercise: {str(e)}")
        return False


def hapus_exercise(queries: DatabaseQueries, id_exercise: str) -> bool:
    """
    Hapus exercise
    
    Args:
        queries: DatabaseQueries instance
        id_exercise: ID exercise
    
    Returns:
        True if success, False otherwise
    """
    try:
        return queries.hapus_exercise(id_exercise)
    except Exception as e:
        logger.error(f"Error hapus exercise: {str(e)}")
        return False


def ambil_detail_mahasiswa(queries: DatabaseQueries, id_mahasiswa: str) -> Optional[Dict[str, Any]]:
    """
    Ambil detail lengkap mahasiswa (profile + statistik)
    
    Args:
        queries: DatabaseQueries instance
        id_mahasiswa: ID mahasiswa
    
    Returns:
        Dict dengan data mahasiswa lengkap, atau None jika tidak ditemukan
    """
    try:
        # Ambil data mahasiswa
        mahasiswa = queries.cari_pengguna_by_id(id_mahasiswa)
        if not mahasiswa:
            return None
        
        # Ambil statistik submission
        riwayat = queries.ambil_riwayat_submisi(id_mahasiswa, limit=1000)
        pola = queries.ambil_pola_mahasiswa(id_mahasiswa)
        progress = queries.ambil_progress_mahasiswa(id_mahasiswa)
        
        # Hitung stats
        total_submisi = len(riwayat)
        total_pola = len(pola)
        avg_penguasaan = sum(p.get("tingkat_penguasaan", 0) for p in progress) / len(progress) if progress else 0
        
        # Error breakdown
        error_counts: Dict[str, int] = {}
        for r in riwayat:
            tipe = r.get("tipe_error", "Unknown")
            error_counts[tipe] = error_counts.get(tipe, 0) + 1
        
        return {
            "profile": mahasiswa,
            "statistik": {
                "total_submisi": total_submisi,
                "total_pola": total_pola,
                "avg_penguasaan": avg_penguasaan,
                "topik_dipelajari": len(progress),
                "error_breakdown": error_counts
            },
            "riwayat_terbaru": riwayat[:10],
            "pola_terbanyak": pola[:5],
            "progress": progress
        }
        
    except Exception as e:
        logger.error(f"Error ambil detail mahasiswa: {str(e)}")
        return None

