from __future__ import annotations

from typing import List, Optional

from rail_inventory.database.db import get_connection
from rail_inventory.models.locomotive import Locomotive


def _normalize_decoder(control_type: str, decoder_id: Optional[str]) -> Optional[str]:
    if control_type == "DC":
        return None
    if decoder_id is None:
        return None
    decoder_id = decoder_id.strip()
    return decoder_id or None


def add_locomotive(loco: Locomotive) -> int:
    decoder_id = _normalize_decoder(loco.control_type, loco.decoder_id)

    with get_connection() as conn:
        cur = conn.execute(
            """
            INSERT INTO locomotives
              (road_name, locomotive_number, model_manufacturer, prototype_manufacturer,
               control_type, decoder_id, horsepower, notes)
            VALUES
              (?, ?, ?, ?, ?, ?, ?, ?);
            """,
            (
                loco.road_name.strip(),
                loco.locomotive_number.strip(),
                loco.model_manufacturer,
                loco.prototype_manufacturer,
                loco.control_type,
                decoder_id,
                loco.horsepower,
                loco.notes,
            ),
        )
        return int(cur.lastrowid)


def get_all_locomotives() -> List[Locomotive]:
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT id, road_name, locomotive_number,
                   model_manufacturer, prototype_manufacturer,
                   control_type, decoder_id, horsepower, notes
            FROM locomotives
            ORDER BY road_name ASC, locomotive_number ASC;
            """
        ).fetchall()

    return [
        Locomotive(
            id=row["id"],
            road_name=row["road_name"],
            locomotive_number=row["locomotive_number"],
            model_manufacturer=row["model_manufacturer"],
            prototype_manufacturer=row["prototype_manufacturer"],
            control_type=row["control_type"],
            decoder_id=row["decoder_id"],
            horsepower=row["horsepower"],
            notes=row["notes"],
        )
        for row in rows
    ]


def update_locomotive(loco: Locomotive) -> None:
    if loco.id is None:
        raise ValueError("update_locomotive requires loco.id")

    decoder_id = _normalize_decoder(loco.control_type, loco.decoder_id)

    with get_connection() as conn:
        conn.execute(
            """
            UPDATE locomotives
            SET road_name = ?,
                locomotive_number = ?,
                model_manufacturer = ?,
                prototype_manufacturer = ?,
                control_type = ?,
                decoder_id = ?,
                horsepower = ?,
                notes = ?
            WHERE id = ?;
            """,
            (
                loco.road_name.strip(),
                loco.locomotive_number.strip(),
                loco.model_manufacturer,
                loco.prototype_manufacturer,
                loco.control_type,
                decoder_id,
                loco.horsepower,
                loco.notes,
                loco.id,
            ),
        )


def delete_locomotive(loco_id: int) -> None:
    with get_connection() as conn:
        conn.execute("DELETE FROM locomotives WHERE id = ?;", (loco_id,))
