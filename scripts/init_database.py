"""
Script untuk initialize database PahamKode
Auto-create collections dengan indexes yang dibutuhkan

Usage:
    python scripts/init_database.py
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import CollectionInvalid

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    print("❌ ERROR: DATABASE_URL tidak ditemukan di .env")
    sys.exit(1)

# Connect to database
print("🔗 Connecting to Azure Cosmos DB...")
client = MongoClient(DATABASE_URL)
db = client["pahamkode-db"]

print(f"✅ Connected to database: {db.name}")

# ==================== CREATE COLLECTIONS ====================

collections_config = {
    "users": {
        "indexes": [
            ("email", ASCENDING),  # Unique index
            ("created_at", DESCENDING),
            ("status", ASCENDING),
        ]
    },
    "submisi_error": {
        "indexes": [
            ("id_mahasiswa", ASCENDING),
            ("created_at", DESCENDING),
            ("tipe_error", ASCENDING),
            [("id_mahasiswa", ASCENDING), ("tipe_error", ASCENDING)],  # Compound index
        ]
    },
    "pola_error": {
        "indexes": [
            ("id_mahasiswa", ASCENDING),
            ("jenis_kesalahan", ASCENDING),
            ("frekuensi", DESCENDING),
            [("id_mahasiswa", ASCENDING), ("jenis_kesalahan", ASCENDING)],  # Compound unique
        ]
    },
    "progress_belajar": {
        "indexes": [
            ("id_mahasiswa", ASCENDING),
            ("topik", ASCENDING),
            ("tingkat_penguasaan", DESCENDING),
        ]
    },
    "sumber_daya": {
        "indexes": [
            ("kategori", ASCENDING),
            ("topik_terkait", ASCENDING),
            ("created_at", DESCENDING),
        ]
    },
    "topik_pembelajaran": {
        "indexes": [
            ("nama", ASCENDING),  # Unique index
            ("kategori", ASCENDING),
            ("total_error", DESCENDING),
        ]
    },
    "exercises": {
        "indexes": [
            ("topik_terkait", ASCENDING),
            ("tingkat_kesulitan", ASCENDING),
            ("created_at", DESCENDING),
        ]
    },
    "metrik_ai": {
        "indexes": [
            ("timestamp", DESCENDING),
            ("model_used", ASCENDING),
        ]
    },
    "metrik_api": {
        "indexes": [
            ("timestamp", DESCENDING),
            ("endpoint", ASCENDING),
            ("status_code", ASCENDING),
        ]
    },
}

print("\n📦 Creating collections & indexes...")

for collection_name, config in collections_config.items():
    try:
        # Create collection (jika belum ada)
        if collection_name not in db.list_collection_names():
            db.create_collection(collection_name)
            print(f"✅ Created collection: {collection_name}")
        else:
            print(f"⚠️  Collection already exists: {collection_name}")
        
        # Create indexes
        collection = db[collection_name]
        for index_spec in config["indexes"]:
            if isinstance(index_spec, tuple):
                # Single field index
                field, direction = index_spec
                index_name = f"{field}_1" if direction == ASCENDING else f"{field}_-1"
                
                # Special handling untuk unique indexes
                unique = False
                if collection_name == "users" and field == "email":
                    unique = True
                elif collection_name == "topik_pembelajaran" and field == "nama":
                    unique = True
                elif collection_name == "pola_error" and field == "jenis_kesalahan":
                    unique = False  # Will be compound unique instead
                
                collection.create_index(
                    [(field, direction)],
                    name=index_name,
                    unique=unique,
                    background=True
                )
                print(f"  📍 Created index: {collection_name}.{index_name}")
            
            elif isinstance(index_spec, list):
                # Compound index
                index_fields = [(field, direction) for field, direction in index_spec]
                index_name = "_".join([f"{field}_{'1' if dir == ASCENDING else '-1'}" 
                                     for field, dir in index_spec])
                
                # Special handling untuk compound unique
                unique = False
                if collection_name == "pola_error":
                    unique = True  # id_mahasiswa + jenis_kesalahan unique
                
                collection.create_index(
                    index_fields,
                    name=index_name,
                    unique=unique,
                    background=True
                )
                print(f"  📍 Created compound index: {collection_name}.{index_name}")
    
    except CollectionInvalid:
        print(f"⚠️  Collection {collection_name} already exists")
    except Exception as e:
        print(f"❌ Error creating collection/index {collection_name}: {str(e)}")

# ==================== SEED INITIAL DATA (OPTIONAL) ====================

print("\n🌱 Seeding initial data...")

# 1. Create admin user (jika belum ada)
import bcrypt

admin_email = "admin@pahamkode.com"
if db.users.count_documents({"email": admin_email}) == 0:
    admin_password = "admin123"  # GANTI dengan password kuat!
    password_hash = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt())
    
    admin_user = {
        "email": admin_email,
        "nama": "Admin PahamKode",
        "password_hash": password_hash.decode('utf-8'),
        "role": "admin",
        "status": "aktif",
        "tingkat_kemahiran": "mahir",
        "created_at": datetime.now()
    }
    
    db.users.insert_one(admin_user)
    print(f"✅ Created admin user: {admin_email} / {admin_password}")
    print("   ⚠️  GANTI PASSWORD ADMIN SETELAH LOGIN PERTAMA!")
else:
    print(f"⚠️  Admin user already exists: {admin_email}")

# 2. Create sample topics (jika belum ada)
sample_topics = [
    {
        "nama": "Variables & Data Types",
        "kategori": "Python Basics",
        "deskripsi": "Pemahaman tentang variabel dan tipe data",
        "tingkat_kesulitan": "pemula",
        "prerequisites": [],
        "total_error": 0,
        "created_at": datetime.now()
    },
    {
        "nama": "Control Flow (If/Else)",
        "kategori": "Python Basics",
        "deskripsi": "Struktur kontrol percabangan",
        "tingkat_kesulitan": "pemula",
        "prerequisites": ["Variables & Data Types"],
        "total_error": 0,
        "created_at": datetime.now()
    },
    {
        "nama": "Loops (For/While)",
        "kategori": "Python Basics",
        "deskripsi": "Perulangan dan iterasi",
        "tingkat_kesulitan": "pemula",
        "prerequisites": ["Variables & Data Types"],
        "total_error": 0,
        "created_at": datetime.now()
    },
    {
        "nama": "Functions",
        "kategori": "Python Intermediate",
        "deskripsi": "Definisi dan pemanggilan fungsi",
        "tingkat_kesulitan": "menengah",
        "prerequisites": ["Control Flow (If/Else)"],
        "total_error": 0,
        "created_at": datetime.now()
    },
    {
        "nama": "Lists & Dictionaries",
        "kategori": "Python Data Structures",
        "deskripsi": "Struktur data list dan dictionary",
        "tingkat_kesulitan": "menengah",
        "prerequisites": ["Variables & Data Types", "Loops (For/While)"],
        "total_error": 0,
        "created_at": datetime.now()
    },
]

for topic in sample_topics:
    if db.topik_pembelajaran.count_documents({"nama": topic["nama"]}) == 0:
        db.topik_pembelajaran.insert_one(topic)
        print(f"✅ Created topic: {topic['nama']}")
    else:
        print(f"⚠️  Topic already exists: {topic['nama']}")

# 3. Create sample learning resources (jika belum ada)
sample_resources = [
    {
        "judul": "Python Variables - Official Docs",
        "deskripsi": "Dokumentasi resmi Python tentang variabel",
        "url": "https://docs.python.org/3/tutorial/introduction.html#using-python-as-a-calculator",
        "tipe": "dokumentasi",
        "kategori": "Python Basics",
        "topik_terkait": ["Variables & Data Types"],
        "tingkat_kesulitan": "pemula",
        "created_at": datetime.now()
    },
    {
        "judul": "Control Flow - W3Schools",
        "deskripsi": "Tutorial interaktif tentang if/else",
        "url": "https://www.w3schools.com/python/python_conditions.asp",
        "tipe": "tutorial",
        "kategori": "Python Basics",
        "topik_terkait": ["Control Flow (If/Else)"],
        "tingkat_kesulitan": "pemula",
        "created_at": datetime.now()
    },
]

for resource in sample_resources:
    if db.sumber_daya.count_documents({"judul": resource["judul"]}) == 0:
        db.sumber_daya.insert_one(resource)
        print(f"✅ Created resource: {resource['judul']}")
    else:
        print(f"⚠️  Resource already exists: {resource['judul']}")

# ==================== SUMMARY ====================

print("\n" + "="*60)
print("🎉 Database initialization completed!")
print("="*60)

print("\n📊 Collections created:")
for collection_name in collections_config.keys():
    count = db[collection_name].count_documents({})
    print(f"  - {collection_name}: {count} documents")

print("\n🔐 Default credentials:")
print(f"  Email: admin@pahamkode.com")
print(f"  Password: admin123")
print("  ⚠️  GANTI PASSWORD SETELAH LOGIN PERTAMA!")

print("\n✅ Ready to use! Run: streamlit run app/main.py")
