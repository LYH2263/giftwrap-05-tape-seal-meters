def test_tape_off_by_default_keeps_legacy_fields(client):
    r = client.get("/api/estimate", params={"box_id": 1})
    assert r.status_code == 200
    body = r.json()
    assert body["tape_m"] == 0.0
    assert body["tape"]["enabled"] is False
    assert body["paper_m2"] == 0.31
    assert body["ribbon"]["ribbon_m"] > 0.5


def test_tape_on_is_separate_field_from_paper(client):
    r = client.post("/api/estimate", json={
        "box_id": 1, "save": True, "tape_enabled": True, "tape_margin_m": 0.1,
    })
    assert r.status_code == 200
    body = r.json()
    assert body["tape_m"] == 1.1
    assert body["tape"]["tape_m"] == 1.1
    assert body["tape"]["enabled"] is True
    assert body["paper_m2"] == 0.31
    assert body["run_id"] is not None


def test_negative_margin_fails_order_without_persisting(client):
    r = client.post("/api/estimate", json={
        "box_id": 1, "save": True, "tape_enabled": True, "tape_margin_m": -0.1,
    })
    assert r.status_code == 422
    assert client.get("/api/runs").json()["items"] == []


def test_stored_run_pinned_after_default_margin_changes(client):
    saved = client.post("/api/estimate", json={
        "box_id": 1, "save": True, "tape_enabled": True, "tape_margin_m": 0.1,
    }).json()
    rid = saved["run_id"]

    # Change the global default margin: stored rows must not be recomputed.
    upd = client.post("/api/settings", json={"tape_margin_m": 0.5})
    assert upd.status_code == 200

    listed = client.get("/api/runs").json()["items"][0]
    detail = client.get(f"/api/runs/{rid}").json()
    for view in (listed["result"], detail["result"]):
        assert view["tape_m"] == 1.1
        assert view["paper_m2"] == 0.31

    # Same params on the bench, dry run: must agree with the stored record.
    dry = client.get("/api/estimate", params={
        "box_id": 1, "tape_enabled": "true", "tape_margin_m": 0.1,
    }).json()
    assert dry["tape_m"] == detail["result"]["tape_m"] == 1.1
    assert dry["paper_m2"] == detail["result"]["paper_m2"] == 0.31


def test_default_tape_settings_apply_without_overrides(client):
    client.post("/api/settings", json={"tape_enabled": True, "tape_margin_m": 0.2})
    body = client.get("/api/estimate", params={"box_id": 1}).json()
    assert body["tape_m"] == 1.2
    assert body["paper_m2"] == 0.31
