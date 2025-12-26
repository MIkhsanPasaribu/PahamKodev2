"""
Models Database - MongoDB Schemas dengan Dataclasses
Definisi struktur data untuk semua collections di database

CATATAN: Menggunakan dataclasses (bukan ORM) untuk fleksibilitas maksimal dengan MongoDB
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any
from bson import ObjectId


# ==================== USER MODELS ====================

@dataclass
class Pengguna:
    """Model untuk collection 'users' - Mahasiswa & Admin"""
    email: str
    nama: Optional[str]
    password_hash: str
    role: str = "mahasiswa"  # "mahasiswa" atau "admin"
    status: str = "aktif"  # "aktif", "suspended", "nonaktif"
    tingkat_kemahiran: str = "pemula"  # "pemula", "menengah", "mahir"
    created_at: datetime = field(default_factory=datetime.now)
    last_login: Optional[datetime] = None
    _id: Optional[ObjectId] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert ke dict untuk MongoDB insert/update"""
        data = {
            "email": self.email,
            "nama": self.nama,
            "password_hash": self.password_hash,
            "role": self.role,
            "status": self.status,
            "tingkat_kemahiran": self.tingkat_kemahiran,
            "created_at": self.created_at,
            "last_login": self.last_login
        }
        if self._id:
            data["_id"] = self._id
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Pengguna':
        """Create instance dari MongoDB document"""
        return cls(
            email=data["email"],
            nama=data.get("nama"),
            password_hash=data["password_hash"],
            role=data.get("role", "mahasiswa"),
            status=data.get("status", "aktif"),
            tingkat_kemahiran=data.get("tingkat_kemahiran", "pemula"),
            created_at=data.get("created_at", datetime.now()),
            last_login=data.get("last_login"),
            _id=data.get("_id")
        )


# ==================== ERROR SUBMISSION MODELS ====================

