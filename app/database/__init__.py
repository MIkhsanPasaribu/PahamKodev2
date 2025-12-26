"""
Database Package - PyMongo Connection & Models

CATATAN: Tidak menggunakan ORM (seperti Prisma), native MongoDB operations
untuk fleksibilitas maksimal dengan Azure Cosmos DB.
"""

# Export koneksi
from .koneksi import dapatkan_koneksi_database, dapatkan_database, tutup_koneksi_database

# Export models
from .models import (
    Pengguna,
    SubmisiError,
    PolaError,
    ProgressBelajar,
    MetrikAI,
    SumberDaya,
    TopikPembelajaran,
    Exercise,
    MetrikAPI
)

# Export queries
from .queries import DatabaseQueries

__all__ = [
    # Koneksi
    'dapatkan_koneksi_database',
    'dapatkan_database',
    'tutup_koneksi_database',
    # Models
    'Pengguna',
    'SubmisiError',
    'PolaError',
    'ProgressBelajar',
    'MetrikAI',
    'SumberDaya',
    'TopikPembelajaran',
    'Exercise',
    'MetrikAPI',
    # Queries
    'DatabaseQueries',
]
