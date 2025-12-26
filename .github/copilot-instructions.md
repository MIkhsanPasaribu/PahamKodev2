# PahamKode - Copilot Instructions

## Project Overview

PahamKode adalah aplikasi web berbasis cloud computing untuk analisis semantik error pemrograman. Sistem ini menggunakan AI untuk menganalisis error dari sudut pandang konseptual, bukan hanya sintaks, dengan fokus pada pemahaman mendalam tentang **mengapa** error terjadi.

## Syarat Pengembangan

- **Bahasa**: Full Bahasa Indonesia untuk semua kode pada string, nama variabel, dan komentar (kecuali nama file dan library eksternal)
- **Code Quality**: Mengikuti best practices & pattern terbaik, readable, clean, maintainable, scalable, reliable, dan simple.

### Core Objectives

1. **Semantic Error Analysis** - Analisis error secara konseptual, bukan hanya teknis
2. **Pattern Mining** - Identifikasi pola kesalahan berulang mahasiswa
3. **Adaptive Explanation** - Penjelasan disesuaikan dengan level kognitif (Bloom's Taxonomy)
4. **Personalized Learning** - Rekomendasi pembelajaran yang dipersonalisasi

---

## Architecture & Tech Stack

### System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    STREAMLIT APP (Fullstack)                    │
│  Python 3.11+ dengan Streamlit Framework                       │
│  Frontend + Backend dalam satu aplikasi                        │
│  Deployed on: Azure Virtual Machine B1s (~$7.59/month)         │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              AI ORCHESTRATION                            │  │
│  │  • LangChain for prompt management                       │  │
│  │  • GitHub Models (FREE) - RECOMMENDED                    │  │
│  │  • Structured outputs dengan dataclasses                 │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              UI COMPONENTS                               │  │
│  │  • st.sidebar untuk navigasi                             │  │
│  │  • streamlit-ace untuk code editor                       │  │
│  │  • plotly/altair untuk visualisasi                       │  │
│  │  • Session state untuk authentication                    │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              ↓ PyMongo
┌─────────────────────────────────────────────────────────────────┐
│                      DATABASE LAYER                             │
│  Azure Cosmos DB (FREE TIER)                                    │
│  • MongoDB API                                                  │
│  • PyMongo untuk native MongoDB operations                     │
│  • Session-based authentication                                │
│  • Global distribution & low latency                           │
└─────────────────────────────────────────────────────────────────┘
```

### Tech Stack Details

#### Application Framework

- **Framework**: Streamlit (Fullstack Python)
- **Language**: Python 3.11+ dengan type hints
- **UI Components**: Streamlit native components
- **Code Editor**: streamlit-ace (syntax highlighting)
- **Charts**: Plotly / Altair / Matplotlib
- **State Management**: st.session_state
- **Deployment**: Azure Virtual Machine B1s (~$7.59/month)
- **Port**: 8501 (default Streamlit port)

#### Core Libraries

- **AI Framework**: LangChain
- **Database Driver**: PyMongo (native MongoDB)
- **Validation**: dataclasses + type hints
- **Environment**: python-dotenv
- **Authentication**: Session-based (st.session_state)
- **Password Hashing**: bcrypt
- **Date/Time**: datetime, timezone

#### Database & Auth

- **Database**: Azure Cosmos DB (Free Tier - MongoDB API)
- **Driver**: PyMongo (native MongoDB driver)
- **Auth**: Session-based authentication (Streamlit session state)
- **Storage**: 1000 RU/s, 25GB storage (Free tier)
- **Benefits**: Global distribution, low latency, auto-scaling
- **Schema**: Manual schemas dengan dataclasses (no ORM)

#### AI Services (Cost-Efficient Options)

**Option 1 (RECOMMENDED - Llama 3.1 70B Powerful & Cheap!):**

- **Provider**: Azure AI Model Catalog / Azure ML Inference
- **Model**: **Llama 3.1 70B Instruct** (Meta's powerful open model)
- **Cost**:
  - Input: $0.000264/1K tokens
  - Output: $0.000264/1K tokens
  - **Cheaper than GPT-4o-mini + More powerful!**
- **Example Calculations**:

  ```
  10K analysis/month @ 500 tokens each:
  = 10,000 × 500 × $0.000264/1000
  = $1.32/month ✅ SUPER MURAH!

  100K analysis/month:
  = ~$13.20/month (sangat affordable!)
  ```

- **Pros**:
  - 70B parameters (very capable for semantic analysis)
  - Open source (no vendor lock-in)
  - Strong reasoning & multilingual support
  - Best value for money (quality vs price)
- **Best for**: Production apps dengan budget ketat tapi butuh quality tinggi

**Option 2 (FREE - For Development):**

- **Provider**: GitHub Models (Powered by Azure Infrastructure)
- **Models Available**:
  - **GPT-4o-mini**: Fast, efficient, FREE
  - **GPT-4o**: Most capable, FREE
  - **Phi-3-mini/medium**: Microsoft's open model, FREE
  - **Llama 3**: Meta's model, FREE
- **Endpoint**: `models.inference.ai.azure.com`
- **Cost**: **$0/month** (100% GRATIS!)
- **Rate Limits**:
  - 15 requests/minute per model
  - 150K tokens/day per model
- **Best for**: Development, testing, prototyping

**Option 3 (Alternative - Azure OpenAI):**

- **Provider**: Azure OpenAI Service
- **Model**: **GPT-4o-mini**
- **Cost**:
  - Input: $0.00015/1K tokens
  - Output: $0.0006/1K tokens
- **Example Calculations**:

  ```
  10K analysis/month @ 500 tokens each:
  = 10,000 × (250 input + 250 output) tokens
  = 10,000 × (250×0.00015 + 250×0.0006)/1000
  = 10,000 × $0.0001875
  = $1.88/month ✅ SUPER MURAH!

  100K analysis/month:
  = ~$18.75/month (still affordable!)
  ```

- **Best for**: Production dengan budget ketat, high traffic

**Option 3 (ALTERNATIVE - Cheapest Azure OpenAI):**

- **Provider**: Azure OpenAI Service
- **Model**: **GPT-3.5-turbo**
- **Cost**:
  - Input: $0.0005/1K tokens
  - Output: $0.0015/1K tokens
- **Example**: 50K requests @ 500 tokens = ~$50/month
- **Best for**: Production standard

**Option 4 (LLAMA 3.1 70B - Powerful & Cheap!):**

- **Provider**: Azure AI Model Catalog / Azure ML Inference
- **Model**: **Llama 3.1 70B Instruct** (Meta's powerful open model)
- **Cost**:
  - Input: $0.000264/1K tokens
  - Output: $0.000264/1K tokens
  - **Cheaper than GPT-4o-mini!**
- **Example Calculations**:

  ```
  10K analysis/month @ 500 tokens each:
  = 10,000 × 500 × $0.000264/1000
  = $1.32/month ✅ LEBIH MURAH dari GPT-4o-mini!

  100K analysis/month:
  = ~$13.20/month (sangat affordable!)
  ```

- **Pros**:
  - 70B parameters (very capable for semantic analysis)
  - Open source (no vendor lock-in)
  - Strong reasoning capabilities
  - Good multilingual support
- **Cons**:
  - Perlu deploy ke Azure ML endpoint (setup lebih kompleks)
  - Cold start time
  - Need to manage endpoint
- **Best for**: Production dengan budget ketat tapi butuh quality tinggi

**Option 5 (OPEN SOURCE - Ultra Cheap):**

- **Provider**: Azure AI Model Catalog / Azure ML Inference
- **Models**:
  - **Phi-3-mini**: Microsoft's 3.8B parameter model
  - **Phi-3-medium**: Microsoft's 14B parameter model
  - **Mistral-7B**: Open source, efficient
  - **Llama-3-8B**: Meta's smaller model
- **Cost**: $0.0001-0.0003/1K tokens (10x lebih murah!)
- **Deployment**: Azure ML Managed Endpoint
- **Example**: 100K requests = ~$3-10/month
- **Trade-off**: Lower quality than Llama 3.1 70B or GPT models
- **Best for**: Budget maksimal tapi OK dengan kualitas sedang

---

**💡 RECOMMENDATION untuk PahamKode:**

**Development Phase:**

```python
# .env
USE_GITHUB_MODELS=true  # For free development
GITHUB_TOKEN=ghp_your_token_here
MODEL_NAME=gpt-4o-mini
```

**Production Phase (RECOMMENDED - Llama 3.1 70B):**

```python
# .env
USE_LLAMA=true
LLAMA_ENDPOINT_URL=https://pahamkode-llama.southeastasia.inference.ml.azure.com/score
LLAMA_API_KEY=your_llama_endpoint_key
```

**Budget Breakdown dengan Budget $30-40:**

1. **Recommended Setup (Llama 3.1 70B):**

   - VM: $7.59/month
   - Llama 3.1 70B: ~$1.32/month (10K requests) to ~$13/month (100K requests)
   - **Total: $8.91-20.59/month** ✅✅
   - **Quality**: ⭐⭐⭐⭐⭐ (70B parameters)
   - Good for: Production dengan quality tinggi & cost-efficient

2. **Alternative 1 (GitHub Models - FREE):**

   - VM: $7.59/month
   - GitHub Models: $0/month
   - **Total: $7.59/month** ✅
   - Good for: Development & low traffic (<10K users)

3. **Alternative 2 (Azure OpenAI):**
   - VM: $7.59/month
   - GPT-4o-mini: ~$5-20/month
   - **Total: $12.59-27.59/month** ✅
   - Good for: Jika tidak mau setup Azure ML endpoint

---

## Development Guidelines

### 1. Streamlit Application Development

#### File Structure

```
app/
├── main.py                      # Streamlit entry point (landing page)
├── config.py                    # Environment & settings
├── database/
│   ├── __init__.py
│   ├── koneksi.py               # PyMongo connection
│   ├── models.py                # MongoDB schemas (dataclasses)
│   └── queries.py               # Database operations
├── services/
│   ├── __init__.py
│   ├── ai_service.py            # GitHub Models + LangChain
│   ├── analisis_service.py      # Semantic analysis logic
│   ├── pola_service.py          # Pattern mining
│   └── autentikasi_service.py   # Session-based auth
├── pages/
│   ├── 1_🔍_Analisis.py         # Analysis page (main feature)
│   ├── 2_📜_Riwayat.py          # History page
│   ├── 3_📊_Pola.py             # Patterns page
│   └── 4_📈_Progress.py         # Progress dashboard
├── components/
│   ├── __init__.py
│   ├── sidebar.py               # Navigation sidebar
│   ├── autentikasi.py           # Login/register forms
│   └── visualisasi.py           # Charts & graphs
└── utils/
    ├── __init__.py
    ├── prompts.py               # LangChain prompts
    ├── keamanan.py              # Password hashing
    └── helpers.py               # Utility functions
```

#### Best Practices

**1. Server Components First**

```typescript
// app/history/page.tsx - Use Server Component by default
// Fetch data via Backend API dengan server-side fetch

export default async function HistoryPage() {
  // Get auth token from cookies
  const token = cookies().get("auth_token")?.value;

  // Fetch data directly in Server Component
  const response = await fetch(
    `${process.env.NEXT_PUBLIC_API_URL}/api/history`,
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
      cache: "no-store",
    }
  );

  const submissions = await response.json();

  return <HistoryList submissions={submissions} />;
}
```

**2. Client Components Only When Needed**

```typescript
// components/editor/code-editor.tsx
"use client";

