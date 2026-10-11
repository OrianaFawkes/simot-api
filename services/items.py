
from datetime import datetime, timezone
from uuid import uuid4

from pydantic import ValidationError

from schemas.items import PantryItem, PantryItemCreate


# Temporary in-memory storage.
item_store: dict[str, PantryItem] = {}


def create_item(data: PantryItemCreate) -> PantryItem:
    now = datetime.now(timezone.utc)

    item = PantryItem(
        **data.model_dump(),
        id=str(uuid4()),
        created_at=now,
        updated_at=now,
    )

    item_store[item.id] = item
    return item


def list_items() -> list[PantryItem]:
    return list(item_store.values())


def get_item(item_id: str) -> PantryItem | None:
    return item_store.get(item_id)


def update_item(
    item_id: str,
    updates: dict,
) -> PantryItem | None:
    current = item_store.get(item_id)

    if current is None:
        return None

    # Only include fields accepted by the create schema.
    merged = current.model_dump(
        include=set(PantryItemCreate.model_fields)
    )
    merged.update(updates)

    # Validate the complete updated item, not just the changed fields.
    validated = PantryItemCreate.model_validate(merged)

    updated = PantryItem(
        **validated.model_dump(),
        id=current.id,
        created_at=current.created_at,
        updated_at=datetime.now(timezone.utc),
    )

    item_store[item_id] = updated
    return updated


def delete_item(item_id: str) -> bool:
    return item_store.pop(item_id, None) is not None