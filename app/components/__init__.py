"""
Package components untuk PahamKode
Mengelola UI components yang reusable
"""

from .sidebar import render_sidebar
from .autentikasi import render_login_page, render_register_page
from .visualisasi import render_grafik_pola, render_grafik_progress

__all__ = [
    "render_sidebar",
    "render_login_page",
    "render_register_page",
    "render_grafik_pola",
    "render_grafik_progress",
]
