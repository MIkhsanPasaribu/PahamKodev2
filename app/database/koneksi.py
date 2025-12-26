"""
Koneksi Database - PyMongo untuk Azure Cosmos DB
Mengelola koneksi MongoDB dengan caching untuk performa optimal
"""

from pymongo import MongoClient
from pymongo.database import Database
from typing import Optional
import streamlit as st
from app.config import settings


@st.cache_resource
def dapatkan_koneksi_database() -> MongoClient:
    """
    Dapatkan koneksi PyMongo ke Azure Cosmos DB.
    Cached untuk reuse di seluruh app (singleton pattern).
    
    Returns:
        MongoClient: Instance client MongoDB yang sudah terkoneksi
    """
    try:
        client = MongoClient(
            settings.DATABASE_URL,
            serverSelectionTimeoutMS=5000,  # 5 detik timeout
            connectTimeoutMS=10000,  # 10 detik timeout untuk initial connection
            socketTimeoutMS=30000,  # 30 detik untuk operasi socket
        )
        
        # Test koneksi
        client.server_info()
        
        return client
    except Exception as e:
        st.error(f"❌ Gagal koneksi ke database: {str(e)}")
        raise


def dapatkan_database() -> Database:
    """
    Dapatkan database instance dari client yang sudah cached.
    
    Returns:
        Database: Instance database MongoDB
    """
    client = dapatkan_koneksi_database()
    return client[settings.DATABASE_NAME]


def tutup_koneksi_database() -> None:
    """
    Tutup koneksi database (dipanggil saat aplikasi shutdown).
    Jarang digunakan karena Streamlit mengelola lifecycle otomatis.
    """
    try:
        client = dapatkan_koneksi_database()
        client.close()
    except Exception:
        pass  # Ignore errors saat closing