import { useState } from "react";
import Editor from "@monaco-editor/react";

export function CodeEditor() {
  const [code, setCode] = useState("");
  // Interactive components need 'use client'
  return <Editor value={code} onChange={(val) => setCode(val || "")} />;
}
```

**3. Type-Safe API Calls**

```typescript
// lib/api-client.ts
import { z } from "zod";

const AnalysisResponseSchema = z.object({
  error_type: z.string(),
  root_cause: z.string(),
  conceptual_gap: z.string(),
  bloom_level: z.enum([
    "Remember",
    "Understand",
    "Apply",
    "Analyze",
    "Evaluate",
    "Create",
  ]),
  explanation: z.string(),
  fix_suggestion: z.string(),
  related_topics: z.array(z.string()),
  practice_suggestion: z.string(),
});

export type AnalysisResponse = z.infer<typeof AnalysisResponseSchema>;

export async function analyzeError(data: {
  code: string;
  error_message: string;
  language: string;
}) {
  const response = await fetch(
    `${process.env.NEXT_PUBLIC_API_URL}/api/analyze`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    }
  );

  const json = await response.json();
  return AnalysisResponseSchema.parse(json);
}
```

**4. Environment Variables**

```typescript
// .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**5. shadcn/ui Integration**

```bash
# Install shadcn/ui
npx shadcn-ui@latest init

# Add components as needed
npx shadcn-ui@latest add button
npx shadcn-ui@latest add card
npx shadcn-ui@latest add badge
```

---

### 2. Backend Development (FastAPI)

#### File Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Environment variables
│   ├── database.py          # Prisma client setup
│   ├── models/
│   │   └── schemas.py       # Pydantic schemas
│   ├── services/
│   │   ├── ai_service.py    # LangChain + AI integration
│   │   ├── analysis_service.py
│   │   └── pattern_service.py
│   ├── routes/
│   │   ├── analyze.py
│   │   ├── history.py
│   │   └── patterns.py
│   └── utils/
│       ├── prompts.py       # LangChain prompt templates
│       └── parsers.py       # Output parsers
├── prisma/
│   └── schema.prisma        # Prisma schema
├── requirements.txt
└── .env
```

#### Best Practices

**1. Streamlit App Structure**

```python
# app/main.py
import streamlit as st
from app.config import Settings
from app.database.koneksi import dapatkan_koneksi_database
from app.components.sidebar import render_sidebar
from app.components.autentikasi import render_login_page

