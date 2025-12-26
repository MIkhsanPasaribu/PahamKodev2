"""
Database Queries - CRUD Operations untuk semua Collections
Menggunakan PyMongo native untuk operasi database

CATATAN: 
- Semua method async untuk best practice dengan Streamlit
- Error handling terintegrasi
- Logging untuk monitoring
"""

from pymongo.database import Database
from pymongo.collection import Collection
from typing import Dict, List, Optional, Any
from bson import ObjectId
from datetime import datetime, timedelta
import logging

from app.database.models import (
    Pengguna, SubmisiError, PolaError, ProgressBelajar,
    MetrikAI, SumberDaya, TopikPembelajaran, Exercise, MetrikAPI
)

logger = logging.getLogger(__name__)


class DatabaseQueries:
    """Database operations untuk semua collections"""
    
    def __init__(self, db: Database):
        self.db = db
        self.users: Collection = db.users
        self.submisi_error: Collection = db.submisi_error
        self.pola_error: Collection = db.pola_error
        self.progress_belajar: Collection = db.progress_belajar
        self.metrik_ai: Collection = db.metrik_ai
        self.sumber_daya: Collection = db.sumber_daya
        self.topik_pembelajaran: Collection = db.topik_pembelajaran
        self.exercises: Collection = db.exercises
        self.metrik_api: Collection = db.metrik_api
    
    
    # ==================== USER OPERATIONS ====================
    
    def buat_pengguna(self, data_pengguna: Dict[str, Any]) -> ObjectId:
        """Buat user baru (mahasiswa/admin)"""
        try:
            result = self.users.insert_one(data_pengguna)
            logger.info(f"User baru dibuat: {data_pengguna.get('email')}")
            return result.inserted_id
        except Exception as e:
            logger.error(f"Error buat pengguna: {str(e)}")
            raise
    
    def cari_pengguna_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Cari user berdasarkan email"""
        try:
            return self.users.find_one({"email": email})
        except Exception as e:
            logger.error(f"Error cari pengguna by email: {str(e)}")
            return None
    
    def cari_pengguna_by_id(self, id_pengguna: str) -> Optional[Dict[str, Any]]:
        """Cari user berdasarkan ID"""
        try:
            return self.users.find_one({"_id": ObjectId(id_pengguna)})
        except Exception as e:
            logger.error(f"Error cari pengguna by ID: {str(e)}")
            return None
    
    def update_status_pengguna(self, id_pengguna: str, status: str) -> bool:
        """Update status user (aktif/suspended/nonaktif) - Admin function"""
        try:
            result = self.users.update_one(
                {"_id": ObjectId(id_pengguna)},
                {"$set": {"status": status}}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error update status pengguna: {str(e)}")
            return False
    
    def update_last_login(self, id_pengguna: str) -> bool:
        """Update last login timestamp"""
        try:
            result = self.users.update_one(
                {"_id": ObjectId(id_pengguna)},
                {"$set": {"last_login": datetime.now()}}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error update last login: {str(e)}")
            return False
    
    def daftar_semua_mahasiswa(
        self, 
        skip: int = 0, 
        limit: int = 50,
        filter_status: Optional[str] = None,
        filter_tingkat: Optional[str] = None,
        search_query: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Ambil daftar mahasiswa dengan pagination & filter - Admin function"""
        try:
            query: Dict[str, Any] = {"role": "mahasiswa"}
            
            # Filter by status
            if filter_status:
                query["status"] = filter_status
            
            # Filter by tingkat kemahiran
            if filter_tingkat:
                query["tingkat_kemahiran"] = filter_tingkat
            
            # Search by nama or email
            if search_query:
                query["$or"] = [
                    {"nama": {"$regex": search_query, "$options": "i"}},
                    {"email": {"$regex": search_query, "$options": "i"}}
                ]
            
            cursor = self.users.find(query).sort("created_at", -1).skip(skip).limit(limit)
            return list(cursor)
        except Exception as e:
            logger.error(f"Error daftar mahasiswa: {str(e)}")
            return []
    
    def hitung_total_mahasiswa(self) -> int:
        """Hitung total mahasiswa - Admin analytics"""
        try:
            return self.users.count_documents({"role": "mahasiswa"})
        except Exception as e:
            logger.error(f"Error hitung total mahasiswa: {str(e)}")
            return 0
    
    
    # ==================== ERROR SUBMISSION OPERATIONS ====================
    
    def simpan_submisi_error(self, submisi: Dict[str, Any]) -> ObjectId:
        """Simpan submisi error baru"""
        try:
            result = self.submisi_error.insert_one(submisi)
            logger.info(f"Submisi error baru: {result.inserted_id}")
            return result.inserted_id
        except Exception as e:
            logger.error(f"Error simpan submisi: {str(e)}")
            raise
    
    def ambil_riwayat_submisi(
        self, 
        id_mahasiswa: str, 
        limit: int = 20,
        skip: int = 0
    ) -> List[Dict[str, Any]]:
        """Ambil riwayat submisi mahasiswa dengan pagination"""
        try:
            cursor = self.submisi_error.find(
                {"id_mahasiswa": ObjectId(id_mahasiswa)}
            ).sort("created_at", -1).skip(skip).limit(limit)
            return list(cursor)
        except Exception as e:
            logger.error(f"Error ambil riwayat: {str(e)}")
            return []
    
    def hitung_submisi_by_tipe(self, id_mahasiswa: str, tipe_error: str) -> int:
        """Hitung jumlah error dengan tipe tertentu (untuk pattern detection)"""
        try:
            return self.submisi_error.count_documents({
                "id_mahasiswa": ObjectId(id_mahasiswa),
                "tipe_error": tipe_error
            })
        except Exception as e:
            logger.error(f"Error hitung submisi by tipe: {str(e)}")
            return 0
    
    def ambil_submisi_terakhir(self, id_mahasiswa: str, jumlah: int = 5) -> List[Dict[str, Any]]:
        """Ambil N submisi terakhir untuk konteks AI"""
        try:
            cursor = self.submisi_error.find(
                {"id_mahasiswa": ObjectId(id_mahasiswa)}
            ).sort("created_at", -1).limit(jumlah)
            return list(cursor)
        except Exception as e:
            logger.error(f"Error ambil submisi terakhir: {str(e)}")
            return []
    
    def hitung_total_submisi(self, id_mahasiswa: Optional[str] = None) -> int:
        """Hitung total submisi (global atau per mahasiswa)"""
        try:
            query = {"id_mahasiswa": ObjectId(id_mahasiswa)} if id_mahasiswa else {}
            return self.submisi_error.count_documents(query)
        except Exception as e:
            logger.error(f"Error hitung total submisi: {str(e)}")
            return 0
    
    
    # ==================== PATTERN OPERATIONS ====================
    
    def buat_atau_update_pola(
        self,
        id_mahasiswa: str,
        jenis_kesalahan: str,
        deskripsi_miskonsepsi: str,
        sumber_daya: List[str]
    ) -> None:
        """Buat atau update pola error (dipanggil saat pattern detected ≥3x)"""
        try:
            frekuensi = self.hitung_submisi_by_tipe(id_mahasiswa, jenis_kesalahan)
            
            self.pola_error.update_one(
                {
                    "id_mahasiswa": ObjectId(id_mahasiswa),
                    "jenis_kesalahan": jenis_kesalahan
                },
                {
                    "$set": {
                        "frekuensi": frekuensi,
                        "kejadian_terakhir": datetime.now(),
                        "deskripsi_miskonsepsi": deskripsi_miskonsepsi,
                        "sumber_daya_direkomendasikan": sumber_daya,
                        "updated_at": datetime.now()
                    },
                    "$setOnInsert": {
                        "kejadian_pertama": datetime.now(),
                        "created_at": datetime.now()
                    }
                },
                upsert=True
            )
            logger.info(f"Pattern updated: {jenis_kesalahan} (frekuensi: {frekuensi})")
        except Exception as e:
            logger.error(f"Error update pola: {str(e)}")
            raise
    
    def ambil_pola_mahasiswa(self, id_mahasiswa: str) -> List[Dict[str, Any]]:
        """Ambil semua pola error mahasiswa (sorted by frekuensi)"""
        try:
            cursor = self.pola_error.find(
                {"id_mahasiswa": ObjectId(id_mahasiswa)}
            ).sort("frekuensi", -1)
            return list(cursor)
        except Exception as e:
            logger.error(f"Error ambil pola mahasiswa: {str(e)}")
            return []
    
    def ambil_pola_global(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Ambil top error patterns secara global - Admin analytics"""
        try:
            pipeline = [
                {
                    "$group": {
                        "_id": "$jenis_kesalahan",
                        "total_mahasiswa": {"$addToSet": "$id_mahasiswa"},
                        "total_frekuensi": {"$sum": "$frekuensi"},
                        "deskripsi_sample": {"$first": "$deskripsi_miskonsepsi"}
                    }
                },
                {
                    "$project": {
                        "jenis_kesalahan": "$_id",
                        "jumlah_mahasiswa": {"$size": "$total_mahasiswa"},
                        "total_frekuensi": 1,
                        "deskripsi_sample": 1
                    }
                },
                {
                    "$sort": {"total_frekuensi": -1}
                },
                {
                    "$limit": limit
                }
            ]
            
            result = list(self.pola_error.aggregate(pipeline))
            return result
        except Exception as e:
            logger.error(f"Error ambil pola global: {str(e)}")
            return []
    
    
    # ==================== PROGRESS OPERATIONS ====================
    
    def buat_atau_update_progress(
        self,
        id_mahasiswa: str,
        topik: str,
        tingkat_penguasaan: Optional[int] = None
    ) -> None:
        """Update progress belajar mahasiswa untuk topik tertentu"""
        try:
            update_fields: Dict[str, Any] = {
                "updated_at": datetime.now(),
                "tanggal_error_terakhir": datetime.now()
            }
            
            if tingkat_penguasaan is not None:
                update_fields["tingkat_penguasaan"] = tingkat_penguasaan
            
            self.progress_belajar.update_one(
                {
                    "id_mahasiswa": ObjectId(id_mahasiswa),
                    "topik": topik
                },
                {
                    "$set": update_fields,
                    "$inc": {"jumlah_error_di_topik": 1},
                    "$setOnInsert": {
                        "created_at": datetime.now()
                    }
                },
                upsert=True
            )
            logger.info(f"Progress updated untuk topik: {topik}")
        except Exception as e:
            logger.error(f"Error update progress: {str(e)}")
            raise
    
    def ambil_progress_mahasiswa(self, id_mahasiswa: str) -> List[Dict[str, Any]]:
        """Ambil semua progress belajar mahasiswa"""
        try:
            cursor = self.progress_belajar.find(
                {"id_mahasiswa": ObjectId(id_mahasiswa)}
            ).sort("tingkat_penguasaan", -1)
            return list(cursor)
        except Exception as e:
            logger.error(f"Error ambil progress: {str(e)}")
            return []
    
    def hitung_rata_rata_penguasaan(self, id_mahasiswa: str) -> float:
        """Hitung rata-rata tingkat penguasaan mahasiswa"""
        try:
            pipeline = [
                {"$match": {"id_mahasiswa": ObjectId(id_mahasiswa)}},
                {"$group": {
                    "_id": None,
                    "rata_rata": {"$avg": "$tingkat_penguasaan"}
                }}
            ]
            result = list(self.progress_belajar.aggregate(pipeline))
            return result[0]["rata_rata"] if result else 0.0
        except Exception as e:
            logger.error(f"Error hitung rata-rata penguasaan: {str(e)}")
            return 0.0
    
    
    # ==================== AI METRICS OPERATIONS ====================
    
    def simpan_metrik_ai(self, metrik: Dict[str, Any]) -> ObjectId:
        """Simpan metrik AI usage (untuk cost tracking & performance)"""
        try:
            result = self.metrik_ai.insert_one(metrik)
            return result.inserted_id
        except Exception as e:
            logger.error(f"Error simpan metrik AI: {str(e)}")
            raise
    
    def ambil_statistik_ai(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Ambil statistik AI usage - Admin monitoring"""
        try:
            query: Dict[str, Any] = {}
            if start_date or end_date:
                query["created_at"] = {}
                if start_date:
                    query["created_at"]["$gte"] = start_date
                if end_date:
                    query["created_at"]["$lte"] = end_date
            
            pipeline = [
                {"$match": query},
                {
                    "$group": {
                        "_id": None,
                        "total_request": {"$sum": 1},
                        "total_token": {"$sum": "$total_token"},
                        "total_biaya": {"$sum": "$biaya"},
                        "rata_rata_waktu_respons": {"$avg": "$waktu_respons"},
                        "sukses_count": {
                            "$sum": {"$cond": ["$status_berhasil", 1, 0]}
                        }
                    }
                }
            ]
            
            result = list(self.metrik_ai.aggregate(pipeline))
            if result:
                stats = result[0]
                stats["success_rate"] = (stats["sukses_count"] / stats["total_request"] * 100) if stats["total_request"] > 0 else 0
                return stats
            else:
                return {
                    "total_request": 0,
                    "total_token": 0,
                    "total_biaya": 0.0,
                    "rata_rata_waktu_respons": 0.0,
                    "success_rate": 0.0
                }
        except Exception as e:
            logger.error(f"Error ambil statistik AI: {str(e)}")
            return {}
    
    
    # ==================== LEARNING RESOURCES OPERATIONS ====================
    
    def ambil_semua_sumber_daya(self) -> List[Dict[str, Any]]:
        """Ambil semua learning resources"""
        try:
            cursor = self.sumber_daya.find().sort("created_at", -1)
            return list(cursor)
        except Exception as e:
            logger.error(f"Error ambil semua sumber daya: {str(e)}")
            return []
    
    def tambah_sumber_daya(self, data: Dict[str, Any]) -> ObjectId:
        """Tambah learning resource baru - Admin function"""
        try:
            data["created_at"] = datetime.now()
            data["updated_at"] = datetime.now()
            result = self.sumber_daya.insert_one(data)
            logger.info(f"Sumber daya baru ditambahkan: {data.get('judul')}")
            return result.inserted_id
        except Exception as e:
            logger.error(f"Error tambah sumber daya: {str(e)}")
            raise
    
    def buat_sumber_daya(self, sumber: Dict[str, Any]) -> ObjectId:
        """Buat learning resource baru - Admin function (alias untuk tambah_sumber_daya)"""
        return self.tambah_sumber_daya(sumber)
    
    def update_sumber_daya(self, id_sumber: str, data_update: Dict[str, Any]) -> bool:
        """Update learning resource - Admin function"""
        try:
            data_update["updated_at"] = datetime.now()
            result = self.sumber_daya.update_one(
                {"_id": ObjectId(id_sumber)},
                {"$set": data_update}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error update sumber daya: {str(e)}")
            return False
    
    def hapus_sumber_daya(self, id_sumber: str) -> bool:
        """Hapus learning resource - Admin function"""
        try:
            result = self.sumber_daya.delete_one({"_id": ObjectId(id_sumber)})
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Error hapus sumber daya: {str(e)}")
            return False
    
    def ambil_sumber_daya_by_topik(
        self,
        topik: str,
        tipe: Optional[str] = None,
        tingkat: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Ambil learning resources berdasarkan topik (untuk rekomendasi)"""
        try:
            query: Dict[str, Any] = {"topik_terkait": topik}
            if tipe:
                query["tipe"] = tipe
            if tingkat:
                query["tingkat_kesulitan"] = tingkat
            
            cursor = self.sumber_daya.find(query).sort("created_at", -1)
            return list(cursor)
        except Exception as e:
            logger.error(f"Error ambil sumber daya by topik: {str(e)}")
            return []
    
    def daftar_semua_sumber_daya(
        self,
        skip: int = 0,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Ambil semua learning resources - Admin function"""
        try:
            cursor = self.sumber_daya.find().sort("created_at", -1).skip(skip).limit(limit)
            return list(cursor)
        except Exception as e:
            logger.error(f"Error daftar sumber daya: {str(e)}")
            return []
    
    
    # ==================== TOPIC OPERATIONS ====================
    
    def ambil_semua_topik(self) -> List[Dict[str, Any]]:
        """Ambil semua topik pembelajaran"""
        try:
            cursor = self.topik_pembelajaran.find().sort("kategori", 1)
            return list(cursor)
        except Exception as e:
            logger.error(f"Error ambil semua topik: {str(e)}")
            return []
    
    def tambah_topik(self, data: Dict[str, Any]) -> ObjectId:
        """Tambah topik pembelajaran baru - Admin function"""
        try:
            data["created_at"] = datetime.now()
            data["updated_at"] = datetime.now()
            result = self.topik_pembelajaran.insert_one(data)
            logger.info(f"Topik baru ditambahkan: {data.get('nama')}")
            return result.inserted_id
        except Exception as e:
            logger.error(f"Error tambah topik: {str(e)}")
            raise
    
    def buat_topik(self, topik: Dict[str, Any]) -> ObjectId:
        """Buat topik pembelajaran baru - Admin function (alias untuk tambah_topik)"""
        return self.tambah_topik(topik)
    
    def update_topik(self, id_topik: str, data_update: Dict[str, Any]) -> bool:
        """Update topik pembelajaran - Admin function"""
        try:
            data_update["updated_at"] = datetime.now()
            result = self.topik_pembelajaran.update_one(
                {"_id": ObjectId(id_topik)},
                {"$set": data_update}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error update topik: {str(e)}")
            return False
    
    def hapus_topik(self, id_topik: str) -> bool:
        """Hapus topik pembelajaran - Admin function"""
        try:
            result = self.topik_pembelajaran.delete_one({"_id": ObjectId(id_topik)})
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Error hapus topik: {str(e)}")
            return False
    
    def daftar_semua_topik(self) -> List[Dict[str, Any]]:
        """Ambil semua topik pembelajaran"""
        try:
            cursor = self.topik_pembelajaran.find().sort("kategori", 1)
            return list(cursor)
        except Exception as e:
            logger.error(f"Error daftar topik: {str(e)}")
            return []
    
    def increment_error_count_topik(self, nama_topik: str) -> None:
        """Increment error count untuk topik (untuk tracking kesulitan)"""
        try:
            self.topik_pembelajaran.update_one(
                {"nama": nama_topik},
                {"$inc": {"total_error": 1}}
            )
        except Exception as e:
            logger.error(f"Error increment topik error: {str(e)}")
    
    
    # ==================== EXERCISE OPERATIONS ====================
    
    def ambil_semua_exercises(self) -> List[Dict[str, Any]]:
        """Ambil semua exercises"""
        try:
            cursor = self.exercises.find().sort("created_at", -1)
            return list(cursor)
        except Exception as e:
            logger.error(f"Error ambil semua exercises: {str(e)}")
            return []
    
    def tambah_exercise(self, data: Dict[str, Any]) -> ObjectId:
        """Tambah exercise baru - Admin function"""
        try:
            data["created_at"] = datetime.now()
            data["updated_at"] = datetime.now()
            result = self.exercises.insert_one(data)
            logger.info(f"Exercise baru ditambahkan: {data.get('judul')}")
            return result.inserted_id
        except Exception as e:
            logger.error(f"Error tambah exercise: {str(e)}")
            raise
    
    def buat_exercise(self, exercise: Dict[str, Any]) -> ObjectId:
        """Buat exercise baru - Admin function (alias untuk tambah_exercise)"""
        return self.tambah_exercise(exercise)
    
    def update_exercise(self, id_exercise: str, data_update: Dict[str, Any]) -> bool:
        """Update exercise - Admin function"""
        try:
            data_update["updated_at"] = datetime.now()
            result = self.exercises.update_one(
                {"_id": ObjectId(id_exercise)},
                {"$set": data_update}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error update exercise: {str(e)}")
            return False
    
    def hapus_exercise(self, id_exercise: str) -> bool:
        """Hapus exercise - Admin function"""
        try:
            result = self.exercises.delete_one({"_id": ObjectId(id_exercise)})
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Error hapus exercise: {str(e)}")
            return False
    
    def ambil_exercises_by_topik(self, topik: str, tingkat: Optional[str] = None) -> List[Dict[str, Any]]:
        """Ambil exercises berdasarkan topik"""
        try:
            query: Dict[str, Any] = {"topik": topik}
            if tingkat:
                query["tingkat_kesulitan"] = tingkat
            
            cursor = self.exercises.find(query).sort("tingkat_kesulitan", 1)
            return list(cursor)
        except Exception as e:
            logger.error(f"Error ambil exercises: {str(e)}")
            return []
    
    def daftar_semua_exercises(self, skip: int = 0, limit: int = 50) -> List[Dict[str, Any]]:
        """Ambil semua exercises - Admin function"""
        try:
            cursor = self.exercises.find().sort("created_at", -1).skip(skip).limit(limit)
            return list(cursor)
        except Exception as e:
            logger.error(f"Error daftar exercises: {str(e)}")
            return []
    
    
    # ==================== API METRICS OPERATIONS ====================
    
    def simpan_metrik_api(self, metrik: Dict[str, Any]) -> ObjectId:
        """Simpan API metrics untuk monitoring"""
        try:
            result = self.metrik_api.insert_one(metrik)
            return result.inserted_id
        except Exception as e:
            logger.error(f"Error simpan metrik API: {str(e)}")
            raise
    
    def ambil_statistik_api(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Ambil statistik API performance - Admin monitoring"""
        try:
            query: Dict[str, Any] = {}
            if start_date or end_date:
                query["created_at"] = {}
                if start_date:
                    query["created_at"]["$gte"] = start_date
                if end_date:
                    query["created_at"]["$lte"] = end_date
            
            pipeline = [
                {"$match": query},
                {
                    "$group": {
                        "_id": None,
                        "total_request": {"$sum": 1},
                        "rata_rata_waktu": {"$avg": "$waktu_respons"},
                        "request_berhasil": {
                            "$sum": {"$cond": [{"$lt": ["$status_code", 400]}, 1, 0]}
                        },
                        "request_error": {
                            "$sum": {"$cond": [{"$gte": ["$status_code", 400]}, 1, 0]}
                        }
                    }
                }
            ]
            
            result = list(self.metrik_api.aggregate(pipeline))
            if result:
                stats = result[0]
                stats["success_rate"] = (stats["request_berhasil"] / stats["total_request"] * 100) if stats["total_request"] > 0 else 0
                return stats
            else:
                return {
                    "total_request": 0,
                    "rata_rata_waktu": 0.0,
                    "success_rate": 0.0
                }
        except Exception as e:
            logger.error(f"Error ambil statistik API: {str(e)}")
            return {}
    
    
    # ==================== ADMIN ANALYTICS QUERIES ====================
    
    def pertumbuhan_mahasiswa(self, days: int = 30) -> List[Dict[str, Any]]:
        """Ambil statistik pertumbuhan registrasi mahasiswa - Admin analytics"""
        try:
            start_date = datetime.now() - timedelta(days=days)
            
            pipeline = [
                {
                    "$match": {
                        "role": "mahasiswa",
                        "created_at": {"$gte": start_date}
                    }
                },
                {
                    "$group": {
                        "_id": {
                            "$dateToString": {
                                "format": "%Y-%m-%d",
                                "date": "$created_at"
                            }
                        },
                        "jumlah": {"$sum": 1}
                    }
                },
                {
                    "$sort": {"_id": 1}
                }
            ]
            
            result = list(self.users.aggregate(pipeline))
            return result
        except Exception as e:
            logger.error(f"Error pertumbuhan mahasiswa: {str(e)}")
            return []
    
    def top_errors_global(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Ambil top error types secara global - Admin analytics"""
        try:
            pipeline = [
                {
                    "$group": {
                        "_id": "$tipe_error",
                        "jumlah": {"$sum": 1},
                        "mahasiswa_terdampak": {"$addToSet": "$id_mahasiswa"}
                    }
                },
                {
                    "$project": {
                        "tipe_error": "$_id",
                        "jumlah": 1,
                        "jumlah_mahasiswa": {"$size": "$mahasiswa_terdampak"}
                    }
                },
                {
                    "$sort": {"jumlah": -1}
                },
                {
                    "$limit": limit
                }
            ]
            
            result = list(self.submisi_error.aggregate(pipeline))
            return result
        except Exception as e:
            logger.error(f"Error top errors global: {str(e)}")
            return []
    
    def mahasiswa_dengan_kesulitan_terbanyak(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Identifikasi mahasiswa yang paling butuh bantuan - Admin analytics"""
        try:
            pipeline = [
                {
                    "$group": {
                        "_id": "$id_mahasiswa",
                        "total_error": {"$sum": 1},
                        "unique_error_types": {"$addToSet": "$tipe_error"}
                    }
                },
                {
                    "$lookup": {
                        "from": "users",
                        "localField": "_id",
                        "foreignField": "_id",
                        "as": "user_info"
                    }
                },
                {
                    "$unwind": "$user_info"
                },
                {
                    "$project": {
                        "id_mahasiswa": "$_id",
                        "nama": "$user_info.nama",
                        "email": "$user_info.email",
                        "total_error": 1,
                        "unique_error_count": {"$size": "$unique_error_types"}
                    }
                },
                {
                    "$sort": {"total_error": -1}
                },
                {
                    "$limit": limit
                }
            ]
            
            result = list(self.submisi_error.aggregate(pipeline))
            return result
        except Exception as e:
            logger.error(f"Error mahasiswa kesulitan: {str(e)}")
            return []
    
    def topik_paling_sulit(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Identifikasi topik dengan error terbanyak - Admin analytics"""
        try:
            cursor = self.topik_pembelajaran.find().sort("total_error", -1).limit(limit)
            return list(cursor)
        except Exception as e:
            logger.error(f"Error topik sulit: {str(e)}")
            return []
