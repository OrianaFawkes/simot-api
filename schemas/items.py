
from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class Unit(str, Enum):
    PIECE = "piece"
    PACK = "pack"
    BOTTLE = "bottle"
    CAN = "can"
    GRAM = "g"
    KILOGRAM = "kg"
    MILLILITER = "ml"
    LITER = "l"


class Category(str, Enum):
    GRAINS = "grains"
    DAIRY = "dairy"
    MEAT_SEAFOOD = "meat_seafood"
    FRUITS_VEGETABLES = "fruits_vegetables"
    CONDIMENTS = "condiments"
    SNACKS = "snacks"
    BEVERAGES = "beverages"
    OTHER = "other"


class StorageLocation(str, Enum):
    PANTRY = "pantry"
    FRIDGE = "fridge"
    FREEZER = "freezer"
    OTHER = "other"


class PantryItemCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=1, max_length=120)
    quantity: float = Field(ge=0, allow_inf_nan=False)
    unit: Unit
    category: Category = Category.OTHER

    min_quantity: float | None = Field(
        default=None, ge=0, allow_inf_nan=False
    )
    is_essential: bool = False

    barcode: str | None = Field(default=None, max_length=100)
    expiry_date: date | None = None
    opened_at: datetime | None = None
    storage_location: StorageLocation = StorageLocation.PANTRY
    purchase_date: date | None = None


class PantryItemUpdate(BaseModel):
    # Every field is optional for PATCH.
    # Explicit nulls for required fields are rejected when the
    # updated item is validated as a PantryItemCreate.
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str | None = Field(default=None, min_length=1, max_length=120)
    quantity: float | None = Field(
        default=None, ge=0, allow_inf_nan=False
    )
    unit: Unit | None = None
    category: Category | None = None

    min_quantity: float | None = Field(
        default=None, ge=0, allow_inf_nan=False
    )
    is_essential: bool | None = None

    barcode: str | None = Field(default=None, max_length=100)
    expiry_date: date | None = None
    opened_at: datetime | None = None
    storage_location: StorageLocation | None = None
    purchase_date: date | None = None


class PantryItem(PantryItemCreate):
    id: str
    created_at: datetime
    updated_at: datetime