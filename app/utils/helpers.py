"""
Helpers - Utility Functions

CATATAN:
- Format helpers (date, numbers, etc.)
- Validation helpers
- Common operations
"""

import logging
from datetime import datetime, timedelta
from typing import Any, Optional, Dict, List
import re

logger = logging.getLogger(__name__)


# ==================== DATE/TIME HELPERS ====================

def format_datetime(dt: datetime, format_type: str = "full") -> str:
    """
    Format datetime untuk display
    
    Args:
        dt: datetime object
        format_type: "full", "date", "time", "relative"
    
    Returns:
        Formatted date string
    """
    if dt is None:
        return "N/A"
    
    if format_type == "full":
        return dt.strftime("%d %B %Y, %H:%M")
    elif format_type == "date":
        return dt.strftime("%d %B %Y")
    elif format_type == "time":
        return dt.strftime("%H:%M:%S")
    elif format_type == "relative":
        return format_relative_time(dt)
    else:
        return str(dt)


def format_relative_time(dt: datetime) -> str:
    """
    Format datetime sebagai relative time (e.g., "2 jam yang lalu")
    
    Args:
        dt: datetime object
    
    Returns:
        Relative time string
    """
    if dt is None:
        return "N/A"
    
    now = datetime.now()
    diff = now - dt
    
    seconds = diff.total_seconds()
    
    if seconds < 60:
        return "Baru saja"
    elif seconds < 3600:
        minutes = int(seconds / 60)
        return f"{minutes} menit yang lalu"
    elif seconds < 86400:
        hours = int(seconds / 3600)
        return f"{hours} jam yang lalu"
    elif seconds < 604800:
        days = int(seconds / 86400)
        return f"{days} hari yang lalu"
    elif seconds < 2592000:
        weeks = int(seconds / 604800)
        return f"{weeks} minggu yang lalu"
    else:
        months = int(seconds / 2592000)
        return f"{months} bulan yang lalu"


# ==================== NUMBER FORMATTING ====================

def format_number(num: float, decimal_places: int = 2) -> str:
    """
    Format number dengan thousand separator
    
    Args:
        num: Number to format
        decimal_places: Number of decimal places
    
    Returns:
        Formatted number string
    """
    if num is None:
        return "0"
    
    return f"{num:,.{decimal_places}f}"


def format_percentage(value: float, total: float, decimal_places: int = 1) -> str:
    """
    Calculate and format percentage
    
    Args:
        value: Numerator
        total: Denominator
        decimal_places: Number of decimal places
    
    Returns:
        Formatted percentage string (e.g., "75.0%")
    """
    if total == 0:
        return "0%"
    
    percentage = (value / total) * 100
    return f"{percentage:.{decimal_places}f}%"


# ==================== VALIDATION HELPERS ====================

def validasi_email(email: str) -> bool:
    """
    Validasi format email
    
    Args:
        email: Email string to validate
    
    Returns:
        True if valid, False otherwise
    """
    if not email:
        return False
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validasi_password(password: str, min_length: int = 6) -> tuple[bool, str]:
    """
    Validasi password strength
    
    Args:
        password: Password string
        min_length: Minimum required length
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not password:
        return False, "Password tidak boleh kosong"
    
    if len(password) < min_length:
        return False, f"Password minimal {min_length} karakter"
    
    # Optional: Add more checks (uppercase, numbers, special chars)
    # For now, just check length
    
    return True, ""


# ==================== STRING HELPERS ====================

def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate text to max length
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
    
    Returns:
        Truncated text
    """
    if not text or len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def capitalize_first(text: str) -> str:
    """
    Capitalize first letter of each word
    
    Args:
        text: Text to capitalize
    
    Returns:
        Capitalized text
    """
    if not text:
        return ""
    
    return text.title()


# ==================== DATA HELPERS ====================

def paginate_list(items: List[Any], page: int, per_page: int) -> tuple[List[Any], Dict[str, Any]]:
    """
    Paginate a list of items
    
    Args:
        items: List of items to paginate
        page: Current page (0-indexed)
        per_page: Items per page
    
    Returns:
        Tuple of (paginated_items, pagination_info)
    """
    total_items = len(items)
    total_pages = (total_items + per_page - 1) // per_page  # Ceiling division
    
    start_idx = page * per_page
    end_idx = start_idx + per_page
    
    paginated_items = items[start_idx:end_idx]
    
    pagination_info = {
        "current_page": page,
        "per_page": per_page,
        "total_items": total_items,
        "total_pages": total_pages,
        "has_previous": page > 0,
        "has_next": page < total_pages - 1
    }
    
    return paginated_items, pagination_info


def group_by_field(items: List[Dict[str, Any]], field: str) -> Dict[str, List[Dict[str, Any]]]:
    """
    Group list of dicts by a specific field
    
    Args:
        items: List of dictionaries
        field: Field name to group by
    
    Returns:
        Dictionary with grouped items
    """
    grouped: Dict[str, List[Dict[str, Any]]] = {}
    
    for item in items:
        key = item.get(field, "unknown")
        if key not in grouped:
            grouped[key] = []
        grouped[key].append(item)
    
    return grouped


# ==================== COLOR HELPERS ====================

def get_severity_color(severity: str) -> str:
    """
    Get color based on severity level
    
    Args:
        severity: Severity level (rendah, sedang, tinggi)
    
    Returns:
        Color name or hex code
    """
    colors = {
        "rendah": "green",
        "sedang": "orange",
        "tinggi": "red",
        "critical": "darkred"
    }
    
    return colors.get(severity.lower(), "gray")


def get_status_color(status: str) -> str:
    """
    Get color based on status
    
    Args:
        status: Status string (aktif, suspended, nonaktif)
    
    Returns:
        Color name or hex code
    """
    colors = {
        "aktif": "green",
        "suspended": "red",
        "nonaktif": "gray"
    }
    
    return colors.get(status.lower(), "gray")


# ==================== CACHE HELPERS ====================

def create_cache_key(*args: Any) -> str:
    """
    Create a cache key from arguments
    
    Args:
        *args: Arguments to create key from
    
    Returns:
        Cache key string
    """
    return ":".join(str(arg) for arg in args)


# ==================== LOGGING HELPERS ====================

def log_user_action(user_id: str, action: str, details: Optional[Dict[str, Any]] = None):
    """
    Log user action untuk audit trail
    
    Args:
        user_id: User ID
        action: Action description
        details: Optional additional details
    """
    logger.info(
        f"User Action: {action}",
        extra={
            "user_id": user_id,
            "action": action,
            "details": details or {},
            "timestamp": datetime.now().isoformat()
        }
    )
