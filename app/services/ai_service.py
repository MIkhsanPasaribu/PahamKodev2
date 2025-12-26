"""
AI Service - LangChain Integration dengan GitHub Models (FREE!)

CATATAN: 
- Menggunakan GitHub Models untuk cost-efficiency (FREE tier)
- LangChain untuk prompt management & structured outputs
- Fallback ke Azure OpenAI jika perlu
"""

import os
from typing import Optional, Dict, Any
import logging
from langchain_openai import AzureChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from datetime import datetime

from app.config import settings

logger = logging.getLogger(__name__)


# ==================== STRUCTURED OUTPUT SCHEMAS ====================

class HasilAnalisis(BaseModel):
    """Schema untuk structured output dari AI analysis"""
    tipe_error: str = Field(description="Kategori error (e.g., 'Type Mismatch', 'Logic Error', 'Syntax Error')")
    penyebab_utama: str = Field(description="Root cause dari perspektif konseptual - MENGAPA error terjadi")
    kesenjangan_konsep: str = Field(description="Miskonsepsi atau knowledge gap spesifik yang menyebabkan error")
    level_bloom: str = Field(description="Bloom's Taxonomy level untuk penjelasan: Remember, Understand, Apply, Analyze, Evaluate, Create")
    penjelasan: str = Field(description="Penjelasan mendalam yang disesuaikan dengan Bloom level")
    saran_perbaikan: str = Field(description="Step-by-step solution dengan penjelasan konsep")
    topik_terkait: list[str] = Field(description="List topik yang perlu dipelajari/diperkuat")
    saran_latihan: str = Field(description="Rekomendasi latihan spesifik untuk memperkuat pemahaman")


# ==================== LLM INITIALIZATION ====================

def dapatkan_llm_github_models() -> AzureChatOpenAI:
    """
    Initialize LLM dengan GitHub Models (FREE!)
    
    Rate Limits:
    - 15 requests/minute per model
    - 150K tokens/day per model
    
    Models available:
    - gpt-4o-mini (recommended - fast & efficient)
    - gpt-4o (most capable)
    - phi-3-mini (Microsoft's model)
    """
    try:
        llm = AzureChatOpenAI(
            model="gpt-4o-mini",  # atau "gpt-4o" untuk quality lebih tinggi
            api_key=settings.GITHUB_TOKEN,
            azure_endpoint="https://models.inference.ai.azure.com",
            api_version="2024-02-01",
            temperature=0.3,  # Lower temperature untuk consistency
            max_tokens=2000,
            timeout=30,
        )
        logger.info("GitHub Models LLM initialized successfully")
        return llm
    except Exception as e:
        logger.error(f"Error initialize GitHub Models: {str(e)}")
        raise


def dapatkan_llm_azure_openai() -> AzureChatOpenAI:
    """
    Fallback: Initialize LLM dengan Azure OpenAI
    (Gunakan jika GitHub Models tidak tersedia)
    """
    try:
        llm = AzureChatOpenAI(
            model="gpt-4o-mini",
            api_key=settings.AZURE_OPENAI_API_KEY,
            azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
            api_version="2024-02-01",
            temperature=0.3,
            max_tokens=2000,
            timeout=30,
        )
        logger.info("Azure OpenAI LLM initialized successfully")
        return llm
    except Exception as e:
        logger.error(f"Error initialize Azure OpenAI: {str(e)}")
        raise


def dapatkan_llm() -> AzureChatOpenAI:
    """Auto-select LLM based on settings"""
    if settings.USE_GITHUB_MODELS:
        return dapatkan_llm_github_models()
    else:
        return dapatkan_llm_azure_openai()


# ==================== PROMPT TEMPLATES ====================

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


def buat_prompt_analisis_semantik() -> ChatPromptTemplate:
    """Buat prompt template untuk semantic error analysis"""
    parser = PydanticOutputParser(pydantic_object=HasilAnalisis)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT_SEMANTIC_ANALYSIS),
        ("user", USER_PROMPT_TEMPLATE)
    ])
    
    return prompt


# ==================== SEMANTIC ANALYSIS FUNCTION ====================

def analisis_error_semantik(
    kode: str,
    pesan_error: str,
    bahasa: str,
    tingkat_kemahiran: str,
    riwayat_error: list[Dict[str, Any]]
) -> Optional[HasilAnalisis]:
    """
    Analisis error secara semantik menggunakan LangChain + GitHub Models
    
    NOTE: This is synchronous function untuk compatibility dengan Streamlit
    
    Args:
        kode: Source code yang mengandung error
        pesan_error: Error message dari compiler/interpreter
        bahasa: Programming language (python, javascript, java, cpp)
        tingkat_kemahiran: Level mahasiswa (pemula, menengah, mahir)
        riwayat_error: Recent error history untuk konteks
    
    Returns:
        HasilAnalisis object dengan structured analysis
    """
    try:
        start_time = datetime.now()
        
        # 1. Initialize LLM
        llm = dapatkan_llm()
        
        # 2. Setup output parser
        parser = PydanticOutputParser(pydantic_object=HasilAnalisis)
        
        # 3. Create prompt
        prompt = buat_prompt_analisis_semantik()
        
        # 4. Format riwayat error untuk context
        riwayat_context = "\n".join([
            f"- {err.get('tipe_error', 'Unknown')}: {err.get('kesenjangan_konsep', 'N/A')}"
            for err in riwayat_error[:5]  # Ambil 5 terakhir saja
        ]) if riwayat_error else "Belum ada riwayat error"
        
        # 5. Create chain
        chain = prompt | llm | parser
        
        # 6. Invoke chain (synchronous untuk Streamlit compatibility)
        result: HasilAnalisis = chain.invoke({
            "kode": kode,
            "pesan_error": pesan_error,
            "bahasa": bahasa,
            "tingkat_kemahiran": tingkat_kemahiran,
            "riwayat_error": riwayat_context,
            "format_instructions": parser.get_format_instructions()
        })
        
        # 7. Calculate metrics
        end_time = datetime.now()
        waktu_respons = (end_time - start_time).total_seconds()
        
        logger.info(f"Semantic analysis completed in {waktu_respons:.2f}s")
        logger.info(f"Error type detected: {result.tipe_error}")
        logger.info(f"Bloom level: {result.level_bloom}")
        
        return result
        
    except Exception as e:
        logger.error(f"Error dalam analisis semantik: {str(e)}", exc_info=True)
        return None


# ==================== TOKEN COUNTING (untuk metrik) ====================

def hitung_token_estimasi(text: str) -> int:
    """
    Estimasi jumlah token (rough estimation)
    1 token ≈ 4 characters untuk English
    1 token ≈ 2-3 characters untuk Indonesian (lebih efisien)
    """
    return len(text) // 3


def hitung_biaya_estimasi(token_input: int, token_output: int, model: str = "gpt-4o-mini") -> float:
    """
    Hitung estimasi biaya AI call
    
    GitHub Models: FREE (no cost!)
    Azure OpenAI GPT-4o-mini:
    - Input: $0.00015/1K tokens
    - Output: $0.0006/1K tokens
    """
    if settings.USE_GITHUB_MODELS:
        return 0.0  # FREE!
    
    # Azure OpenAI pricing
    biaya_input = (token_input / 1000) * 0.00015
    biaya_output = (token_output / 1000) * 0.0006
    
    return biaya_input + biaya_output
