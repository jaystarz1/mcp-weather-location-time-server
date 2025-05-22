from datetime import datetime
from zoneinfo import ZoneInfo

def get_current_time(timezone: str = "UTC"):
    """
    Returns the current date and time in the specified timezone (IANA format).
    """
    try:
        tz = ZoneInfo(timezone)
    except Exception:
        tz = ZoneInfo("UTC")
    now = datetime.now(tz)
    return {
        "timezone": str(timezone),
        "datetime": now.isoformat(timespec="seconds"),
        "is_dst": bool(now.dst()),
    }
