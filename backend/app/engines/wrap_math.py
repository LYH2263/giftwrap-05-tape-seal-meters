def paper_area(length: float, width: float, height: float, overlap: float = 1.15) -> dict:
    L, W, H = float(length), float(width), float(height)
    if min(L, W, H) <= 0:
        raise ValueError("box dimensions must be positive")
    base = 2 * (L * W + L * H + W * H)
    need = base * float(overlap)
    return {"box_surface": round(base, 3), "overlap": float(overlap), "paper_m2": round(need, 3)}


def ribbon_estimate(length: float, width: float, height: float, wrap_style: str = "cross") -> dict:
    """Helper: approximate ribbon length in meters (not stored as primary metric)."""
    L, W, H = float(length), float(width), float(height)
    girth = 2 * (W + H)
    if wrap_style == "band":
        meters = girth + 0.3
    else:
        meters = girth * 2 + L + 0.5
    return {"wrap_style": wrap_style, "ribbon_m": round(meters, 2)}


def tape_length(length: float, width: float, margin: float = 0.0) -> dict:
    """Sealing tape: one lap around length+width, plus registered spare margin (meters).

    Tape is a separate field from paper area and must never be folded into paper_m2.
    """
    L, W = float(length), float(width)
    if min(L, W) <= 0:
        raise ValueError("box dimensions must be positive")
    margin = float(margin)
    if margin < 0:
        raise ValueError("tape margin must be non-negative")
    meters = 2 * (L + W) + margin
    return {"tape_m": round(meters, 3), "tape_margin_m": margin}
