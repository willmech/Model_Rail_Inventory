from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Literal

ControlType = Literal["DC", "DCC", "DCC+Sound"]


@dataclass
class Locomotive:
    id: Optional[int]
    road_name: str
    locomotive_number: str
    model_manufacturer: Optional[str] = None
    prototype_manufacturer: Optional[str] = None
    control_type: ControlType = "DC"
    decoder_id: Optional[str] = None
    horsepower: Optional[int] = None
    notes: Optional[str] = None
