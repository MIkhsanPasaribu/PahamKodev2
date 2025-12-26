"""
Halaman Tentang Tim Pengembang - PahamKode
Menampilkan informasi lengkap tentang tim developer dan proyek

Page: 9_👥_Tentang_Tim.py
Navigation: Sidebar → 👥 Tentang Tim
"""

import streamlit as st

from components.tim_developer import render_developer_card, DEVELOPER_INFO


# ==================== PAGE CONFIG ====================

st.set_page_config(
    page_title="Tentang Tim - PahamKode",
    page_icon="👥",
    layout="wide"
)


# ==================== SESSION CHECK ====================

def cek_session_state():
    """Cek apakah user sudah login"""
    if "pengguna" not in st.session_state:
        st.session_state.pengguna = None
    
    if "queries" not in st.session_state:
        st.error("❌ Session error. Silakan kembali ke landing page.")
        st.stop()


cek_session_state()


# ==================== MAIN CONTENT ====================

def tampilkan_halaman_tim():
    """Render halaman Tentang Tim lengkap"""
    
    # Render developer card dengan versi full (compact=False)
    render_developer_card(DEVELOPER_INFO, compact=False)
    
    # Additional info section
    st.markdown("---")
    st.markdown("### 📚 Sumber Daya & Dokumentasi")
    
    col_doc1, col_doc2, col_doc3 = st.columns(3)
    
    with col_doc1:
        st.markdown("""
        **📖 Dokumentasi**
        - [Setup Guide](./README.md)
        - [Copilot Instructions](./.github/copilot-instructions.md)
        - [Azure Setup](./AZURE_PORTAL_SETUP.md)
        """)
    
    with col_doc2:
        st.markdown("""
        **🔧 Teknis**
        - [Pyright Error Fixes](./PYRIGHT_ERROR_FIXES_REPORT.md)
        - [Rancangan Halaman Tim](./RANCANGAN_HALAMAN_TIM.md)
        - [GitHub Issues](https://github.com/MIkhsanPasaribu/PahamKodev2/issues)
        """)
    
    with col_doc3:
        st.markdown("""
        **🎓 Pembelajaran**
        - [Bloom's Taxonomy](https://en.wikipedia.org/wiki/Bloom%27s_taxonomy)
        - [Semantic Analysis](https://en.wikipedia.org/wiki/Semantic_analysis)
        - [LangChain Docs](https://python.langchain.com/)
        """)
    
    # Architecture section
    st.markdown("---")
    st.markdown("### 🏗️ Arsitektur Sistem")
    
    st.markdown("""
    #### Stack Teknologi
    
    **Frontend & Backend (Integrated)**
    - 🐍 Python 3.11+
    - 🎨 Streamlit 1.31 (Full-stack framework)
    - 💾 PyMongo (Native MongoDB driver)
    
    **Database**
    - 🗄️ Azure Cosmos DB (Free Tier)
    - 📊 MongoDB API
    - ⚡ 1000 RU/s, 25GB Storage
    
    **AI/ML**
    - 🤖 LangChain (Orchestration)
    - 🎯 GitHub Models (FREE!)
    - 💡 GPT-4o-mini (Primary model)
    
    **Authentication**
    - 🔐 Session-based (st.session_state)
    - 🔒 Bcrypt password hashing
    - 👤 Role-based access (Admin/Mahasiswa)
    
    **Deployment**
    - ☁️ Azure Virtual Machine B1s
    - 🌐 Port 8501 (Streamlit default)
    - ⚙️ systemd auto-restart
    """)
    
    # Cost breakdown
    st.markdown("---")
    st.markdown("### 💰 Estimasi Biaya Operasional")
    
    cost_data = {
        "Service": ["Azure Cosmos DB", "Azure VM B1s", "VM Disk (HDD)", "GitHub Models", "Total"],
        "Tier/SKU": ["Free Tier", "1 vCPU, 1GB RAM", "Standard HDD 30GB", "FREE", ""],
        "Biaya/Bulan": ["$0", "$7.59", "$1.54", "$0", "$9.13"]
    }
    
    st.table(cost_data)
    
    st.info("""
    ✨ **Hemat**: Total biaya produksi hanya **$9.13/bulan**! 
    
    Menggunakan **GitHub Models** (FREE) untuk AI inference menghemat biaya signifikan 
    dibanding Azure OpenAI atau service AI lainnya.
    """)
    
    # Feature roadmap
    st.markdown("---")
    st.markdown("### 🗺️ Feature Roadmap")
    
    roadmap = {
        "Feature": [
            "✅ Semantic Error Analysis",
            "✅ Pattern Mining (≥3x errors)",
            "✅ Bloom's Taxonomy Levels",
            "✅ Session-based Auth",
            "✅ AI Admin Dashboard",
            "🔄 Advanced Visualizations",
            "🔄 Mobile App (React Native)",
            "🔄 Collaborative Learning"
        ],
        "Status": [
            "Completed",
            "Completed",
            "Completed",
            "Completed",
            "Completed",
            "In Progress",
            "Planned",
            "Planned"
        ],
        "Timeline": [
            "v1.0",
            "v1.0",
            "v1.0",
            "v1.0",
            "v1.0",
            "v1.1",
            "v2.0",
            "v2.0"
        ]
    }
    
    st.table(roadmap)
    
    # Contact & Support
    st.markdown("---")
    st.markdown("### 💬 Kontak & Support")
    
    st.markdown("""
    Punya pertanyaan atau ingin berkontribusi? Hubungi melalui:
    
    - 📧 **Email**: Gunakan link GitHub atau LinkedIn untuk menghubungi
    - 🐙 **GitHub**: Buka [issue](https://github.com/MIkhsanPasaribu/PahamKodev2/issues) 
      atau submit pull request
    - 💼 **LinkedIn**: Connect dan message
    - 🌐 **Website**: Kunjungi portfolio pribadi untuk info lebih lanjut
    """)


# ==================== EXECUTE ====================

tampilkan_halaman_tim()
