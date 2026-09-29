from app.engines.wrap_math import paper_area, ribbon_estimate, tape_length
import pytest

def test_book_box():
    r = paper_area(0.30, 0.20, 0.15, 1.15)
    assert r["box_surface"] == 0.27
    assert r["paper_m2"] == 0.31

def test_ribbon_cross():
    rb = ribbon_estimate(0.30, 0.20, 0.15, "cross")
    assert rb["ribbon_m"] > 0.5

def test_tape_lap_plus_margin():
    t = tape_length(0.30, 0.20, 0.1)
    assert t["tape_m"] == 1.1
    assert t["tape_margin_m"] == 0.1

def test_tape_zero_margin():
    assert tape_length(0.3, 0.2)["tape_m"] == 1.0

def test_tape_negative_margin_rejected():
    with pytest.raises(ValueError):
        tape_length(0.3, 0.2, -0.01)
