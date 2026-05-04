from app.database import EquipmentStatus, ReservationStatus, CommandType
from app.schemas.command_schemas import CommandTypeEnum
from app.schemas.equipment_schemas import EquipmentStatusEnum
from app.schemas.reservation_schemas import ReservationStatusEnum


async def seed_equipment_statuses():
    for status in EquipmentStatusEnum:
        await EquipmentStatus.get_or_create(name=status.value)


async def seed_reservation_statuses():
    for status in ReservationStatusEnum:
        await ReservationStatus.get_or_create(name=status.value)


async def seed_command_types():
    for command in CommandTypeEnum:
        await CommandType.get_or_create(name=command.value)