@dataclass
class SubmisiError:
    """Model untuk collection 'submisi_error' - Error submissions dengan AI analysis"""
    id_mahasiswa: ObjectId
    kode: str
    pesan_error: str
    bahasa: str = "python"  # python, javascript, java, cpp
    tipe_error: Optional[str] = None
    penyebab_utama: Optional[str] = None
    kesenjangan_konsep: Optional[str] = None
    level_bloom: Optional[str] = None  # Remember, Understand, Apply, Analyze, Evaluate, Create
    penjelasan: Optional[str] = None
    saran_perbaikan: Optional[str] = None
    topik_terkait: List[str] = field(default_factory=list)
    saran_latihan: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    _id: Optional[ObjectId] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert ke dict untuk MongoDB"""
        data = {
            "id_mahasiswa": self.id_mahasiswa,
            "kode": self.kode,
            "pesan_error": self.pesan_error,
            "bahasa": self.bahasa,
            "tipe_error": self.tipe_error,
            "penyebab_utama": self.penyebab_utama,
            "kesenjangan_konsep": self.kesenjangan_konsep,
            "level_bloom": self.level_bloom,
            "penjelasan": self.penjelasan,
            "saran_perbaikan": self.saran_perbaikan,
            "topik_terkait": self.topik_terkait,
            "saran_latihan": self.saran_latihan,
            "created_at": self.created_at
        }
        if self._id:
            data["_id"] = self._id
        return data


# ==================== PATTERN MODELS ====================

@dataclass
class PolaError:
    """Model untuk collection 'pola_error' - Detected error patterns"""
    id_mahasiswa: ObjectId
    jenis_kesalahan: str
    frekuensi: int = 1
    kejadian_pertama: Optional[datetime] = None
    kejadian_terakhir: datetime = field(default_factory=datetime.now)
    deskripsi_miskonsepsi: Optional[str] = None
    sumber_daya_direkomendasikan: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    _id: Optional[ObjectId] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert ke dict untuk MongoDB"""
        data = {
            "id_mahasiswa": self.id_mahasiswa,
            "jenis_kesalahan": self.jenis_kesalahan,
            "frekuensi": self.frekuensi,
            "kejadian_pertama": self.kejadian_pertama,
            "kejadian_terakhir": self.kejadian_terakhir,
            "deskripsi_miskonsepsi": self.deskripsi_miskonsepsi,
            "sumber_daya_direkomendasikan": self.sumber_daya_direkomendasikan,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
        if self._id:
            data["_id"] = self._id
        return data


# ==================== PROGRESS MODELS ====================

@dataclass
class ProgressBelajar:
    """Model untuk collection 'progress_belajar' - Learning progress per topik"""
    id_mahasiswa: ObjectId
    topik: str
    tingkat_penguasaan: int = 0  # 0-100
    jumlah_error_di_topik: int = 0
    tanggal_error_terakhir: Optional[datetime] = None
    tren_perbaikan: Optional[str] = None  # "membaik", "stagnan", "menurun"
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    _id: Optional[ObjectId] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert ke dict untuk MongoDB"""
        data = {
            "id_mahasiswa": self.id_mahasiswa,
            "topik": self.topik,
            "tingkat_penguasaan": self.tingkat_penguasaan,
            "jumlah_error_di_topik": self.jumlah_error_di_topik,
            "tanggal_error_terakhir": self.tanggal_error_terakhir,
            "tren_perbaikan": self.tren_perbaikan,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
        if self._id:
            data["_id"] = self._id
        return data


# ==================== AI METRICS MODELS ====================

@dataclass
class MetrikAI:
    """Model untuk collection 'metrik_ai' - AI model usage tracking untuk admin"""
    id_submisi: Optional[ObjectId] = None
    model: str = "gpt-4o-mini"  # Model yang digunakan
    token_input: int = 0
    token_output: int = 0
    total_token: int = 0
    biaya: float = 0.0  # Dalam USD
    waktu_respons: float = 0.0  # Dalam detik
    status_berhasil: bool = True
    error_message: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    _id: Optional[ObjectId] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert ke dict untuk MongoDB"""
        data = {
            "id_submisi": self.id_submisi,
            "model": self.model,
            "token_input": self.token_input,
            "token_output": self.token_output,
            "total_token": self.total_token,
            "biaya": self.biaya,
            "waktu_respons": self.waktu_respons,
            "status_berhasil": self.status_berhasil,
            "error_message": self.error_message,
            "created_at": self.created_at
        }
        if self._id:
            data["_id"] = self._id
        return data


# ==================== LEARNING RESOURCES MODELS ====================

@dataclass
class SumberDaya:
    """Model untuk collection 'sumber_daya' - Learning resources (managed by admin)"""
    judul: str
    deskripsi: Optional[str] = None
    tipe: str = "artikel"  # video, artikel, tutorial, exercise, quiz
    url: Optional[str] = None
    konten: Optional[str] = None  # Untuk konten internal (quiz/exercise)
    topik_terkait: List[str] = field(default_factory=list)
    tingkat_kesulitan: str = "pemula"  # pemula, menengah, mahir
    durasi: Optional[int] = None  # Durasi dalam menit
    dibuat_oleh: Optional[ObjectId] = None  # Admin yang membuat
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    _id: Optional[ObjectId] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert ke dict untuk MongoDB"""
        data = {
            "judul": self.judul,
            "deskripsi": self.deskripsi,
            "tipe": self.tipe,
            "url": self.url,
            "konten": self.konten,
            "topik_terkait": self.topik_terkait,
            "tingkat_kesulitan": self.tingkat_kesulitan,
            "durasi": self.durasi,
            "dibuat_oleh": self.dibuat_oleh,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
        if self._id:
            data["_id"] = self._id
        return data


# ==================== TOPIC MODELS ====================

@dataclass
class TopikPembelajaran:
    """Model untuk collection 'topik_pembelajaran' - Learning topics (managed by admin)"""
    nama: str
    deskripsi: Optional[str] = None
    kategori: str = "dasar"  # dasar, lanjutan, expert
    tingkat_kesulitan: str = "pemula"
    prerequisite: List[str] = field(default_factory=list)  # Topik yang harus dikuasai dulu
    tujuan_pembelajaran: List[str] = field(default_factory=list)
    estimasi_waktu: Optional[int] = None  # Dalam menit
    total_error: int = 0  # Counter untuk tracking kesulitan topik
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    _id: Optional[ObjectId] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert ke dict untuk MongoDB"""
        data = {
            "nama": self.nama,
            "deskripsi": self.deskripsi,
            "kategori": self.kategori,
            "tingkat_kesulitan": self.tingkat_kesulitan,
            "prerequisite": self.prerequisite,
            "tujuan_pembelajaran": self.tujuan_pembelajaran,
            "estimasi_waktu": self.estimasi_waktu,
            "total_error": self.total_error,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
        if self._id:
            data["_id"] = self._id
        return data


# ==================== EXERCISE MODELS ====================

@dataclass
class Exercise:
    """Model untuk collection 'exercises' - Practice exercises"""
    judul: str
    deskripsi: str
    topik: str
    tingkat_kesulitan: str = "pemula"
    instruksi: str = ""
    kode_pemula: Optional[str] = None  # Starter code
    solusi_referensi: str = ""
    test_cases: List[str] = field(default_factory=list)
    poin_belajar: List[str] = field(default_factory=list)
    estimasi_waktu: Optional[int] = None
    dibuat_oleh: Optional[ObjectId] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    _id: Optional[ObjectId] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert ke dict untuk MongoDB"""
        data = {
            "judul": self.judul,
            "deskripsi": self.deskripsi,
            "topik": self.topik,
            "tingkat_kesulitan": self.tingkat_kesulitan,
            "instruksi": self.instruksi,
            "kode_pemula": self.kode_pemula,
            "solusi_referensi": self.solusi_referensi,
            "test_cases": self.test_cases,
            "poin_belajar": self.poin_belajar,
            "estimasi_waktu": self.estimasi_waktu,
            "dibuat_oleh": self.dibuat_oleh,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
        if self._id:
            data["_id"] = self._id
        return data


# ==================== API METRICS MODELS ====================

@dataclass
class MetrikAPI:
    """Model untuk collection 'metrik_api' - API performance tracking"""
    endpoint: str
    method: str  # GET, POST, etc
    status_code: int
    waktu_respons: float  # Dalam milidetik
    user_agent: Optional[str] = None
    ip_address: Optional[str] = None
    error_message: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    _id: Optional[ObjectId] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert ke dict untuk MongoDB"""
        data = {
            "endpoint": self.endpoint,
            "method": self.method,
            "status_code": self.status_code,
            "waktu_respons": self.waktu_respons,
            "user_agent": self.user_agent,
            "ip_address": self.ip_address,
            "error_message": self.error_message,
            "created_at": self.created_at
        }
        if self._id:
            data["_id"] = self._id
        return data
