from fastapi import HTTPException
from app.engines.wrap_math import paper_area, ribbon_estimate, tape_length
from app.repositories import boxes, history, settings_repo

def run_estimate(box_id: int, overlap: float | None, wrap_style: str, save: bool, note: str,
                 tape_enabled: bool | None = None, tape_margin_m: float | None = None):
    box = boxes.get_box(box_id)
    if not box:
        raise HTTPException(404)
    if box.get("data_quality") == "dirty":
        raise HTTPException(422, "dirty box")
    ov = float(overlap) if overlap is not None else settings_repo.get_overlap()
    tape_on = settings_repo.get_tape_enabled() if tape_enabled is None else bool(tape_enabled)
    margin = settings_repo.get_tape_margin_m() if tape_margin_m is None else float(tape_margin_m)
    calc = paper_area(box["length"], box["width"], box["height"], ov)
    ribbon = ribbon_estimate(box["length"], box["width"], box["height"], wrap_style)
    # Tape is its own field, never folded into paper_m2. A negative margin fails
    # the whole order before any row is written.
    if tape_on:
        try:
            tape = {"enabled": True, **tape_length(box["length"], box["width"], margin)}
        except ValueError as exc:
            raise HTTPException(422, str(exc))
    else:
        tape = {"enabled": False, "tape_m": 0.0}
    payload = {**calc, "ribbon": ribbon, "tape": tape, "tape_m": tape["tape_m"], "box_id": box_id}
    run_id = history.insert_run(box_id, ov, payload, note) if save else None
    return {"box": box, "run_id": run_id, **calc, "ribbon": ribbon, "tape": tape, "tape_m": tape["tape_m"]}
