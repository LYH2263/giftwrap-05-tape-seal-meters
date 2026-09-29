from fastapi import APIRouter
from app.repositories import settings_repo
from app.schemas.settings import SettingsUpdate
router = APIRouter()
@router.get("/settings")
def settings(): return settings_repo.get_all()
@router.post("/settings")
def update_settings(body: SettingsUpdate):
    values = {}
    if body.tape_enabled is not None:
        values["tape_enabled"] = "true" if body.tape_enabled else "false"
    if body.tape_margin_m is not None:
        values["tape_margin_m"] = str(float(body.tape_margin_m))
    if values:
        settings_repo.update(values)
    return settings_repo.get_all()
