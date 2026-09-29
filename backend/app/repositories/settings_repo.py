from app.config import DEFAULT_OVERLAP, DEFAULT_TAPE_ENABLED, DEFAULT_TAPE_MARGIN_M
from app.db import connect

def get_all():
    c = connect()
    try:
        d = {r["key"]: r["value"] for r in c.execute("SELECT key,value FROM settings").fetchall()}
        d.setdefault("overlap", str(DEFAULT_OVERLAP))
        d.setdefault("tape_enabled", str(bool(DEFAULT_TAPE_ENABLED)).lower())
        d.setdefault("tape_margin_m", str(DEFAULT_TAPE_MARGIN_M))
        return d
    finally:
        c.close()

def get_overlap():
    return float(get_all().get("overlap", DEFAULT_OVERLAP))

def get_tape_enabled():
    return str(get_all().get("tape_enabled", "")).lower() in ("1", "true", "yes", "on")

def get_tape_margin_m():
    return float(get_all().get("tape_margin_m", DEFAULT_TAPE_MARGIN_M))

def update(values: dict):
    c = connect()
    try:
        c.executemany(
            "INSERT INTO settings(key,value) VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
            list(values.items()),
        )
        c.commit()
    finally:
        c.close()
