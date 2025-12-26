"""
Mahasiswa - Export Progress

MAHASISWA FEATURE (NEW) 🟡
- Export progress report
- PDF/CSV format
- Share dengan mentor/instructor
"""

import streamlit as st
import pandas as pd
import logging
from datetime import datetime, timedelta
from io import BytesIO

from app.components.sidebar import render_sidebar
from app.services.autentikasi_service import is_mahasiswa
from app.utils.helpers import format_datetime, format_percentage, format_number

logger = logging.getLogger(__name__)


# ==================== PAGE CONFIG ====================

st.set_page_config(
    page_title="Export Progress - PahamKode",
    page_icon="📄",
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


# ==================== MAIN PAGE ====================

st.title("📄 Export Progress Report")
st.markdown("Generate dan download laporan progress pembelajaran Anda")

pengguna = st.session_state.pengguna
queries = st.session_state.queries
id_mahasiswa = str(pengguna["_id"])

st.markdown("---")


# ==================== HELPER FUNCTIONS ====================

def _format_top_errors(errors: list) -> str:
    """Format top errors for display"""
    if not errors:
        return "- Tidak ada data"
    return "\n".join([f"- {tipe}: {count}x" for tipe, count in errors])


# ==================== REPORT OPTIONS ====================

st.markdown("### ⚙️ Konfigurasi Report")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Periode Report**")
    
    periode_option = st.radio(
        "Pilih Periode",
        options=["7 Hari Terakhir", "30 Hari Terakhir", "90 Hari Terakhir", "Semua Data", "Custom"],
        key="periode_option"
    )
    
    # Custom date range
    if periode_option == "Custom":
        tanggal_mulai = st.date_input("Tanggal Mulai", value=datetime.now() - timedelta(days=30))
        tanggal_akhir = st.date_input("Tanggal Akhir", value=datetime.now())
    else:
        tanggal_mulai = None
        tanggal_akhir = None

with col2:
    st.markdown("**Format Report**")
    
    report_type = st.radio(
        "Jenis Report",
        options=["Summary", "Detailed"],
        key="report_type"
    )
    
    export_format = st.radio(
        "Format File",
        options=["CSV", "PDF (Coming Soon)"],
        key="export_format"
    )

st.markdown("---")


# ==================== PREVIEW SECTION ====================

st.markdown("### 👀 Preview Report")

# Initialize variables BEFORE try block to avoid "possibly unbound" warnings
date_from = None
date_to = None
riwayat = []
pola = []
progress = []
total_submisi = 0
total_pola = 0
avg_penguasaan = 0.0
error_counts = {}
top_errors = []

try:
    # Determine date range
    if periode_option == "7 Hari Terakhir":
        date_from = datetime.now() - timedelta(days=7)
        date_to = datetime.now()
    elif periode_option == "30 Hari Terakhir":
        date_from = datetime.now() - timedelta(days=30)
        date_to = datetime.now()
    elif periode_option == "90 Hari Terakhir":
        date_from = datetime.now() - timedelta(days=90)
        date_to = datetime.now()
    elif periode_option == "Custom" and tanggal_mulai and tanggal_akhir:
        date_from = datetime.combine(tanggal_mulai, datetime.min.time())
        date_to = datetime.combine(tanggal_akhir, datetime.max.time())
    
    # Fetch data
    riwayat = queries.ambil_riwayat_submisi(id_mahasiswa, limit=1000)
    pola = queries.ambil_pola_mahasiswa(id_mahasiswa)
    progress = queries.ambil_progress_mahasiswa(id_mahasiswa)
    
    # Filter by date if needed
    if date_from and date_to:
        riwayat = [
            r for r in riwayat
            if date_from <= r.get("created_at", datetime.now()) <= date_to
        ]
    
    # Calculate stats
    total_submisi = len(riwayat)
    total_pola = len(pola)
    avg_penguasaan = sum(p.get("tingkat_penguasaan", 0) for p in progress) / len(progress) if progress else 0
    
    # Top errors
    error_counts = {}
    for r in riwayat:
        tipe = r.get("tipe_error", "Unknown")
        error_counts[tipe] = error_counts.get(tipe, 0) + 1
    
    top_errors = sorted(error_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Submisi", format_number(total_submisi, 0))
    
    with col2:
        st.metric("Pola Terdeteksi", format_number(total_pola, 0))
    
    with col3:
        st.metric("Rata-rata Penguasaan", format_percentage(avg_penguasaan, 100.0))
    
    with col4:
        st.metric("Topik Dipelajari", format_number(len(progress), 0))
    
    st.markdown("---")
    
    # Preview tables
    if report_type == "Detailed":
        st.markdown("#### 📊 Detail Progress per Topik")
        if progress:
            df_progress = pd.DataFrame([
                {
                    "Topik": p.get("topik", "N/A"),
                    "Penguasaan (%)": p.get("tingkat_penguasaan", 0),
                    "Jumlah Error": p.get("jumlah_error_di_topik", 0),
                    "Tren": p.get("tren_perbaikan", "N/A"),
                }
                for p in progress
            ])
            st.dataframe(df_progress, use_container_width=True)
        else:
            st.info("Tidak ada data progress.")
        
        st.markdown("#### 🔴 Top 10 Errors")
        if top_errors:
            df_errors = pd.DataFrame([
                {
                    "Tipe Error": tipe,
                    "Jumlah": count
                }
                for tipe, count in top_errors
            ])
            st.dataframe(df_errors, use_container_width=True)
        else:
            st.info("Tidak ada data errors.")
        
        st.markdown("#### 🔁 Pola Kesalahan Berulang")
        if pola:
            df_pola = pd.DataFrame([
                {
                    "Jenis Kesalahan": p.get("jenis_kesalahan", "N/A"),
                    "Frekuensi": p.get("frekuensi", 0),
                    "Kejadian Terakhir": format_datetime(p.get("kejadian_terakhir")),
                }
                for p in pola
            ])
            st.dataframe(df_pola, use_container_width=True)
        else:
            st.info("Tidak ada pola terdeteksi.")
    
    else:  # Summary
        st.markdown("#### 📋 Summary")
        st.info(f"""
        **Periode:** {format_datetime(date_from) if date_from else "Semua"} - {format_datetime(date_to) if date_to else "Sekarang"}
        
        **Overview:**
        - Total Submisi Error: {total_submisi}
        - Pola Terdeteksi: {total_pola}
        - Rata-rata Penguasaan: {avg_penguasaan:.1f}%
        - Topik Dipelajari: {len(progress)}
        
        **Top 3 Errors:**
        {_format_top_errors(top_errors[:3])}
        
        **Rekomendasi:**
        - Fokus pada topik dengan penguasaan < 60%
        - Review pola kesalahan berulang
        - Latihan konsisten untuk improvement
        """)


except Exception as e:
    logger.error(f"Error generating preview: {e}")
    st.error(f"❌ Error: {str(e)}")

st.markdown("---")


# ==================== GENERATE REPORT ====================

st.markdown("### 🚀 Generate & Download Report")

if st.button("📥 Generate Report", type="primary", use_container_width=True):
    
    if export_format == "CSV":
        try:
            # Generate CSV report
            with st.spinner("Generating CSV report..."):
                
                # Prepare data
                report_data = {
                    "Info Mahasiswa": {
                        "Nama": pengguna.get("nama", "N/A"),
                        "Email": pengguna.get("email", "N/A"),
                        "Tingkat Kemahiran": pengguna.get("tingkat_kemahiran", "N/A"),
                        "Report Generated": format_datetime(datetime.now()),
                        "Periode": f"{format_datetime(date_from) if date_from else 'Semua'} - {format_datetime(date_to) if date_to else 'Sekarang'}"
                    },
                    "Summary": {
                        "Total Submisi": total_submisi,
                        "Total Pola": total_pola,
                        "Rata-rata Penguasaan": f"{avg_penguasaan:.1f}%",
                        "Topik Dipelajari": len(progress)
                    }
                }
                
                # Create Excel file with multiple sheets
                output = BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    # Info sheet
                    df_info = pd.DataFrame([report_data["Info Mahasiswa"]]).T
                    df_info.columns = ["Value"]
                    df_info.to_excel(writer, sheet_name='Info')
                    
                    # Summary sheet
                    df_summary = pd.DataFrame([report_data["Summary"]]).T
                    df_summary.columns = ["Value"]
                    df_summary.to_excel(writer, sheet_name='Summary')
                    
                    # Progress sheet
                    if progress:
                        df_progress = pd.DataFrame([
                            {
                                "Topik": p.get("topik", "N/A"),
                                "Penguasaan (%)": p.get("tingkat_penguasaan", 0),
                                "Jumlah Error": p.get("jumlah_error_di_topik", 0),
                                "Tren": p.get("tren_perbaikan", "N/A"),
                            }
                            for p in progress
                        ])
                        df_progress.to_excel(writer, sheet_name='Progress', index=False)
                    
                    # Errors sheet
                    if top_errors:
                        df_errors = pd.DataFrame([
                            {"Tipe Error": tipe, "Jumlah": count}
                            for tipe, count in top_errors
                        ])
                        df_errors.to_excel(writer, sheet_name='Top Errors', index=False)
                    
                    # Pola sheet
                    if pola:
                        df_pola = pd.DataFrame([
                            {
                                "Jenis Kesalahan": p.get("jenis_kesalahan", "N/A"),
                                "Frekuensi": p.get("frekuensi", 0),
                                "Kejadian Terakhir": format_datetime(p.get("kejadian_terakhir")),
                                "Misconception": p.get("deskripsi_miskonsepsi", "N/A"),
                            }
                            for p in pola
                        ])
                        df_pola.to_excel(writer, sheet_name='Pola Kesalahan', index=False)
                
                output.seek(0)
                
                # Download button
                st.download_button(
                    label="📥 Download Excel Report",
                    data=output,
                    file_name=f"pahamkode_report_{pengguna.get('nama', 'mahasiswa')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
                
                st.success("✅ Report berhasil di-generate!")
        
        except Exception as e:
            logger.error(f"Error generating CSV: {e}")
            st.error(f"❌ Error generating report: {str(e)}")
    
    else:  # PDF
        st.warning("""
        **PDF Export Coming Soon!**
        
        Untuk saat ini, silakan gunakan format Excel/CSV.
        PDF export dengan visualisasi charts akan segera hadir.
        """)


        st.warning("""
        **PDF Export Coming Soon!**
        
        Untuk saat ini, silakan gunakan format Excel/CSV.
        PDF export dengan visualisasi charts akan segera hadir.
        """)


# ==================== INFO SECTION ====================

st.markdown("---")

st.info("""
### 💡 Tips Menggunakan Report

1. **Export secara berkala** untuk track progress jangka panjang
2. **Bagikan dengan mentor** untuk feedback dan guidance
3. **Review pola kesalahan** untuk identify improvement areas
4. **Gunakan Excel** untuk analisis lebih lanjut dengan pivot tables

**Format Excel includes:**
- 📊 Info Mahasiswa
- 📈 Summary Statistics
- 🎯 Progress per Topik
- 🔴 Top Errors
- 🔁 Pola Kesalahan Berulang
""")


# ==================== REFRESH ====================

if st.button("🔄 Refresh Data", use_container_width=True):
    st.rerun()
