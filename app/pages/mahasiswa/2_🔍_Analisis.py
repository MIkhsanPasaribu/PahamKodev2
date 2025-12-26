"""
Mahasiswa - Analisis Error (MAIN FEATURE)

CRITICAL MAHASISWA FEATURE 🟡
- Code editor dengan syntax highlighting
- Real-time semantic error analysis
- AI-powered explanations
- Personalized recommendations
"""

import streamlit as st
from streamlit_ace import st_ace
from datetime import datetime
import logging

from app.components.sidebar import render_sidebar
from app.services.analisis_service import proses_analisis_error, ambil_rekomendasi_belajar
from app.services.autentikasi_service import is_mahasiswa
from app.utils.helpers import capitalize_first

logger = logging.getLogger(__name__)


# ==================== PAGE CONFIG ====================

st.set_page_config(
    page_title="Analisis Error - PahamKode",
    page_icon="🔍",
    layout="wide"
)


# ==================== AUTHENTICATION CHECK ====================

if "pengguna" not in st.session_state or st.session_state.pengguna is None:
    st.error("❌ Anda harus login terlebih dahulu!")
    st.stop()

if not is_mahasiswa(st.session_state.pengguna):
    st.error("❌ Halaman ini hanya untuk Mahasiswa.")
    st.stop()


# ==================== SIDEBAR ====================

render_sidebar()


# ==================== SESSION STATE ====================

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

if "show_recommendations" not in st.session_state:
    st.session_state.show_recommendations = False


# ==================== MAIN PAGE ====================

st.title("🔍 Analisis Error Semantik")
st.markdown("""
Analisis error pemrograman secara **konseptual** - bukan hanya sintaks, tapi **MENGAPA** error terjadi.
""")

pengguna = st.session_state.pengguna
queries = st.session_state.queries
id_mahasiswa = str(pengguna["_id"])

st.markdown("---")


# ==================== INPUT SECTION ====================

col1, col2 = st.columns([7, 3])

with col2:
    st.markdown("### ⚙️ Pengaturan")
    
    bahasa = st.selectbox(
        "Bahasa Pemrograman",
        options=["python", "javascript", "java", "cpp", "csharp"],
        format_func=lambda x: {
            "python": "Python",
            "javascript": "JavaScript",
            "java": "Java",
            "cpp": "C++",
            "csharp": "C#"
        }[x],
        key="bahasa_pemrograman"
    )
    
    # Language mode mapping for ace editor
    ace_mode = {
        "python": "python",
        "javascript": "javascript",
        "java": "java",
        "cpp": "c_cpp",
        "csharp": "csharp"
    }.get(bahasa, "python")
    
    st.markdown("---")
    
    st.markdown("### 💡 Panduan")
    
    st.info("""
    **Cara Menggunakan:**
    1. Paste kode Anda di editor
    2. Paste error message
    3. Klik "Analisis Error"
    4. Tunggu analisis AI
    5. Pelajari penjelasan konseptual
    """)

with col1:
    st.markdown("### 💻 Kode Anda")
    
    # Code editor with syntax highlighting
    kode = st_ace(
        placeholder="Paste kode Anda di sini...",
        language=ace_mode,
        theme="monokai",
        keybinding="vscode",
        font_size=14,
        tab_size=4,
        show_gutter=True,
        show_print_margin=False,
        wrap=True,
        auto_update=True,
        readonly=False,
        min_lines=15,
        max_lines=30,
        key="code_editor"
    )
    
    st.markdown("### ❌ Error Message")
    
    pesan_error = st.text_area(
        "Paste error message di sini",
        height=100,
        placeholder="Contoh: TypeError: can only concatenate str (not \"int\") to str",
        key="error_message"
    )

st.markdown("---")


# ==================== ANALYZE BUTTON ====================

col1, col2, col3 = st.columns([3, 3, 4])

with col1:
    analyze_button = st.button(
        "🔍 Analisis Error",
        use_container_width=True,
        type="primary"
    )

with col2:
    if st.button("🗑️ Clear", use_container_width=True):
        st.session_state.analysis_result = None
        st.session_state.show_recommendations = False
        st.rerun()


# ==================== ANALYSIS PROCESS ====================

if analyze_button:
    if not kode or not pesan_error:
        st.error("❌ Kode dan error message harus diisi!")
    else:
        with st.spinner("🤖 Menganalisis error secara semantik... Mohon tunggu."):
            try:
                # Process semantic analysis (returns tuple)
                submisi, pattern_alert = proses_analisis_error(
                    queries=queries,
                    id_mahasiswa=id_mahasiswa,
                    kode=kode,
                    pesan_error=pesan_error,
                    bahasa=bahasa
                )
                
                # Check if analysis successful
                if submisi:
                    # Convert SubmisiError to dict untuk UI
                    hasil = submisi.to_dict()
                    
                    # Add pattern alert if any
                    if pattern_alert:
                        hasil["pattern_alert"] = pattern_alert
                    
                    st.session_state.analysis_result = hasil
                    st.session_state.show_recommendations = True
                    st.success("✅ Analisis selesai!")
                else:
                    st.error("❌ Analisis gagal. Silakan coba lagi.")
                
            except Exception as e:
                logger.error(f"Error during analysis: {e}")
                st.error(f"❌ Error saat analisis: {str(e)}")


# ==================== ANALYSIS RESULTS ====================

