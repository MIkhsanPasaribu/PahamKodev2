"""
Analisis Service - Main Business Logic untuk Error Analysis
Menggabungkan AI analysis dengan database operations

CATATAN:
- Orchestrates AI service dengan database queries
- Pattern detection (≥3 errors of same type)
- Progress tracking otomatis
- Metrics logging untuk admin monitoring
"""

import logging
from typing import Optional, Dict, Any, Tuple
from datetime import datetime
from bson import ObjectId

from services.ai_service import (
    analisis_error_semantik,
    HasilAnalisis,
    hitung_token_estimasi,
    hitung_biaya_estimasi
)
from database.queries import DatabaseQueries
from database.models import SubmisiError, MetrikAI

logger = logging.getLogger(__name__)


# ==================== MAIN ANALYSIS FUNCTION ====================

def proses_analisis_error(
    queries: DatabaseQueries,
    id_mahasiswa: str,
    kode: str,
    pesan_error: str,
    bahasa: str = "python"
) -> Tuple[Optional[SubmisiError], Optional[str]]:
    """
    Proses analisis error secara lengkap (SYNCHRONOUS untuk Streamlit):
    1. Get student context dari database
    2. Call AI untuk semantic analysis
    3. Save hasil analisis ke database
    4. Check for patterns (≥3 occurrences)
    5. Update progress tracking
    6. Log AI metrics
    
    Args:
        queries: DatabaseQueries instance
        id_mahasiswa: Student ID
        kode: Source code dengan error
        pesan_error: Error message
        bahasa: Programming language
    
    Returns:
        Tuple of (SubmisiError object, pattern_alert string if applicable)
    """
    try:
        start_time = datetime.now()
        
        # 1. Get student context
        mahasiswa = queries.cari_pengguna_by_id(id_mahasiswa)
        if not mahasiswa:
            logger.error(f"Mahasiswa tidak ditemukan: {id_mahasiswa}")
            return None, None
        
        tingkat_kemahiran = mahasiswa.get("tingkat_kemahiran", "pemula")
        
        # 2. Get recent error history untuk konteks AI
        riwayat_error = queries.ambil_submisi_terakhir(id_mahasiswa, jumlah=5)
        
        # 3. Call AI untuk semantic analysis (synchronous)
        logger.info(f"Starting semantic analysis untuk mahasiswa: {id_mahasiswa}")
        
        hasil_ai: Optional[HasilAnalisis] = analisis_error_semantik(
            kode=kode,
            pesan_error=pesan_error,
            bahasa=bahasa,
            tingkat_kemahiran=tingkat_kemahiran,
            riwayat_error=riwayat_error
        )
        
        if not hasil_ai:
            logger.error("AI analysis gagal")
            return None, None
        
        # 4. Create SubmisiError object
        submisi = SubmisiError(
            id_mahasiswa=ObjectId(id_mahasiswa),
            kode=kode,
            pesan_error=pesan_error,
            bahasa=bahasa,
            tipe_error=hasil_ai.tipe_error,
            penyebab_utama=hasil_ai.penyebab_utama,
            kesenjangan_konsep=hasil_ai.kesenjangan_konsep,
            level_bloom=hasil_ai.level_bloom,
            penjelasan=hasil_ai.penjelasan,
            saran_perbaikan=hasil_ai.saran_perbaikan,
            topik_terkait=hasil_ai.topik_terkait,
            saran_latihan=hasil_ai.saran_latihan,
            created_at=datetime.now()
        )
        
        # 5. Save ke database
        id_submisi = queries.simpan_submisi_error(submisi.to_dict())
        submisi._id = id_submisi
        
        logger.info(f"Submisi error saved: {id_submisi}")
        
        # 6. Check for pattern (≥3 errors of same type)
        pattern_alert: Optional[str] = None
        frekuensi_error = queries.hitung_submisi_by_tipe(id_mahasiswa, hasil_ai.tipe_error)
        
        if frekuensi_error >= 3:
            logger.warning(f"Pattern detected: {hasil_ai.tipe_error} (frekuensi: {frekuensi_error})")
            
            # Create/update pattern record
            queries.buat_atau_update_pola(
                id_mahasiswa=id_mahasiswa,
                jenis_kesalahan=hasil_ai.tipe_error,
                deskripsi_miskonsepsi=hasil_ai.kesenjangan_konsep,
                sumber_daya=hasil_ai.topik_terkait
            )
            
            pattern_alert = (
                f"⚠️ **Pola Error Terdeteksi!**\n\n"
                f"Kamu sudah mengalami error **'{hasil_ai.tipe_error}'** sebanyak **{frekuensi_error} kali**.\n\n"
                f"**Rekomendasi:** Fokus pelajari topik berikut:\n"
                f"{', '.join(hasil_ai.topik_terkait[:3])}\n\n"
                f"Lihat halaman **Pola Error** untuk detail lengkap."
            )
        
        # 7. Update progress tracking untuk topik terkait
        for topik in hasil_ai.topik_terkait:
            queries.buat_atau_update_progress(
                id_mahasiswa=id_mahasiswa,
                topik=topik
            )
            
            # Increment error count di topik pembelajaran
            queries.increment_error_count_topik(topik)
        
        # 8. Log AI metrics untuk admin monitoring
        end_time = datetime.now()
        waktu_respons = (end_time - start_time).total_seconds()
        
        # Estimate tokens (rough estimation)
        token_input = hitung_token_estimasi(kode + pesan_error)
        token_output = hitung_token_estimasi(hasil_ai.penjelasan + hasil_ai.saran_perbaikan)
        total_token = token_input + token_output
        biaya = hitung_biaya_estimasi(token_input, token_output)
        
        metrik = MetrikAI(
            id_submisi=id_submisi,
            model="gpt-4o-mini",  # atau model yang dipakai
            token_input=token_input,
            token_output=token_output,
            total_token=total_token,
            biaya=biaya,
            waktu_respons=waktu_respons,
            status_berhasil=True,
            created_at=datetime.now()
        )
        
        queries.simpan_metrik_ai(metrik.to_dict())
        
        logger.info(
            f"Analysis completed: {waktu_respons:.2f}s, "
            f"{total_token} tokens, ${biaya:.4f}"
        )
        
        return submisi, pattern_alert
        
    except Exception as e:
        logger.error(f"Error dalam proses analisis: {str(e)}", exc_info=True)
        
        # Log failed AI metrics
        try:
            metrik_gagal = MetrikAI(
                model="gpt-4o-mini",
                token_input=0,
                token_output=0,
                total_token=0,
                biaya=0.0,
                waktu_respons=0.0,
                status_berhasil=False,
                error_message=str(e),
                created_at=datetime.now()
            )
            queries.simpan_metrik_ai(metrik_gagal.to_dict())
        except:
            pass
        
        return None, None


