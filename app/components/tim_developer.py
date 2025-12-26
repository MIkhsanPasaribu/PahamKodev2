"""
Komponen Tim Pengembang - Reusable Developer Profile Components

CATATAN:
- Digunakan di halaman Tentang Tim dan sebagai footer di login/register
- Responsive design untuk mobile & desktop
- Mengintegrasikan foto developer dan social media links
"""

import streamlit as st
from typing import Dict, Any, Optional
from pathlib import Path


# ==================== CONSTANTS ====================

# Lokasi foto developer
FOTO_DEVELOPER_PATH = Path(__file__).parent.parent / "static" / "images" / "ikhsan.jpg"

# Info developer (define di sini untuk reusability)
DEVELOPER_INFO = {
    "nama": "M. Ikhsan Pasaribu",
    "nim": "23076039",
    "prodi": "Pendidikan Teknik Informatika",
    "foto": str(FOTO_DEVELOPER_PATH),
    "biodata": "Developer passionate tentang AI dan education technology. Fokus pada pengembangan sistem pembelajaran adaptif dengan AI untuk meningkatkan kualitas pendidikan pemrograman.",
    "social_media": {
        "github": {
            "url": "https://github.com/MIkhsanPasaribu",
            "icon": "🐙",
            "label": "GitHub"
        },
        "linkedin": {
            "url": "https://www.linkedin.com/in/mikhsanpasaribu",
            "icon": "💼",
            "label": "LinkedIn"
        },
        "instagram": {
            "url": "https://www.instagram.com/m.ikhsanp1/",
            "icon": "📸",
            "label": "Instagram"
        },
        "website": {
            "url": "https://mikhsanpasaribu.vercel.app/",
            "icon": "🌐",
            "label": "Website"
        }
    },
    "project": {
        "nama": "PahamKode",
        "deskripsi": "Sistem AI untuk Analisis Semantik Error Pemrograman",
        "repository": "https://github.com/MIkhsanPasaribu/PahamKodev2",
        "versi": "1.0.0",
        "description_long": "Platform berbasis AI yang menganalisis error pemrograman dari sudut pandang konseptual dan semantik. Bukan hanya memperbaiki syntax, tapi membantu mahasiswa memahami MENGAPA error terjadi melalui adaptive learning dengan Bloom's Taxonomy."
    }
}


# ==================== SOCIAL MEDIA LINKS COMPONENT ====================

def render_social_media_links(social_media: Dict[str, Dict[str, str]], size: str = "medium"):
    """
    Render tombol social media yang dapat diklik
    
    Args:
        social_media: Dict dengan informasi social media
        size: "small" (compact), "medium" (normal), "large" (prominent)
    """
    
    if not social_media:
        return
    
    # Layout kolom untuk social media buttons
    num_socials = len(social_media)
    cols = st.columns(num_socials)
    
    for idx, (platform, info) in enumerate(social_media.items()):
        with cols[idx]:
            # Button dengan custom styling
            button_text = f"{info['icon']} {info['label']}"
            
            if st.button(
                button_text,
                use_container_width=True,
                key=f"social_button_{platform}"
            ):
                st.markdown(f"[Membuka {info['label']}...]({info['url']})")


# ==================== DEVELOPER CARD COMPONENT ====================