if st.session_state.analysis_result:
    hasil = st.session_state.analysis_result
    
    st.markdown("---")
    st.markdown("## 📊 Hasil Analisis")
    
    
    # ==================== ERROR TYPE & BLOOM LEVEL ====================
    
    col1, col2 = st.columns(2)
    
    with col1:
        tipe_error = hasil.get("tipe_error", "Unknown")
        st.markdown(f"""
        <div style="background-color:#ef4444;color:white;padding:12px;border-radius:8px;text-align:center;">
            <h3 style="margin:0;">Tipe Error</h3>
            <h2 style="margin:8px 0 0 0;">{tipe_error}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        level_bloom = hasil.get("level_bloom", "Understand")
        bloom_color = {
            "Remember": "#6b7280",
            "Understand": "#3b82f6",
            "Apply": "#10b981",
            "Analyze": "#f59e0b",
            "Evaluate": "#f97316",
            "Create": "#ef4444"
        }.get(level_bloom, "#3b82f6")
        
        st.markdown(f"""
        <div style="background-color:{bloom_color};color:white;padding:12px;border-radius:8px;text-align:center;">
            <h3 style="margin:0;">Bloom's Taxonomy Level</h3>
            <h2 style="margin:8px 0 0 0;">{level_bloom}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    
    # ==================== ROOT CAUSE & CONCEPTUAL GAP ====================
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎯 Penyebab Utama")
        st.info(hasil.get("penyebab_utama", "N/A"))
    
    with col2:
        st.markdown("### 🧠 Kesenjangan Konsep")
        st.warning(hasil.get("kesenjangan_konsep", "N/A"))
    
    st.markdown("---")
    
    
    # ==================== EXPLANATION ====================
    
    st.markdown("### 📖 Penjelasan Konseptual")
    
    with st.expander("Lihat Penjelasan Lengkap", expanded=True):
        penjelasan = hasil.get("penjelasan", "N/A")
        st.markdown(penjelasan)
    
    st.markdown("---")
    
    
    # ==================== FIX SUGGESTION ====================
    
    st.markdown("### 💡 Saran Perbaikan")
    
    saran_perbaikan = hasil.get("saran_perbaikan", "N/A")
    
    st.code(saran_perbaikan, language=bahasa)
    
    st.markdown("---")
    
    
    # ==================== RELATED TOPICS ====================
    
    st.markdown("### 📚 Topik Terkait")
    
    topik_terkait = hasil.get("topik_terkait", [])
    
    if topik_terkait:
        # Display as tags
        tags_html = " ".join([
            f'<span style="background-color:#3b82f6;color:white;padding:6px 12px;border-radius:20px;margin:4px;display:inline-block;">{topic}</span>'
            for topic in topik_terkait
        ])
        
        st.markdown(tags_html, unsafe_allow_html=True)
    else:
        st.info("Tidak ada topik terkait.")
    
    st.markdown("---")
    
    
    # ==================== PRACTICE SUGGESTION ====================
    
    st.markdown("### ✏️ Saran Latihan")
    
    saran_latihan = hasil.get("saran_latihan", "N/A")
    
    st.success(saran_latihan)
    
    
    # ==================== PATTERN ALERT ====================
    
    if hasil.get("pattern_alert"):
        st.markdown("---")
        st.markdown("### ⚠️ Pattern Alert")
        
        st.warning(hasil["pattern_alert"])
        
        if st.button("📊 Lihat Pola Lengkap"):
            st.switch_page("pages/mahasiswa/4_📊_Pola.py")
    
    
    # ==================== RECOMMENDED RESOURCES ====================
    
    if st.session_state.show_recommendations:
        st.markdown("---")
        st.markdown("### 📖 Sumber Belajar yang Direkomendasikan")
        
        try:
            # Get recommended resources based on weak topics
            rekomendasi = ambil_rekomendasi_belajar(
                queries,
                id_mahasiswa,
                topik_terkait[:3] if topik_terkait else []
            )
            
            if rekomendasi:
                for resource in rekomendasi[:5]:
                    with st.container():
                        col_info, col_action = st.columns([8, 2])
                        
                        with col_info:
                            st.markdown(f"""
                            **{resource.get('judul', 'N/A')}** | 
                            <span style="background-color:#10b981;color:white;padding:2px 8px;border-radius:4px;font-size:12px;">{resource.get('tipe', 'N/A').upper()}</span>
                            """, unsafe_allow_html=True)
                            
                            st.caption(resource.get("deskripsi", "")[:150] + "...")
                        
                        with col_action:
                            url = resource.get("url", "#")
                            if url and url != "#":
                                st.link_button("🔗 Buka", url, use_container_width=True)
                        
                        st.markdown("---")
            else:
                st.info("Tidak ada rekomendasi saat ini. Lihat halaman Sumber Belajar untuk resources lengkap.")
        
        except Exception as e:
            logger.error(f"Error fetching recommendations: {e}")
            st.info("Lihat halaman Sumber Belajar untuk resources lengkap.")


# ==================== EXAMPLE SECTION ====================

if not st.session_state.analysis_result:
    st.markdown("---")
    st.markdown("## 💡 Contoh Error")
    
    tab_python, tab_js = st.tabs(["Python", "JavaScript"])
    
    with tab_python:
        st.markdown("### Contoh Python Error")
        
        st.code('''
# Kode dengan error
x = "5"
y = 3
hasil = x + y  # TypeError
print(hasil)
        ''', language="python")
        
        st.markdown("**Error Message:**")
        st.code('TypeError: can only concatenate str (not "int") to str')
    
    with tab_js:
        st.markdown("### Contoh JavaScript Error")
        
        st.code('''
// Kode dengan error
function calculateArea(radius) {
    return Math.PI * radius * radius;
}

let area = calculateArea();  // Error: radius is undefined
console.log(area);
        ''', language="javascript")
        
        st.markdown("**Error Message:**")
        st.code('NaN (Not a Number)')
