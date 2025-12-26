"""
Prompts - LangChain Prompt Templates

CATATAN:
- Prompt templates untuk AI semantic analysis
- Disesuaikan untuk Bahasa Indonesia
- Terstruktur dengan format instructions
"""

from langchain.prompts import ChatPromptTemplate


# ==================== SYSTEM PROMPTS ====================

SYSTEM_PROMPT_SEMANTIC_ANALYSIS = """Kamu adalah asisten AI ahli dalam analisis error pemrograman secara SEMANTIK dan KONSEPTUAL.

Tugasmu adalah menganalisis error dari sudut pandang pembelajaran dan pemahaman konsep, BUKAN hanya dari perspektif teknis/sintaks.

FOKUS ANALISIS:
1. **Root Cause Konseptual** - MENGAPA error terjadi dari segi pemahaman mahasiswa
2. **Miskonsepsi** - Kesalahpahaman konsep apa yang menyebabkan error ini
3. **Bloom's Taxonomy** - Level kognitif yang tepat untuk penjelasan
4. **Pembelajaran Holistik** - Topik terkait yang perlu diperkuat

PENTING:
- Jangan hanya jelaskan "bagaimana" memperbaiki error
- Fokus pada "mengapa" error terjadi dan "apa" yang perlu dipahami
- Adaptasi penjelasan berdasarkan Bloom level
- Berikan rekomendasi pembelajaran yang actionable

Bloom's Taxonomy Levels:
- Remember: Mahasiswa perlu mengingat konsep dasar
- Understand: Mahasiswa perlu memahami konsep lebih dalam
- Apply: Mahasiswa perlu latihan menerapkan konsep
- Analyze: Mahasiswa perlu menganalisis hubungan antar konsep
- Evaluate: Mahasiswa perlu mengevaluasi pilihan solusi
- Create: Mahasiswa siap membuat implementasi kompleks

{format_instructions}"""


USER_PROMPT_TEMPLATE = """Analisis error ini secara SEMANTIK dan KONSEPTUAL:

**Kode yang Error:**
```{bahasa}
{kode}
```

**Pesan Error:**
{pesan_error}

**Konteks Mahasiswa:**
- Tingkat Kemahiran: {tingkat_kemahiran}
- Riwayat Error Terakhir (untuk konteks):
{riwayat_error}

**Instruksi Analisis:**
Berikan analisis mendalam yang berfokus pada:
1. Tipe error dan penyebab utama dari perspektif KONSEPTUAL
2. Miskonsepsi atau kesenjangan pemahaman yang menyebabkan error
3. Level Bloom yang tepat untuk penjelasan berdasarkan kemahiran mahasiswa
4. Penjelasan yang disesuaikan dengan level Bloom tersebut
5. Saran perbaikan yang edukatif, bukan hanya "fix the code"
6. Topik terkait yang perlu dipelajari/diperkuat
7. Rekomendasi latihan spesifik

PENTING: Penjelasan dalam Bahasa Indonesia yang mudah dipahami!"""


# ==================== PROMPT BUILDERS ====================

def buat_prompt_analisis_semantik() -> ChatPromptTemplate:
    """
    Buat prompt template untuk semantic error analysis
    
    Returns:
        ChatPromptTemplate untuk LangChain
    """
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT_SEMANTIC_ANALYSIS),
        ("user", USER_PROMPT_TEMPLATE)
    ])
    
    return prompt


# ==================== EXAMPLE PROMPTS (untuk testing) ====================

CONTOH_KODE_ERROR_PYTHON = """
def hitung_rata_rata(angka):
    total = 0
    for i in angka:
        total += i
    return total / 0  # Error: division by zero
"""

CONTOH_PESAN_ERROR_PYTHON = """
ZeroDivisionError: division by zero
"""

CONTOH_KODE_ERROR_JAVASCRIPT = """
function hitungTotal(arr) {
    let total = 0;
    for (let i = 0; i <= arr.length; i++) {
        total += arr[i];  // Error: undefined
    }
    return total;
}
"""

CONTOH_PESAN_ERROR_JAVASCRIPT = """
TypeError: Cannot read property of undefined
"""


# ==================== HELPER FUNCTIONS ====================

def format_riwayat_error(riwayat: list) -> str:
    """
    Format riwayat error untuk prompt
    
    Args:
        riwayat: List of error dictionaries
    
    Returns:
        Formatted string untuk prompt
    """
    if not riwayat:
        return "Belum ada riwayat error"
    
    formatted = []
    for i, err in enumerate(riwayat[:5], 1):  # Max 5 terakhir
        tipe = err.get("tipe_error", "Unknown")
        kesenjangan = err.get("kesenjangan_konsep", "N/A")
        formatted.append(f"{i}. {tipe}: {kesenjangan}")
    
    return "\n".join(formatted)


def estimasi_tingkat_kesulitan(tipe_error: str) -> str:
    """
    Estimasi tingkat kesulitan based on error type
    
    Args:
        tipe_error: Error type string
    
    Returns:
        Difficulty level: "mudah", "sedang", "sulit"
    """
    # Simple heuristic - could be improved with ML
    mudah_keywords = ["syntax", "typo", "indentation", "missing"]
    sedang_keywords = ["type", "attribute", "index", "key"]
    sulit_keywords = ["logic", "runtime", "recursion", "memory", "algorithm"]
    
    tipe_lower = tipe_error.lower()
    
    if any(keyword in tipe_lower for keyword in sulit_keywords):
        return "sulit"
    elif any(keyword in tipe_lower for keyword in sedang_keywords):
        return "sedang"
    else:
        return "mudah"