def render_developer_card(developer_info: Dict[str, Any], compact: bool = False):
    """
    Render developer profile card dengan foto dan informasi
    
    Args:
        developer_info: Dict dengan informasi developer (dari DEVELOPER_INFO)
        compact: If True, tampilkan versi compact untuk footer
    """
    
    if compact:
        # Compact version untuk footer di login/register
        st.markdown("""
        ---
        ### 👨‍💻 Dikembangkan oleh
        """)
        
        col_text, col_links = st.columns([3, 1])
        
        with col_text:
            st.markdown(f"""
            **{developer_info['nama']}** - {developer_info['prodi']}
            
            {developer_info['biodata'][:100]}...
            """)
        
        with col_links:
            # Compact social media buttons
            for platform, info in developer_info['social_media'].items():
                st.markdown(
                    f"[{info['icon']}]({info['url']})",
                    help=info['label']
                )
            
            # Link ke halaman tim lengkap
            st.markdown("📖 [Lihat Profil Lengkap](./👥_Tentang_Tim)")
    
    else:
        # Full version untuk halaman Tentang Tim
        
        # Header
        st.title("👥 Tentang Tim Pengembang")
        st.markdown("---")
        
        # Developer card dengan 2 kolom: foto + info
        col_foto, col_info = st.columns([1, 2], gap="large")
        
        with col_foto:
            # Foto developer
            try:
                st.image(
                    developer_info['foto'],
                    use_column_width=True,
                    caption=developer_info['nama'],
                    width=250
                )
            except Exception as e:
                st.warning(f"⚠️ Tidak dapat memuat foto: {str(e)}")
                st.info("Foto developer tidak ditemukan")
        
        with col_info:
            # Informasi developer
            st.markdown(f"""
            ### {developer_info['nama']}
            
            **NIM**: {developer_info['nim']}  
            **Prodi**: {developer_info['prodi']}
            
            #### 📝 Biodata
            {developer_info['biodata']}
            """)
            
            # Social media links - full version
            st.markdown("#### 🔗 Terhubung Denganku")
            render_social_media_links(developer_info['social_media'], size="large")
        
        # Project information section
        st.markdown("---")
        st.markdown("### 📊 Tentang Proyek")
        
        project = developer_info['project']
        
        col_proj1, col_proj2 = st.columns(2)
        
        with col_proj1:
            st.markdown(f"""
            **Nama Proyek**: {project['nama']}
            
            **Versi**: {project['versi']}
            
            **Status**: ✅ Production Ready
            """)
        
        with col_proj2:
            st.markdown(f"""
            **Repository**: 
            [🔗 GitHub Link]({project['repository']})
            
            **Deskripsi**:
            {project['deskripsi']}
            """)
        
        # Detailed project description
        st.markdown("#### 🎯 Tentang PahamKode")
        st.info(project['description_long'])
        
        # Features section
        st.markdown("#### ✨ Fitur Utama")
        
        features = [
            ("🧠 Analisis Semantik", "Analisis error dari sudut pandang konseptual dan pemahaman"),
            ("🤖 AI-Powered", "Menggunakan LangChain + GitHub Models (AI gratis)"),
            ("📊 Pattern Mining", "Deteksi pola kesalahan berulang mahasiswa"),
            ("🎓 Bloom's Taxonomy", "Penjelasan disesuaikan dengan level kognitif"),
            ("💾 MongoDB", "Database scalable dengan Azure Cosmos DB"),
            ("⚡ Streamlit", "Fullstack Python framework untuk rapid development")
        ]
        
        col1, col2, col3 = st.columns(3)
        
        for idx, (feature_name, feature_desc) in enumerate(features):
            col = [col1, col2, col3][idx % 3]
            with col:
                st.markdown(f"**{feature_name}**")
                st.caption(feature_desc)
        
        # Tech stack
        st.markdown("#### 🛠️ Tech Stack")
        
        tech_col1, tech_col2, tech_col3 = st.columns(3)
        
        with tech_col1:
            st.markdown("""
            **Backend**
            - Python 3.11+
            - Streamlit 1.31
            - PyMongo
            """)
        
        with tech_col2:
            st.markdown("""
            **Database**
            - Azure Cosmos DB
            - MongoDB API
            - Free Tier
            """)
        
        with tech_col3:
            st.markdown("""
            **AI/ML**
            - LangChain
            - GitHub Models
            - GPT-4o-mini
            """)
        
        # Footer section
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: #666;">
        <p><small>
        Dibuat dengan ❤️ oleh M. Ikhsan Pasaribu
        <br/>
        Pendidikan Teknik Informatika - Universitas
        </small></p>
        </div>
        """, unsafe_allow_html=True)


# ==================== DEVELOPER INFO FOOTER ====================

def render_developer_info_footer():
    """
    Render footer dengan info developer untuk halaman login/register
    Compact version yang tidak terlalu prominent
    """
    
    render_developer_card(DEVELOPER_INFO, compact=True)


# ==================== EXPORT INFO ====================

def get_developer_info() -> Dict[str, Any]:
    """Get developer info dictionary untuk digunakan di tempat lain"""
    return DEVELOPER_INFO
