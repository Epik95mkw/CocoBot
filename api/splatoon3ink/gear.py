from typing import TypedDict, Optional

from . import _util


class ImageRef(TypedDict):
    url: str


class GearAbility(TypedDict):
    __splatoon3ink_id: str
    name: str
    image: ImageRef

class BrandAbility(GearAbility):
    desc: str
    isEmptySlot: bool


class BrandInfo(TypedDict):
    name: str
    id: str

class CurrentDailyBrand(BrandInfo):
    usualGearPower: BrandAbility

class NextDailyBrand(BrandInfo):
    image: ImageRef

class GearBrand(BrandInfo):
    usualGearPower: BrandAbility
    image: ImageRef


class GearItem(TypedDict):
    __splatoon3ink_id: str
    __typename: str
    name: str
    primaryGearPower: GearAbility
    additionalGearPowers: list[GearAbility]
    image: ImageRef
    brand: GearBrand

class ShopSlotRef(TypedDict):
    id: str

class ShopSlot(TypedDict):
    id: str
    saleEndTime: str
    price: int
    gear: GearItem
    isAlreadyOrdered: bool
    nextGear: Optional[ShopSlotRef]
    previousGear: Optional[ShopSlotRef]
    ownedGear: None


class DailyBrandData(TypedDict):
    image: ImageRef
    brand: CurrentDailyBrand
    saleEndTime: str
    brandGears: list[ShopSlot]
    nextBrand: NextDailyBrand

class ShopCategories(TypedDict):
    pickupBrand: DailyBrandData
    limitedGears: list[ShopSlot]

class ShopData(TypedDict):
    gesotown: ShopCategories


def get() -> Optional[ShopData]:
    return _util.fetch_api('/gear.json')