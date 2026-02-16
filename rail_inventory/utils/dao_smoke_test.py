from rail_inventory.database.db import initialize_database
from rail_inventory.database.locomotives_dao import (
    add_locomotive,
    delete_locomotive,
    get_all_locomotives,
    update_locomotive,
)
from rail_inventory.models.locomotive import Locomotive


def run() -> None:
    initialize_database()

    new_id = add_locomotive(
        Locomotive(
            id=None,
            road_name="CN",
            locomotive_number="2234",
            model_manufacturer="Kato",
            prototype_manufacturer="GE",
            control_type="DCC+Sound",
            decoder_id="DCC-001",
            horsepower=4400,
            notes="Smoke test insert",
        )
    )
    print(f"Inserted id={new_id}")

    locos = get_all_locomotives()
    print(f"Count after insert: {len(locos)}")

    target = next(l for l in locos if l.id == new_id)
    target.notes = "Updated note"
    target.control_type = "DC"
    target.decoder_id = "SHOULD-BE-CLEARED"
    update_locomotive(target)
    print("Updated (DC should clear decoder_id)")

    delete_locomotive(new_id)
    print("Deleted")

    print(f"Count after delete: {len(get_all_locomotives())}")


if __name__ == "__main__":
    run()
