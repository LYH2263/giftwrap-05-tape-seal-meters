from pydantic import BaseModel, Field

class SettingsUpdate(BaseModel):
    tape_enabled: bool | None = None
    tape_margin_m: float | None = Field(default=None, ge=0)