# Page config
st.set_page_config(
    page_title="PahamKode - Analisis Error Semantik",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    """Entry point untuk aplikasi Streamlit"""

    # Initialize session state
    if "pengguna" not in st.session_state:
        st.session_state.pengguna = None

    # Database connection
    if "db" not in st.session_state:
        st.session_state.db = dapatkan_koneksi_database()

    # Authentication check
    if st.session_state.pengguna is None:
        render_login_page()
    else:
        # Render sidebar
        render_sidebar()

        # Landing page content
        st.title("🧠 PahamKode")
        st.subheader("Analisis Semantik Error Pemrograman")

        st.markdown("""
        ## Apa itu PahamKode?

        Sistem AI yang menganalisis error pemrograman dari sudut pandang **konseptual**,
        bukan hanya sintaks. Kami fokus pada **MENGAPA** error terjadi.

        ### 🎯 Fitur Utama:
        1. **Analisis Semantik** - Root cause analysis konseptual
        2. **Pattern Mining** - Deteksi pola kesalahan berulang
        3. **Adaptive Explanation** - Penjelasan disesuaikan Bloom's Taxonomy
        4. **Personalized Learning** - Rekomendasi belajar dipersonalisasi
        """)

if __name__ == "__main__":
    main()
```

**2. PyMongo Database Connection**

```python
# app/database/koneksi.py
from pymongo import MongoClient
from typing import Optional
import streamlit as st
from app.config import settings

@st.cache_resource
def dapatkan_koneksi_database() -> MongoClient:
    """
    Dapatkan koneksi PyMongo ke Azure Cosmos DB.
    Cached untuk reuse di seluruh app.
    """
    client = MongoClient(settings.DATABASE_URL)
    return client

def dapatkan_database():
    """Dapatkan database instance"""
    client = dapatkan_koneksi_database()
    return client[settings.DATABASE_NAME]
```

**3. MongoDB Schemas dengan Dataclasses**

```python
# app/database/models.py
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from bson import ObjectId

@dataclass
class Pengguna:
    email: str
    nama: Optional[str]
    password_hash: str
    role: str = "mahasiswa"
    status: str = "aktif"
    tingkat_kemahiran: str = "pemula"
    created_at: datetime = field(default_factory=datetime.now)
    _id: Optional[ObjectId] = None

    def to_dict(self):
        """Convert ke dict untuk MongoDB"""
        data = {
            "email": self.email,
            "nama": self.nama,
            "password_hash": self.password_hash,
            "role": self.role,
            "status": self.status,
            "tingkat_kemahiran": self.tingkat_kemahiran,
            "created_at": self.created_at
        }
        if self._id:
            data["_id"] = self._id
        return data

    @classmethod
    def from_dict(cls, data: dict):
        """Create dari MongoDB document"""
        return cls(
            email=data["email"],
            nama=data.get("nama"),
            password_hash=data["password_hash"],
            role=data.get("role", "mahasiswa"),
            status=data.get("status", "aktif"),
            tingkat_kemahiran=data.get("tingkat_kemahiran", "pemula"),
            created_at=data.get("created_at", datetime.now()),
            _id=data.get("_id")
        )

@dataclass
class SubmisiError:
    id_mahasiswa: ObjectId
    kode: str
    pesan_error: str
    bahasa: str = "python"
    tipe_error: Optional[str] = None
    penyebab_utama: Optional[str] = None
    kesenjangan_konsep: Optional[str] = None
    level_bloom: Optional[str] = None
    penjelasan: Optional[str] = None
    saran_perbaikan: Optional[str] = None
    topik_terkait: List[str] = field(default_factory=list)
    saran_latihan: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    _id: Optional[ObjectId] = None

    def to_dict(self):
        """Convert ke dict untuk MongoDB"""
        return {
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
```

**4. Database Queries**

```python
# app/database/queries.py
from pymongo import MongoClient
from pymongo.database import Database
from typing import Dict, List, Optional
from bson import ObjectId
from datetime import datetime

class DatabaseQueries:
    def __init__(self, db: Database):
        self.db = db

    # User operations
    def buat_pengguna(self, data_pengguna: Dict) -> ObjectId:
        """Buat user baru"""
        result = self.db.users.insert_one(data_pengguna)
        return result.inserted_id

    def cari_pengguna_by_email(self, email: str) -> Optional[Dict]:
        """Cari user berdasarkan email"""
        return self.db.users.find_one({"email": email})

    def cari_pengguna_by_id(self, id_pengguna: str) -> Optional[Dict]:
        """Cari user berdasarkan ID"""
        return self.db.users.find_one({"_id": ObjectId(id_pengguna)})

    # SubmisiError operations
    def simpan_submisi_error(self, submisi: Dict) -> ObjectId:
        """Simpan submisi error baru"""
        result = self.db.submisi_error.insert_one(submisi)
        return result.inserted_id

    def ambil_riwayat_submisi(self, id_mahasiswa: str, limit: int = 20) -> List[Dict]:
        """Ambil riwayat submisi mahasiswa"""
        cursor = self.db.submisi_error.find(
            {"id_mahasiswa": ObjectId(id_mahasiswa)}
        ).sort("created_at", -1).limit(limit)
        return list(cursor)

    def hitung_submisi_by_tipe(self, id_mahasiswa: str, tipe_error: str) -> int:
        """Hitung jumlah error dengan tipe tertentu"""
        return self.db.submisi_error.count_documents({
            "id_mahasiswa": ObjectId(id_mahasiswa),
            "tipe_error": tipe_error
        })

    # PolaError operations
    def buat_atau_update_pola(self, id_mahasiswa: str, tipe_error: str,
                               deskripsi_miskonsepsi: str,
                               topik_terkait: List[str]) -> None:
        """Buat atau update pola error"""
        frekuensi = self.hitung_submisi_by_tipe(id_mahasiswa, tipe_error)

        self.db.pola_error.update_one(
            {
                "id_mahasiswa": ObjectId(id_mahasiswa),
                "jenis_kesalahan": tipe_error
            },
            {
                "$set": {
                    "frekuensi": frekuensi,
                    "kejadian_terakhir": datetime.now(),
                    "deskripsi_miskonsepsi": deskripsi_miskonsepsi,
                    "sumber_daya_direkomendasikan": topik_terkait,
                    "updated_at": datetime.now()
                },
                "$setOnInsert": {
                    "kejadian_pertama": datetime.now(),
                    "created_at": datetime.now()
                }
            },
            upsert=True
        )

    def ambil_pola_mahasiswa(self, id_mahasiswa: str) -> List[Dict]:
        """Ambil semua pola error mahasiswa"""
        cursor = self.db.pola_error.find(
            {"id_mahasiswa": ObjectId(id_mahasiswa)}
        ).sort("frekuensi", -1)
        return list(cursor)
```

**5. Session State Management**

```python
# app/components/autentikasi.py
import streamlit as st
import bcrypt
from app.database.queries import DatabaseQueries
from app.database.koneksi import dapatkan_database

def render_login_page():
    """Render halaman login"""
    st.title("🔐 Login ke PahamKode")

    with st.form("form_login"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

        if submit:
            if not email or not password:
                st.error("Email dan password harus diisi!")
                return

            db = dapatkan_database()
            queries = DatabaseQueries(db)

            pengguna = queries.cari_pengguna_by_email(email)

            if pengguna and bcrypt.checkpw(
                password.encode('utf-8'),
                pengguna['password_hash'].encode('utf-8')
            ):
                st.session_state.pengguna = pengguna
                st.success("Login berhasil!")
                st.rerun()
            else:
                st.error("Email atau password salah!")

    st.markdown("---")
    st.markdown("Belum punya akun? [Registrasi](/?page=register)")

def render_register_page():
    """Render halaman registrasi"""
    st.title("📝 Registrasi Akun Baru")

    with st.form("form_register"):
        nama = st.text_input("Nama Lengkap")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        password_konfirmasi = st.text_input("Konfirmasi Password", type="password")
        submit = st.form_submit_button("Daftar")

        if submit:
            if not all([nama, email, password, password_konfirmasi]):
                st.error("Semua field harus diisi!")
                return

            if password != password_konfirmasi:
                st.error("Password tidak cocok!")
                return

            db = dapatkan_database()
            queries = DatabaseQueries(db)

            # Check if email exists
            if queries.cari_pengguna_by_email(email):
                st.error("Email sudah terdaftar!")
                return

            # Hash password
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            # Create user
            data_pengguna = {
                "nama": nama,
                "email": email,
                "password_hash": password_hash.decode('utf-8'),
                "role": "mahasiswa",
                "status": "aktif",
                "tingkat_kemahiran": "pemula",
                "created_at": datetime.now()
            }

            queries.buat_pengguna(data_pengguna)
            st.success("Registrasi berhasil! Silakan login.")
```

---

### 2. Database with PyMongo (No Prisma)

```python
# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routes import analyze, history, patterns

app = FastAPI(
    title="PahamKode API",
    description="Semantic Error Analysis API",
    version="1.0.0"
)

# CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(analyze.router, prefix="/api/analyze", tags=["analyze"])
app.include_router(history.router, prefix="/api/history", tags=["history"])
app.include_router(patterns.router, prefix="/api/patterns", tags=["patterns"])

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

**2. Prisma Client Setup**

```python
# app/database.py
from prisma import Prisma

prisma = Prisma()

async def connect_db():
    """Connect to database on startup"""
    await prisma.connect()

async def disconnect_db():
    """Disconnect from database on shutdown"""
    await prisma.disconnect()

# In main.py
@app.on_event("startup")
async def startup():
    await connect_db()

@app.on_event("shutdown")
async def shutdown():
    await disconnect_db()
```

**3. Pydantic Schemas**

```python
# app/models/schemas.py
from pydantic import BaseModel, Field
from typing import List
from enum import Enum

class BloomLevel(str, Enum):
    REMEMBER = "Remember"
    UNDERSTAND = "Understand"
    APPLY = "Apply"
    ANALYZE = "Analyze"
    EVALUATE = "Evaluate"
    CREATE = "Create"

class AnalyzeRequest(BaseModel):
    code: str = Field(..., description="Code with error")
    error_message: str = Field(..., description="Error message")
    language: str = Field(default="python", description="Programming language")
    student_id: str = Field(..., description="Student UUID")

class AnalysisResult(BaseModel):
    error_type: str
    root_cause: str
    conceptual_gap: str
    bloom_level: BloomLevel
    explanation: str
    fix_suggestion: str
    related_topics: List[str]
    practice_suggestion: str
    pattern_alert: str | None = None
    similar_past_errors: int = 0
```

**4. LangChain Integration (Cost-Efficient)**

```python
# app/services/ai_service.py
from langchain_openai import AzureChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from app.models.schemas import AnalysisResult
from app.config import settings

# Option 1 (RECOMMENDED): Llama 3.1 70B
def get_llm_llama():
    """Use Llama 3.1 70B for powerful & cheap inference"""
    from langchain_community.llms import AzureMLOnlineEndpoint

    return AzureMLOnlineEndpoint(
        endpoint_url=settings.LLAMA_ENDPOINT_URL,
        endpoint_api_key=settings.LLAMA_API_KEY,
        deployment_name="llama-3-1-70b-instruct",
        temperature=0.3,
    )

# Option 2: GitHub Models (FREE for development)
def get_llm_github_models():
    """Use GitHub Models for free AI inference"""
    return AzureChatOpenAI(
        model="gpt-4o-mini",  # or "gpt-4o"
        api_key=settings.GITHUB_TOKEN,
        azure_endpoint="https://models.inference.ai.azure.com",
        api_version="2024-02-01",
        temperature=0.3,
    )

# Option 3: Azure OpenAI (Alternative)
def get_llm_azure_openai():
    """Use Azure OpenAI for production"""
    return AzureChatOpenAI(
        model="gpt-4o-mini",
        api_key=settings.AZURE_OPENAI_API_KEY,
        azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
        api_version="2024-02-01",
        temperature=0.3,
    )

# Auto-select based on environment
def get_llm():
    if settings.USE_LLAMA:
        return get_llm_llama()
    elif settings.USE_GITHUB_MODELS:
        return get_llm_github_models()
    else:
        return get_llm_azure_openai()
```

**Cost Comparison untuk 10K requests @ 500 tokens each:**

```
GitHub Models:      $0          (FREE!)
Llama 3.1 70B:      $1.32       (cheapest paid + powerful!)
GPT-4o-mini:        $1.88       (Azure OpenAI cheapest)
GPT-3.5-turbo:      $5.00       (standard)
Phi-3-mini:         $0.50-$1.00 (ultra cheap, smaller model)
```

**Quality Comparison:**

```
┌──────────────────┬─────────────┬──────────┬────────────┐
│ Model            │ Parameters  │ Quality  │ Cost/10K   │
├──────────────────┼─────────────┼──────────┼────────────┤
│ Llama 3.1 70B    │ 70B         │ ⭐⭐⭐⭐⭐ │ $1.32      │
│ GPT-4o-mini      │ Proprietary │ ⭐⭐⭐⭐⭐ │ $1.88      │
│ GPT-3.5-turbo    │ Proprietary │ ⭐⭐⭐⭐  │ $5.00      │
│ Phi-3-medium     │ 14B         │ ⭐⭐⭐⭐  │ $1.00      │
│ Phi-3-mini       │ 3.8B        │ ⭐⭐⭐   │ $0.50      │
└──────────────────┴─────────────┴──────────┴────────────┘
```

**5. Semantic Analysis with LangChain**

````python
# app/services/analysis_service.py
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from app.services.ai_service import get_llm
from app.models.schemas import AnalysisResult
from app.database import prisma

async def analyze_error_semantically(
    code: str,
    error_message: str,
    language: str,
    student_id: str
) -> AnalysisResult:
    """
    Analyze error semantically using LangChain + AI
    """

    # 1. Fetch student context from database
    student = await prisma.user.find_unique(where={"id": student_id})

    error_history = await prisma.errorsubmission.find_many(
        where={"student_id": student_id},
        order={"created_at": "desc"},
        take=5
    )

    # 2. Build context string
    history_context = "\n".join([
        f"- {err.error_type}: {err.conceptual_gap}"
        for err in error_history
    ])

    # 3. Setup output parser
    parser = PydanticOutputParser(pydantic_object=AnalysisResult)

    # 4. Create prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert programming educator specializing in semantic error analysis.

Your task is to analyze programming errors from a CONCEPTUAL perspective, not just syntactical.
Focus on WHY the error occurred from a learning/understanding standpoint.

Identify:
- The conceptual gap (misconception) that led to this error
- Root cause from a learning theory perspective
- Bloom's Taxonomy level for explanation depth
- Related topics that need reinforcement

{format_instructions}"""),
        ("user", """Analyze this error SEMANTICALLY:

**Code:**
```{language}
{code}
````

**Error Message:**
{error_message}

**Student Context:**

- Proficiency Level: {proficiency_level}
- Recent Error History:
  {history_context}

Provide a deep conceptual analysis focusing on WHY this error occurred.""")
])

    # 5. Create chain
    llm = get_llm()
    chain = prompt | llm | parser

    # 6. Invoke chain
    result = await chain.ainvoke({
        "code": code,
        "error_message": error_message,
        "language": language,
        "proficiency_level": student.proficiency_level if student else "beginner",
        "history_context": history_context or "No previous errors",
        "format_instructions": parser.get_format_instructions()
    })

    # 7. Save to database
    await prisma.errorsubmission.create(
        data={
            "student_id": student_id,
            "code": code,
            "error_message": error_message,
            "language": language,
            "error_type": result.error_type,
            "root_cause": result.root_cause,
            "conceptual_gap": result.conceptual_gap,
            "bloom_level": result.bloom_level.value,
            "explanation": result.explanation,
            "fix_suggestion": result.fix_suggestion,
            "related_topics": result.related_topics,
            "practice_suggestion": result.practice_suggestion,
        }
    )

    # 8. Check for patterns (≥3 similar errors)
    similar_count = await prisma.errorsubmission.count(
        where={
            "student_id": student_id,
            "error_type": result.error_type
        }
    )

    if similar_count >= 3:
        result.pattern_alert = (
            f"⚠️ Pattern detected: You've encountered '{result.error_type}' "
            f"{similar_count} times. Consider reviewing: {', '.join(result.related_topics[:3])}"
        )
        result.similar_past_errors = similar_count

        # Update or create pattern record
        await prisma.errorpattern.upsert(
            where={
                "student_id_pattern_type": {
                    "student_id": student_id,
                    "pattern_type": result.error_type
                }
            },
            create={
                "student_id": student_id,
                "pattern_type": result.error_type,
                "frequency": similar_count,
                "first_occurrence": error_history[-1].created_at if error_history else None,
                "last_occurrence": None,  # Will be set by DB default
                "misconception_description": result.conceptual_gap,
                "recommended_resources": result.related_topics
            },
            update={
                "frequency": similar_count,
                "last_occurrence": None,  # Will be set by DB default
                "misconception_description": result.conceptual_gap
            }
        )

    return result

````

**6. API Routes**
```python
# app/routes/analyze.py
from fastapi import APIRouter, HTTPException
from app.models.schemas import AnalyzeRequest, AnalysisResult
from app.services.analysis_service import analyze_error_semantically

router = APIRouter()

@router.post("/", response_model=AnalysisResult)
async def analyze_error(request: AnalyzeRequest):
    """
    Analyze programming error semantically
    """
    try:
        result = await analyze_error_semantically(
            code=request.code,
            error_message=request.error_message,
            language=request.language,
            student_id=request.student_id
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
````

---

### 3. Database with Prisma

#### Prisma Schema

```prisma
// prisma/schema.prisma
generator client {
  provider = "prisma-client-py"
  interface = "asyncio"
}

datasource db {
  provider = "mongodb"
  url      = env("DATABASE_URL")
}

model User {
  id                String              @id @default(auto()) @map("_id") @db.ObjectId
  email             String              @unique
  nama              String?
  passwordHash      String              @map("password_hash")
  tingkatKemahiran  String              @default("pemula") @map("tingkat_kemahiran")
  createdAt         DateTime            @default(now()) @map("created_at")

  submisiError      SubmisiError[]
  polaError         PolaError[]
  progressBelajar   ProgressBelajar[]

  @@map("users")
}

model SubmisiError {
  id                 String    @id @default(auto()) @map("_id") @db.ObjectId
  idMahasiswa        String    @map("id_mahasiswa") @db.ObjectId
  kode               String
  pesanError         String    @map("pesan_error")
  bahasa             String    @default("python")
  tipeError          String?   @map("tipe_error")
  penyebabUtama      String?   @map("penyebab_utama")
  kesenjanganKonsep  String?   @map("kesenjangan_konsep")
  levelBloom         String?   @map("level_bloom")
  penjelasan         String?
  saranPerbaikan     String?   @map("saran_perbaikan")
  topikTerkait       String[]  @map("topik_terkait") @default([])
  saranLatihan       String?   @map("saran_latihan")
  createdAt          DateTime  @default(now()) @map("created_at")

  mahasiswa          User      @relation(fields: [idMahasiswa], references: [id], onDelete: Cascade)

  @@index([idMahasiswa])
  @@index([tipeError])
  @@map("submisi_error")
}

model PolaError {
  id                       String    @id @default(auto()) @map("_id") @db.ObjectId
  idMahasiswa              String    @map("id_mahasiswa") @db.ObjectId
  jenisKesalahan           String    @map("jenis_kesalahan")
  frekuensi                Int       @default(1)
  kejadianPertama          DateTime? @map("kejadian_pertama")
  kejadianTerakhir         DateTime? @default(now()) @map("kejadian_terakhir")
  deskripsiMiskonsepsi     String?   @map("deskripsi_miskonsepsi")
  sumberDayaDirekomendasikan String[] @map("sumber_daya_direkomendasikan") @default([])
  createdAt                DateTime  @default(now()) @map("created_at")
  updatedAt                DateTime  @updatedAt @map("updated_at")

  mahasiswa                User      @relation(fields: [idMahasiswa], references: [id], onDelete: Cascade)

  @@unique([idMahasiswa, jenisKesalahan])
  @@index([idMahasiswa])
  @@map("pola_error")
}

model ProgressBelajar {
  id                   String    @id @default(auto()) @map("_id") @db.ObjectId
  idMahasiswa          String    @map("id_mahasiswa") @db.ObjectId
  topik                String
  tingkatPenguasaan    Int       @default(0) @map("tingkat_penguasaan")
  jumlahErrorDiTopik   Int       @default(0) @map("jumlah_error_di_topik")
  tanggalErrorTerakhir DateTime? @map("tanggal_error_terakhir")
  trenPerbaikan        String?   @map("tren_perbaikan")
  createdAt            DateTime  @default(now()) @map("created_at")
  updatedAt            DateTime  @updatedAt @map("updated_at")

  mahasiswa            User      @relation(fields: [idMahasiswa], references: [id], onDelete: Cascade)

  @@index([idMahasiswa])
  @@map("progress_belajar")
}
```

#### Prisma Commands

```bash
# Generate Prisma Client
prisma generate

# Push schema to Azure Cosmos DB (no migrations for MongoDB)
prisma db push

# Open Prisma Studio
prisma studio
```

#### Using Prisma in Code

```python
# Example: Fetch user with relations
from app.database import prisma

async def get_user_with_history(user_id: str):
    user = await prisma.user.find_unique(
        where={"id": user_id},
        include={
            "errorSubmissions": {
                "take": 10,
                "order_by": {"created_at": "desc"}
            },
            "errorPatterns": True,
            "learningProgress": True
        }
    )
    return user
```

---

### 4. AI Integration Best Practices

#### Cost Optimization Strategies

**1. Use GitHub Models for Development (FREE)**

```python
# .env
USE_GITHUB_MODELS=true
GITHUB_TOKEN=your_github_token
```

**2. Implement Caching**

```python
from functools import lru_cache
import hashlib

@lru_cache(maxsize=1000)
def get_cached_analysis(code_hash: str, error_hash: str):
    """Cache identical code+error combinations"""
    # Check if we've seen this exact error before
    pass
```

**3. Rate Limiting**

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@router.post("/analyze")
@limiter.limit("10/minute")  # Max 10 requests per minute
async def analyze_error(request: Request, data: AnalyzeRequest):
    pass
```

**4. Token Management**

```python
# Use shorter prompts for GPT-3.5-turbo
# Use gpt-4o-mini instead of gpt-4 for cost savings
# Limit context window to recent 5 errors only
```

#### Prompt Engineering Best Practices

**1. Structured Output with Pydantic**

```python
from pydantic import BaseModel, Field

class AnalysisResult(BaseModel):
    error_type: str = Field(description="Category of error (e.g., 'Type Mismatch', 'Logic Error')")
    root_cause: str = Field(description="WHY error occurred from conceptual perspective")
    conceptual_gap: str = Field(description="Specific misconception or knowledge gap")
    # ... rest of fields
```

**2. Few-Shot Examples**

```python
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an expert programming educator.

Example 1:
Code: x = "5" + 3
Error: TypeError: can only concatenate str (not "int") to str
Analysis:
- Error Type: Type Mismatch
- Root Cause: Student doesn't understand that Python is strongly typed
- Conceptual Gap: Confusion between string concatenation and arithmetic
- Bloom Level: Understand (need to grasp type system)

Now analyze the following error:"""),
    ("user", "{input}")
])
```

**3. Bloom's Taxonomy Adaptation**

```python
async def get_bloom_level_explanation(
    base_explanation: str,
    student_level: str
) -> str:
    """Adapt explanation based on student's proficiency"""

    level_prompts = {
        "beginner": "Explain in very simple terms with concrete examples",
        "intermediate": "Explain with some technical depth and comparisons",
        "advanced": "Explain with abstractions and encourage exploration"
    }

    # Use separate LLM call to adapt explanation
    # This is optional - can be done in main analysis too
```

---

### 5. Deployment to Azure (Cost-Efficient)

#### Frontend Deployment (Azure Static Web Apps - FREE)

**1. Build Configuration**

```yaml
# .github/workflows/azure-static-web-apps.yml
name: Deploy Frontend

on:
  push:
    branches:
      - main

jobs:
  build_and_deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Build And Deploy
        uses: Azure/static-web-apps-deploy@v1
        with:
          azure_static_web_apps_api_token: ${{ secrets.AZURE_STATIC_WEB_APPS_API_TOKEN }}
          repo_token: ${{ secrets.GITHUB_TOKEN }}
          action: "upload"
          app_location: "frontend"
          output_location: ".next"
```

**2. staticwebapp.config.json**

```json
{
  "navigationFallback": {
    "rewrite": "/index.html"
  },
  "routes": [
    {
      "route": "/api/*",
      "allowedRoles": ["authenticated"]
    }
  ]
}
```

#### Backend Deployment (Azure Virtual Machine B1s)

Azure VM B1s adalah pilihan terbaik untuk budget $30-40/month karena:

- **Fixed price**: $7.59/month (predictable cost)
- **Full control**: No timeout, no cold start, no restrictions
- **Stable**: Reliable untuk production
- **Budget-friendly**: Paling murah untuk 24/7 operation

**Spesifikasi VM B1s:**

- 1 vCPU
- 1 GB RAM
- 4 GB temporary storage
- Cocok untuk low-medium traffic

**1. Create VM**

```bash
# Login to Azure
az login

# Create resource group
az group create --name pahamkode-rg --location southeastasia

# Create VM
az vm create \
  --resource-group pahamkode-rg \
  --name pahamkode-vm \
  --image Ubuntu2204 \
  --size Standard_B1s \
  --admin-username azureuser \
  --generate-ssh-keys \
  --public-ip-sku Standard

# Open port 8000
az vm open-port \
  --resource-group pahamkode-rg \
  --name pahamkode-vm \
  --port 8000 \
  --priority 1001
```

**2. requirements.txt**

```txt
fastapi==0.109.0
uvicorn[standard]==0.27.0
prisma==0.11.0
pydantic==2.5.3
python-dotenv==1.0.0
langchain==0.1.0
langchain-openai==0.0.2
supabase==2.3.0
```

**3. Setup Backend on VM**

**3. Setup Backend on VM**

```bash
# SSH into VM
ssh azureuser@<vm-public-ip>

# Install Python 3.11
sudo apt update
sudo apt install -y python3.11 python3.11-venv python3-pip

# Clone repository
git clone https://github.com/yourusername/pahamkode.git
cd pahamkode/backend

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Generate Prisma Client
prisma generate

# Create .env file
cat > .env << EOF
DATABASE_URL=postgresql://...
GITHUB_TOKEN=your_token
USE_GITHUB_MODELS=true
EOF

# Run with systemd (auto-restart on failure)
sudo nano /etc/systemd/system/pahamkode.service
```

**4. Systemd Service File**

```ini
[Unit]
Description=PahamKode FastAPI Backend
After=network.target

[Service]
Type=simple
User=azureuser
WorkingDirectory=/home/azureuser/pahamkode/backend
Environment="PATH=/home/azureuser/pahamkode/backend/venv/bin"
ExecStart=/home/azureuser/pahamkode/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**5. Start Service**

```bash
# Enable and start service
sudo systemctl enable pahamkode
sudo systemctl start pahamkode

# Check status
sudo systemctl status pahamkode

# View logs
sudo journalctl -u pahamkode -f
```

**6. Setup Nginx Reverse Proxy (Optional but Recommended)**

```bash
# Install Nginx
sudo apt install -y nginx

# Configure Nginx
sudo nano /etc/nginx/sites-available/pahamkode
```

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/pahamkode /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

#### AI Model Deployment (Optional - Llama 3.1 70B)

Jika ingin menggunakan Llama 3.1 70B untuk cost-efficiency maksimal dengan quality tinggi:

**1. Deploy Llama 3.1 70B via Azure AI Model Catalog**

```bash
# Login to Azure
az login

# Create Azure ML workspace (if not exists)
az ml workspace create \
  --name pahamkode-ml \
  --resource-group pahamkode-rg \
  --location southeastasia

# Deploy Llama 3.1 70B Instruct
az ml online-deployment create \
  --name llama-3-1-70b-instruct \
  --endpoint-name pahamkode-llama \
  --model azureml://registries/azureml-meta/models/Meta-Llama-3.1-70B-Instruct/versions/1 \
  --instance-type Standard_NC24ads_A100_v4 \
  --instance-count 1
```

**2. Get Endpoint URL & Key**

```bash
# Get scoring URL
az ml online-endpoint show \
  --name pahamkode-llama \
  --resource-group pahamkode-rg \
  --query scoring_uri -o tsv

# Get API key
az ml online-endpoint get-credentials \
  --name pahamkode-llama \
  --resource-group pahamkode-rg
```

**3. Update Backend .env**

```bash
# Add to .env
USE_LLAMA=true
LLAMA_ENDPOINT_URL=https://pahamkode-llama.southeastasia.inference.ml.azure.com/score
LLAMA_API_KEY=your_llama_endpoint_key
```

**4. Cost Management untuk Llama 3.1 70B**

```python
# Implement auto-stop untuk hemat biaya
# Stop endpoint saat tidak digunakan (off-peak hours)

# Schedule dengan Azure Automation:
# - Start: 8 AM (sebelum traffic)
# - Stop: 10 PM (setelah traffic)
# Hemat ~12 jam/hari = 50% cost reduction!
```

**Llama 3.1 70B Pricing:**

- **Hosting**: ~$10-15/month (dengan auto-stop strategy)
- **Inference**: $0.000264/1K tokens
- **Total for 10K requests**: ~$11.32-16.32/month
- **Total for 100K requests**: ~$23.20-28.20/month

---

**Cost Summary untuk Azure VM B1s:**

| Item                         | Monthly Cost          | Notes                        |
| ---------------------------- | --------------------- | ---------------------------- |
| **Azure VM B1s**             | $7.59                 | Fixed price, 24/7 operation  |
| **GitHub Models (AI)**       | $0                    | Free with rate limits        |
| **Llama 3.1 70B (optional)** | $10-15                | Powerful & cheap alternative |
| **Azure Static Web Apps**    | $0                    | Frontend hosting             |
| **Azure Cosmos DB**          | $0                    | Free tier (1000 RU/s, 25GB)  |
| **Azure OpenAI (optional)**  | $10-20                | Premium option               |
| **Total**                    | **$7.59-27.59/month** | Well within $30-40 budget!   |

**Benefits of This Setup:**

- ✅ Predictable fixed cost
- ✅ No surprise bills
- ✅ Stable and reliable
- ✅ Full control over environment
- ✅ No timeout or cold start issues
- ✅ Room in budget for AI tokens

**Remaining Budget:**

- Dengan VM $7.59, masih ada $22-32 untuk:
  - Azure OpenAI tokens jika perlu
  - Domain custom
  - Future scaling
  - Development tools

---

## Key Development Principles

### 1. Type Safety Everywhere

- **Frontend**: TypeScript strict mode, Zod validation
- **Backend**: Python type hints, Pydantic models
- **Database**: Prisma schema with type generation

### 2. Cost Optimization

- **AI**: Prioritize GitHub Models (free) over Azure OpenAI
- **Deployment**: Use Azure free tiers
- **Database**: Azure Cosmos DB free tier (1000 RU/s, 25GB - sufficient for development & moderate traffic)
- **Caching**: Implement aggressive caching for repeated queries

### 3. Error Handling

```python
# Backend
@router.post("/analyze")
async def analyze_error(request: AnalyzeRequest):
    try:
        result = await analyze_error_semantically(...)
        return result
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Analysis failed",
                "message": str(e),
                "fallback": "Please try again or contact support"
            }
        )
```

```typescript
// Frontend
try {
  const result = await analyzeError(data);
  setAnalysis(result);
} catch (error) {
  toast.error(
    error instanceof Error
      ? error.message
      : "Analysis failed. Please try again."
  );
}
```

### 4. Authentication Flow

```typescript
// Frontend: JWT-based Auth via Backend API
import { login, register, logout, ambilToken } from "@/lib/auth";

export function LoginForm() {
  async function handleLogin(email: string, password: string) {
    const response = await login(email, password);

    // Token sudah disimpan otomatis oleh login()
    // User data tersedia di response.user
    console.log("Logged in as:", response.user.email);
  }
}

// Untuk authenticated requests
const token = ambilToken();
const response = await fetch(`${API_URL}/api/analyze`, {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    Authorization: `Bearer ${token}`,
  },
  body: JSON.stringify(data),
});
```

---

## Environment Variables

### Frontend (.env.local)

```bash
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Backend (.env)

```bash
# Database - Azure Cosmos DB (MongoDB API)
DATABASE_URL=mongodb://pahamkode:your-password@pahamkode.mongo.cosmos.azure.com:10255/pahamkode-db?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000

# JWT Authentication
JWT_SECRET_KEY=your-super-secret-jwt-key-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# AI Provider - Llama 3.1 70B (RECOMMENDED)
USE_LLAMA=true
LLAMA_ENDPOINT_URL=https://pahamkode-llama.southeastasia.inference.ml.azure.com/score
LLAMA_API_KEY=your_llama_endpoint_key

# Alternative: GitHub Models (for development)
USE_GITHUB_MODELS=false
GITHUB_TOKEN=ghp_xxxxx

# Alternative: Azure OpenAI
USE_AZURE_OPENAI=false
AZURE_OPENAI_API_KEY=xxxxx
AZURE_OPENAI_ENDPOINT=https://xxxxx.openai.azure.com/

# CORS
FRONTEND_URL=https://pahamkode.com
```

---

## Testing Strategy

### Frontend Testing

```typescript
// __tests__/analyze.test.tsx
import { render, screen } from "@testing-library/react";
import { AnalyzePage } from "@/app/analyze/page";

test("renders code editor", () => {
  render(<AnalyzePage />);
  expect(screen.getByRole("textbox")).toBeInTheDocument();
});
```

### Backend Testing

```python
# tests/test_analysis.py
import pytest
from app.services.analysis_service import analyze_error_semantically

@pytest.mark.asyncio
async def test_semantic_analysis():
    result = await analyze_error_semantically(
        code='x = "5" + 3',
        error_message="TypeError: can only concatenate str",
        language="python",
        student_id="test-uuid"
    )

    assert result.error_type is not None
    assert "type" in result.root_cause.lower()
    assert result.bloom_level in ["Remember", "Understand", "Apply"]
```

---

## Performance Optimization

### 1. Database Query Optimization

```python
# Use select only needed fields
user = await prisma.user.find_unique(
    where={"id": user_id},
    select={
        "id": True,
        "proficiency_level": True
        # Don't fetch unnecessary fields
    }
)

# Use pagination for large lists
submissions = await prisma.errorsubmission.find_many(
    where={"student_id": user_id},
    take=20,
    skip=page * 20,
    order_by={"created_at": "desc"}
)
```

### 2. Frontend Optimization

```typescript
// Use dynamic imports for heavy components
const MonacoEditor = dynamic(() => import('@/components/editor/code-editor'), {
  ssr: false,
  loading: () => <Skeleton className="h-96" />
})

// Debounce API calls
import { useDebouncedCallback } from 'use-debounce'

const debouncedAnalyze = useDebouncedCallback(
  (code) => analyzeError({ code, ... }),
  1000
)
```

### 3. Caching Strategy

```python
from functools import lru_cache
import redis

# In-memory cache for frequent queries
@lru_cache(maxsize=100)
async def get_user_level(user_id: str) -> str:
    user = await prisma.user.find_unique(where={"id": user_id})
    return user.proficiency_level if user else "beginner"

# Redis cache for analysis results (optional)
# Only if you deploy Redis separately
```

---

## Security Best Practices

### 1. Authentication

```python
# Verify Supabase JWT in FastAPI
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
import jwt

security = HTTPBearer()

async def verify_token(credentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            settings.SUPABASE_JWT_SECRET,
            algorithms=["HS256"]
        )
        return payload["sub"]  # user_id
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Use in routes
@router.post("/analyze")
async def analyze(
    request: AnalyzeRequest,
    user_id: str = Depends(verify_token)
):
    # Ensure student_id matches authenticated user
    if request.student_id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")
```

### 2. Input Validation

```python
from pydantic import BaseModel, validator

class AnalyzeRequest(BaseModel):
    code: str
    error_message: str

    @validator('code')
    def validate_code_length(cls, v):
        if len(v) > 10000:  # Max 10K characters
            raise ValueError("Code too long")
        return v
```

### 3. Rate Limiting

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@router.post("/analyze")
@limiter.limit("10/minute")
async def analyze_error(request: Request, data: AnalyzeRequest):
    pass
```

---

## Monitoring & Logging

### 1. Structured Logging

```python
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

@router.post("/analyze")
async def analyze_error(request: AnalyzeRequest):
    start_time = datetime.now()

    try:
        result = await analyze_error_semantically(...)

        duration = (datetime.now() - start_time).total_seconds()
        logger.info(
            f"Analysis completed",
            extra={
                "student_id": request.student_id,
                "language": request.language,
                "duration_seconds": duration,
                "error_type": result.error_type
            }
        )

        return result
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}", exc_info=True)
        raise
```

### 2. Azure Application Insights (Optional)

```python
from opencensus.ext.azure.log_exporter import AzureLogHandler

logger.addHandler(
    AzureLogHandler(
        connection_string=settings.APPLICATIONINSIGHTS_CONNECTION_STRING
    )
)
```

---

## Code Generation Instructions

When generating code for PahamKode:

1. **Always use async/await** for database operations and AI calls
2. **Type everything** - TypeScript in frontend, type hints in backend
3. **Use Prisma** for all database operations (not raw SQL)
4. **Prefer GitHub Models** over Azure OpenAI for cost efficiency
5. **Implement error handling** at every layer
6. **Add logging** for debugging and monitoring
7. **Follow REST conventions** for API routes
8. **Use Server Components** in Next.js when possible
9. **Validate inputs** with Pydantic (backend) and Zod (frontend)
10. **Comment complex logic** especially in AI prompts and chains

---

## Common Tasks Quick Reference

### Add New AI Analysis Feature

1. Define Pydantic schema in `app/models/schemas.py`
2. Create prompt template in `app/utils/prompts.py`
3. Implement service function in `app/services/`
4. Add API route in `app/routes/`
5. Create frontend UI component
6. Add API call in frontend `lib/api-client.ts`

### Add New Database Table

1. Update `prisma/schema.prisma`
2. Run `prisma migrate dev --name add_table_name`
3. Run `prisma generate`
4. Use new model in Python with `await prisma.tablename.create(...)`

### Optimize Costs

1. Switch to GitHub Models: Set `USE_GITHUB_MODELS=true`
2. Implement caching for repeated queries
3. Add rate limiting to prevent abuse
4. Use smaller AI models (gpt-4o-mini vs gpt-4)
5. Limit context window size in prompts

---

## Research Considerations

### Data Collection for Evaluation

```python
# Track metrics for research paper
class AnalysisMetrics(BaseModel):
    analysis_id: int
    response_time_ms: float
    token_count: int
    expert_rating: float | None = None  # For validation
    student_feedback: int | None = None  # 1-5 rating

# Store in separate table for analysis
await prisma.analysismetrics.create(data={
    "analysis_id": submission.id,
    "response_time_ms": duration * 1000,
    "token_count": len(result.explanation.split())
})
```

### A/B Testing Support

```python
# Randomly assign students to control/experimental group
import random

async def assign_experiment_group(user_id: str) -> str:
    # Consistent assignment based on user_id hash
    return "experimental" if hash(user_id) % 2 == 0 else "control"
```

---

## Questions to Ask When Stuck

1. **Is this the most cost-efficient approach?**
2. **Am I using the right Azure tier (free vs paid)?**
3. **Have I implemented proper error handling?**
4. **Is this type-safe?**
5. **Can this be cached?**
6. **Does this need authentication?**
7. **Is this query optimized?**
8. **Have I logged important events?**
9. **Can this use Server Components instead of Client Components?**
10. **Is the prompt token-efficient?**

---

## Additional Resources

- **Prisma Docs**: https://prisma.io/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **Next.js 14 Docs**: https://nextjs.org/docs
- **LangChain Docs**: https://python.langchain.com/docs/get_started/introduction
- **GitHub Models**: https://github.com/marketplace/models
- **Supabase Docs**: https://supabase.com/docs
- **Azure Free Services**: https://azure.microsoft.com/free

---

**Remember**: This project prioritizes **semantic understanding over syntactic fixes**, **cost-efficiency over performance**, and **educational value over convenience**. Every feature should help students understand _why_ errors occur, not just _how_ to fix them.
