
import re
from datetime import date, datetime, time
from typing import Optional, List 
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def ReplacePrice(input: str, pref: str):
    if not input:
        return ""
    preference = "SL" if pref == "Sleeper" else "A"
    input = input.replace("\r", "").replace("\n", "") 
    entries = input.split(";")
    ans = []
    for entry in entries:
        entry = entry.strip().replace("?", "₹")
        if preference in entry and entry:
            ans.append(entry)
    return ", ".join(ans)


def parse_db_time_string(time_str: Optional[str]) -> Optional[time]:
    if not time_str:
        return None
    time_str = time_str.strip().upper()
    time_str = re.sub(r'\s*([AP]M)', r'\1', time_str)
    formats_to_try = ["%I:%M%p", "%H:%M"]
    parsed_time = None
    for fmt in formats_to_try:
        try:
            parsed_time = datetime.strptime(time_str, fmt).time()
            break
        except ValueError:
            continue
    if parsed_time is None:
        print(f"Warning: Could not parse time string from DB: '{time_str}'")
    return parsed_time


def combine_with_date(time_obj: Optional[time], date_val: date) -> Optional[datetime]:
    """Combines a datetime.time object with a date object to create a datetime object."""
    if time_obj is None:
        return None
    return datetime.combine(date_val, time_obj)


def matching(ttype: str, preferences: str) -> bool:
    if not preferences: 
        return True
    if not ttype and preferences:
        return False
        
    ttype_parts = set(normalize_text(ttype))
    up = set(normalize_text(preferences))
    if not up: 
        return True

    updated_parts = set()
    for part in ttype_parts:
        lowered = part.lower()
        if "seater" in lowered and "sleeper" in lowered:
            if "-" in lowered:
                updated_parts.update(subpart.strip() for subpart in lowered.split("-") if subpart.strip())
            elif "/" in lowered:
                updated_parts.update(subpart.strip() for subpart in lowered.split("/") if subpart.strip())
            else: 
                updated_parts.add("seater")
                updated_parts.add("sleeper")
        updated_parts.add(lowered)
    return up.issubset(updated_parts)

def normalize_text(raw: str | list) -> list:
    if not raw:
        return []
    if isinstance(raw, list):
        raw = ' '.join(raw)
    parts =re.split(r'[\s,()\u2010\t]+', raw)
    return [p.strip().lower() for p in parts if p.strip()]