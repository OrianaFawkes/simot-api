
from fastapi import APIRouter, HTTPException, Response, status
from pydantic import ValidationError

from schemas.items import (
    PantryItem,
    PantryItemCreate,
    PantryItemUpdate,
)
from services import items as item_service


router = APIRouter(prefix="/items", tags=["items"])


@router.post(
    "",
    response_model=PantryItem,
    status_code=status.HTTP_201_CREATED,
)
def create_item(payload: PantryItemCreate) -> PantryItem:
    return item_service.create_item(payload)


@router.get("", response_model=list[PantryItem])
def list_items() -> list[PantryItem]:
    return item_service.list_items()


@router.get("/{item_id}", response_model=PantryItem)
def get_item(item_id: str) -> PantryItem:
    item = item_service.get_item(item_id)

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pantry item not found",
        )

    return item


@router.patch("/{item_id}", response_model=PantryItem)
def update_item(
    item_id: str,
    payload: PantryItemUpdate,
) -> PantryItem:
    updates = payload.model_dump(exclude_unset=True)

    try:
        item = item_service.update_item(item_id, updates)
    except ValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=exc.errors(),
        ) from exc

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pantry item not found",
        )

    return item


@router.delete(
    "/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_item(item_id: str) -> Response:
    deleted = item_service.delete_item(item_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pantry item not found",
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)