# ==================== HELPER FUNCTIONS ====================

def format_hasil_analisis(submisi: SubmisiError, pattern_alert: Optional[str] = None) -> Dict[str, Any]:
    """
    Format hasil analisis untuk ditampilkan di UI
    
    Returns:
        Dictionary dengan format yang siap ditampilkan
    """
    return {
        "tipe_error": submisi.tipe_error,
        "penyebab_utama": submisi.penyebab_utama,
        "kesenjangan_konsep": submisi.kesenjangan_konsep,
        "level_bloom": submisi.level_bloom,
        "penjelasan": submisi.penjelasan,
        "saran_perbaikan": submisi.saran_perbaikan,
        "topik_terkait": submisi.topik_terkait,
        "saran_latihan": submisi.saran_latihan,
        "pattern_alert": pattern_alert,
        "created_at": submisi.created_at
    }


def ambil_rekomendasi_belajar(
    queries: DatabaseQueries,
    id_mahasiswa: str,
    topik: str,
    tingkat_kesulitan: Optional[str] = None
) -> Dict[str, Any]:
    """
    Ambil rekomendasi learning resources berdasarkan topik error
    
    Returns:
        Dictionary dengan videos, articles, exercises, quizzes
    """
    try:
        # Get all resources for topik
        semua_resources = queries.ambil_sumber_daya_by_topik(
            topik=topik,
            tingkat=tingkat_kesulitan
        )
        
        # Group by type
        rekomendasi = {
            "video": [],
            "artikel": [],
            "tutorial": [],
            "exercise": [],
            "quiz": []
        }
        
        for resource in semua_resources:
            tipe = resource.get("tipe", "artikel")
            if tipe in rekomendasi:
                rekomendasi[tipe].append({
                    "id": str(resource["_id"]),
                    "judul": resource["judul"],
                    "deskripsi": resource.get("deskripsi"),
                    "url": resource.get("url"),
                    "durasi": resource.get("durasi")
                })
        
        return rekomendasi
        
    except Exception as e:
        logger.error(f"Error ambil rekomendasi: {str(e)}")
        return {}


def hitung_statistik_mahasiswa(
    queries: DatabaseQueries,
    id_mahasiswa: str
) -> Dict[str, Any]:
    """
    Hitung statistik analisis untuk dashboard mahasiswa
    
    Returns:
        Dictionary dengan total_submisi, top_errors, avg_penguasaan, dll
    """
    try:
        # Total submisi
        total_submisi = queries.hitung_total_submisi(id_mahasiswa)
        
        # Ambil pola error (top 5)
        pola_errors = queries.ambil_pola_mahasiswa(id_mahasiswa)[:5]
        
        # Progress learning
        progress_data = queries.ambil_progress_mahasiswa(id_mahasiswa)
        
        # Rata-rata penguasaan
        rata_rata_penguasaan = queries.hitung_rata_rata_penguasaan(id_mahasiswa)
        
        # Recent activity (5 terakhir)
        recent_activity = queries.ambil_riwayat_submisi(id_mahasiswa, limit=5)
        
        return {
            "total_submisi": total_submisi,
            "pola_errors": [
                {
                    "jenis": p["jenis_kesalahan"],
                    "frekuensi": p["frekuensi"]
                }
                for p in pola_errors
            ],
            "progress_topik": [
                {
                    "topik": prog.get("topik", "Unknown"),
                    "penguasaan": prog.get("tingkat_penguasaan", 0),
                    "jumlah_error": prog.get("jumlah_error_di_topik", 0)
                }
                for prog in progress_data
            ],
            "rata_rata_penguasaan": rata_rata_penguasaan,
            "recent_activity": [
                {
                    "tipe_error": act["tipe_error"],
                    "created_at": act["created_at"]
                }
                for act in recent_activity
            ]
        }
        
    except Exception as e:
        logger.error(f"Error hitung statistik: {str(e)}")
        return {}
