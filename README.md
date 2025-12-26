# PahamKode - Analisis Semantik Error Pemrograman

Sistem berbasis AI untuk menganalisis error pemrograman dari sudut pandang **konseptual dan semantik**, bukan hanya sintaks.

## ✅ Status: ARSITEKTUR BARU - STREAMLIT FULLSTACK!

✅ **Framework** - Streamlit (Fullstack Python)  
✅ **Database** - PyMongo + Azure Cosmos DB (MongoDB API)  
✅ **AI Provider** - **GitHub Models (FREE!)**  
✅ **Authentication** - Session-based Auth  
✅ **Deployment** - Single app di Azure VM B1s  
✅ **Type Safety** - Python type hints + pyright **PASSED!**

**Arsitektur Baru**: Streamlit (Frontend + Backend dalam satu app) + PyMongo (native MongoDB)

📄 Dokumentasi lengkap di [.github/copilot-instructions.md](.github/copilot-instructions.md)

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- pip (Python package manager)
- Azure Cosmos DB account (Free tier)

### Setup & Run

```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env dengan credentials Anda:
# - DATABASE_URL (Cosmos DB connection string)
# - GITHUB_TOKEN (dari https://github.com/settings/tokens)
# - USE_GITHUB_MODELS=true

# Run Streamlit app
streamlit run app/main.py
```

App akan buka di browser: **http://localhost:8501**

📘 **Tutorial lengkap**: [GITHUB_MODELS_SETUP.md](GITHUB_MODELS_SETUP.md)

### Testing

```bash
# Python type check
pyright app/  # ✅ PASS

# Run tests (optional)
pytest tests/ -v
```

---

## 🎯 Core Objectives

1. **Semantic Error Analysis** - Analisis error secara konseptual (MENGAPA error terjadi)
2. **Pattern Mining** - Identifikasi pola kesalahan berulang mahasiswa
3. **Adaptive Explanation** - Penjelasan disesuaikan dengan Bloom's Taxonomy
4. **Personalized Learning** - Rekomendasi pembelajaran yang dipersonalisasi

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│      STREAMLIT APP (Fullstack Python)              │
│  Frontend + Backend dalam satu aplikasi             │
│  - UI: Streamlit components                        │
│  - AI: LangChain + GitHub Models (FREE!)           │
│  - Auth: Session-based authentication              │
│  Deployed on: Azure VM B1s ($7.59/month)           │
└─────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────┐
│          DATABASE (Azure Cosmos DB)                 │
│  PyMongo + MongoDB API (FREE TIER)                  │
│  1000 RU/s, 25GB Storage                           │
└─────────────────────────────────────────────────────┘
```

## 💰 Estimasi Biaya

**Recommended Setup (GitHub Models - FREE!):**

| Service                   | Tier/SKU          | Biaya/Bulan        |
| ------------------------- | ----------------- | ------------------ |
| **Azure Cosmos DB**       | Free Tier         | **$0**             |
| **Azure VM B1s**          | 1 vCPU, 1GB RAM   | **$7.59**          |
| **VM Disk (HDD)**         | Standard HDD 30GB | **$1.54**          |
| **GitHub Models (AI)**    | FREE              | **$0**             |
| **Azure Static Web Apps** | Free Tier         | **$0**             |
| **Total**                 |                   | **$9.13/bulan** ✅ |

**🎉 Hemat 70%+ dengan GitHub Models!** (vs Llama $240+/bulan)

### Capacity

- **GitHub Models**: 15 req/min, 150K tokens/day (~9K requests/month)
- **Perfect untuk**: Student projects, development, low-medium traffic (<10K users)
- **Upgrade path**: Azure OpenAI jika traffic meningkat (~$1.88/10K requests)

📘 **Tutorial lengkap**: [GITHUB_MODELS_SETUP.md](GITHUB_MODELS_SETUP.md)

**Development Setup (GitHub Models - GRATIS):**

- Azure VM B1s: $7.59/bulan
- GitHub Models: $0/bulan (FREE!)
- **Total: $7.59/bulan** ✅

## Prerequisites

- Python 3.11+
- pip (Python package manager)
- Azure Cosmos DB account (Free tier)
- GitHub account (untuk GitHub Models - FREE AI)

### Backend Setup

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env dengan konfigurasi Anda

# Generate Prisma Client
prisma generate

# Push schema ke database
prisma db push

# Run server
uvicorn app.main:app --reload --port 8000
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Setup environment variables
cp .env.local.example .env.local
# Edit .env.local dengan konfigurasi Anda

# Run development server
npm run dev
```

Buka browser: http://localhost:3000

## 📁 Project Structure

