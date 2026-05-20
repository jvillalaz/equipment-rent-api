from typing import ClassVar
from uuid import UUID

from app.core.exceptions import NotFoundException, ConflictException
from app.interfaces.equipment_interface import IEquipmentService
from app.interfaces.location_interface import ILocationService
from app.interfaces.reservation_interface import IReservationService
from app.schemas.equipment_schemas import EquipmentResponseSchema, \
    EquipmentRequestSchema, EquipmentStatusResponseSchema, EquipmentUpdateSchema
from app.schemas.equipment_status_log_schemas import EquipmentStatusLogResponseSchema
from app.schemas.location_schema import LocationResponseSchema
from tools.application import Service

class EquipmentService(Service):
    """
    Service class responsible for equipment-related operations.
    """
    equipment_repository: ClassVar[type[IEquipmentService]]
    location_repository: type[ILocationService]
    reservation_repository: type[IReservationService]

    def __new__(
        cls,
        equipment_repository: type[IEquipmentService],
        location_repository: type[ILocationService],
        reservation_repository: type[IReservationService]
    ):
        # Assign the equipment repository implementation to the class.
        cls.equipment_repository = equipment_repository
        cls.location_repository = location_repository
        cls.reservation_repository = reservation_repository
        return cls

    @classmethod
    async def get_equipment_statuses(cls) -> list[EquipmentStatusResponseSchema]:
        """
        Retrieves all possible equipment statuses.
        """
        return await cls.equipment_repository.get_equipment_statuses()

    @classmethod
    async def get_equipments(cls) -> list[EquipmentResponseSchema]:
        """
        Returns a list of all registered equipments
        """
        return await cls.equipment_repository.get_equipments()

    @classmethod
    async def get_specific_equipment(cls, equipment_id: UUID) -> EquipmentResponseSchema:
        """
        Retrieves specific equipment by its ID.
        """
        equipment_response = await cls.equipment_repository.get_specific_equipment(equipment_id)

        if not equipment_response:
            raise NotFoundException(detail=f"Requested equipment {equipment_id} not found")

        return equipment_response

    @classmethod
    async def get_equipment_status_by_id(
            cls,
            status_id: UUID
    ) -> EquipmentStatusResponseSchema:
        """
        Validates the existence of an equipment status raises NotFoundException if not found.
        """
        status_exists = await cls.equipment_repository.get_equipment_status_by_id(status_id)

        if not status_exists:
            raise NotFoundException(detail=f"Equipment status {status_id} not found")

        return status_exists

    @classmethod
    async def get_equipment_by_name(
            cls,
            equipment_name: str,
    ) -> None:
        """
        Raises ConflictException if equipment with the given name already exists.
        """
        existing = await cls.equipment_repository.get_equipment_by_name(equipment_name)

        if existing:
            raise ConflictException(detail=f"Equipment '{equipment_name}' already exists")


    @classmethod
    async def post_equipment(
            cls,
            equipment_data: EquipmentRequestSchema,
    ) -> EquipmentResponseSchema:
        """
        Creates a new equipment.
        """

        _ = await cls.get_equipment_status_by_id(equipment_data.current_status_id)

        equipment_exists = await cls.get_equipment_by_name(equipment_data.name)
        print(equipment_exists)
        if equipment_exists:
            raise ConflictException(detail=f"Equipment '{equipment_data.name}' already exists")

        location_exists: LocationResponseSchema | None = await cls.location_repository.get_location_by_id(equipment_data.location)

        if not location_exists:
            raise NotFoundException(detail=f"Location {equipment_data.location} not found")

        equipment = await cls.equipment_repository.post_equipment(equipment_data)
        return equipment

    @classmethod
    async def patch_equipment(
            cls,
            equipment_id: UUID,
            equipment_data: EquipmentUpdateSchema,
    ) -> EquipmentResponseSchema:
        """
        Updates equipment information.
        """
        _ = await cls.get_specific_equipment(equipment_id)

        if equipment_data.current_status_id is not None:
            _ = await cls.get_equipment_status_by_id(equipment_data.current_status_id)

        location_exists =  await cls.location_repository.get_location_by_id(equipment_data.location)

        if not location_exists:
            raise NotFoundException(detail=f"Location {equipment_data.location} not found")

        equipment_response = await cls.equipment_repository.patch_equipment(equipment_id, equipment_data)

        if not equipment_response:
            raise ConflictException(detail=f"Equipment '{equipment_data.name}' already exists")

        return equipment_response

    @classmethod
    async def delete_equipment(
            cls,
            equipment_id: UUID
    ) -> None:
        """
        Deletes specific equipment by its ID.
        """
        _ = await cls.get_specific_equipment(equipment_id)

        equipment_reservation_exists = await cls.reservation_repository.get_specific_reservation_by_equipment(equipment_id)

        if equipment_reservation_exists:
            raise ConflictException(detail=f"Cannot delete equipment {equipment_id} because it is reserved")

        return await cls.equipment_repository.delete_equipment(equipment_id)

    @classmethod
    async def get_equipment_status_logs(cls) -> list[EquipmentStatusLogResponseSchema]:
        """
        Retrieves a list of all equipment status logs from the database.
        """
        return await cls.equipment_repository.get_equipment_status_logs()

    @classmethod
    async def get_specific_equipment_status_logs(
            cls,
            equipment_id: UUID,
    ) -> list[EquipmentStatusLogResponseSchema]:
        """
        Retrieves a list of specific equipment status logs from the database.
        """
        return await cls.equipment_repository.get_specific_equipment_status_logs(equipment_id)
