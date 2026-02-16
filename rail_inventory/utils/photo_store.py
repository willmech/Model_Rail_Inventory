from __future__ import annotations

import shutil
from pathlib import Path
from uuid import uuid4

from rail_inventory.database.db import get_images_dir


def import_locomotive_photo(source_path: str) -> str:
    """
    Copy a selected photo into data/images/locomotives and return the RELATIVE path
    to store in SQLite (portable within the repo).
    """
    src = Path(source_path).expanduser().resolve()
    if not src.exists():
        raise FileNotFoundError(str(src))

    dest_dir = get_images_dir() / "locomotives"
    ext = src.suffix.lower() or ".jpg"
    dest_name = f"{uuid4().hex}{ext}"
    dest = dest_dir / dest_name

    shutil.copy2(src, dest)

    return f"images/locomotives/{dest_name}"