```
PahamKode/
├── .github/
│   └── copilot-instructions.md    # Development guide
├── app/
│   ├── main.py                    # Streamlit entry point (landing page)
│   ├── config.py                  # Environment & settings
│   ├── database/
│   │   ├── koneksi.py             # PyMongo connection
│   │   ├── models.py              # MongoDB schemas (dataclasses)
│   │   └── queries.py             # Database operations
│   ├── services/
│   │   ├── ai_service.py          # GitHub Models integration
│   │   ├── analisis_service.py    # Semantic analysis
│   │   ├── pola_service.py        # Pattern mining
│   │   └── autentikasi_service.py # Session-based auth
│   ├── pages/
│   │   ├── 1_🔍_Analisis.py       # Analysis page (main feature)
│   │   ├── 2_📜_Riwayat.py        # History page
│   │   ├── 3_📊_Pola.py           # Patterns page
│   │   └── 4_📈_Progress.py       # Progress dashboard
│   ├── components/
│   │   ├── sidebar.py             # Navigation sidebar
│   │   ├── autentikasi.py         # Login/register forms
│   │   └── visualisasi.py         # Charts & graphs
│   └── utils/
│       ├── prompts.py             # LangChain prompts
│       ├── keamanan.py            # Password hashing
│       └── helpers.py             # Utility functions
├── prisma/
│   └── schema.prisma              # DEPRECATED (reference only)
├── requirements.txt               # Python dependencies
├── .env                           # Environment variables
└── README.md                      # This file
```

## ✅ Features Implemented

### Core Application

- ✅ Streamlit fullstack app (frontend + backend dalam satu)
- ✅ PyMongo integration dengan Azure Cosmos DB
- ✅ AI Service dengan LangChain + GitHub Models (FREE!)
- ✅ Session-based authentication
- ✅ Type-safe dengan Python type hints

### Pages

- ✅ Landing page dengan feature showcase
- ✅ Analysis page dengan code editor (streamlit-ace)
- ✅ Real-time semantic error analysis
- ✅ History page dengan submisi listing
- ✅ Patterns page dengan visualization (charts)
- ✅ Progress dashboard per topik

### Services

- ✅ Semantic Error Analysis service
- ✅ Pattern Mining service (deteksi pola ≥3x)
- ✅ Adaptive explanation (Bloom's Taxonomy)
- ✅ Personalized learning recommendations

## 🧪 Testing

### Backend Type Checking

```bash
cd backend
pyright app/
```

### Frontend Type Checking

```bash
cd frontend
npx tsc --noEmit
```

## 📖 Syarat Pengembangan

✅ **Bahasa**: Full Bahasa Indonesia untuk:

- Nama variabel dan function
- String, comments, dan dokumentasi
- (Kecuali nama file dan library eksternal)

✅ **Code Quality**:

- Best practices & design patterns
- Readable, clean, maintainable
- Scalable, reliable, simple
- Type-safe (TypeScript + Python type hints)

## 🔐 Environment Variables

### .env (Root Directory)

```bash
# Database - Azure Cosmos DB (MongoDB API)
DATABASE_URL=mongodb://pahamkode-cosmos:xxxxx@pahamkode-cosmos.mongo.cosmos.azure.com:10255/pahamkode-db?ssl=true&retrywrites=false&replicaSet=globaldb

# JWT Authentication
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# AI Provider - GitHub Models (FREE!)
USE_GITHUB_MODELS=true
GITHUB_TOKEN=ghp_xxxxx
GITHUB_MODEL_NAME=gpt-4o-mini

# Alternative: Azure OpenAI (if needed)
USE_AZURE_OPENAI=false
AZURE_OPENAI_API_KEY=xxxxx
AZURE_OPENAI_ENDPOINT=https://xxxxx.openai.azure.com/

# Application Settings
ENVIRONMENT=development
LOG_LEVEL=INFO
```

## 🚧 Roadmap

- [ ] Authentication dengan Supabase Auth
- [ ] History page untuk riwayat submisi
- [ ] Patterns page dengan visualization
- [ ] Progress dashboard per topik
- [ ] Export hasil analisis (PDF)
- [ ] Integration dengan IDE (VS Code extension)

## 📚 Documentation

Untuk dokumentasi lengkap tentang pengembangan, architecture, dan deployment, lihat:

- [Copilot Instructions](.github/copilot-instructions.md) - Comprehensive development guide
- [Project Explanation](docs/explanation.md) - Detailed project documentation

## 👥 Contributors

- Mikhael Sugianto

## 📄 License

MIT License

---

**PahamKode** - Memahami error dari perspektif konseptual 🧠
