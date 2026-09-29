from pydantic import BaseModel

class EstimateRequest(BaseModel):
    box_id: int
    overlap: float | None = None
    wrap_style: str = "cross"
    save: bool = False
    note: str = ""
    tape_enabled: bool | None = None
    tape_margin_m: float | None = None
