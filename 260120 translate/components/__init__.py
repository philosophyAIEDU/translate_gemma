"""
UI components for TranslateGemma Educator application.
"""

from .text_tab import render_text_tab
from .image_tab import render_image_tab
from .pdf_tab import render_pdf_tab
from .glossary_tab import render_glossary_tab
from .history_tab import render_history_tab

__all__ = [
    'render_text_tab',
    'render_image_tab',
    'render_pdf_tab',
    'render_glossary_tab',
    'render_history_tab',
]
