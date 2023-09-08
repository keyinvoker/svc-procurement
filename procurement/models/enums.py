from enum import Enum


# TODO: is this set or dynamic? if dynamic, make master table
class ItemCategory(Enum):
    MECHANICAL = "mechanical"
    ELECTRICAL = "electrical"
    CIVIL = "civil"
    PIPE = "pipe"
