from typing import Type, List
from uuid import UUID

from app.core.exceptions import NotFoundException, ConflictException
from app.interfaces.equipment_interface import IEquipmentService
from app.schemas.equipment_schemas import EquipmentResponseSchema, \
    EquipmentRequestSchema, EquipmentStatusResponseSchema, EquipmentUpdateSchema
from app.schemas.equipment_status_log_schemas import EquipmentStatusLogResponseSchema
from tools.application import Service


class EquipmentService(Service):
    """
    Service class responsible for equipment-related operations.
    """
    equipment_repository: Type[IEquipmentService]

    def __new__(
        cls,
        equipment_repository: Type[IEquipmentService],
    ):
        # Assign the equipment repository implementation to the class.
        cls.equipment_repository = equipment_repository
        return cls

    @classmethod
    async def get_equipment_statuses(cls) -> List[EquipmentStatusResponseSchema]:
        """
        Retrieves all possible equipment statuses.
        """
        return await cls.equipment_repository.get_equipment_statuses()

    @classmethod
    async def get_equipments(cls) -> List[EquipmentResponseSchema]:
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
    ) -> EquipmentResponseSchema:
        """
        Fetches equipment by name and raises ConflictException if found.
        """
        equipment_name = await cls.equipment_repository.get_equipment_by_name(equipment_name)

        if equipment_name:
            raise ConflictException(detail=f"Equipment {equipment_name} already exists")

        return equipment_name


    @classmethod
    async def post_equipment(
            cls,
            equipment_data: EquipmentRequestSchema,
    ) -> EquipmentResponseSchema:
        """
        Creates a new equipment.
        """
        await cls.get_equipment_status_by_id(equipment_data.current_status_id)
        await cls.get_equipment_by_name(equipment_data.name)

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
        await cls.get_specific_equipment(equipment_id)
        await cls.get_equipment_status_by_id(equipment_data.current_status_id)
        equipment_response =  await cls.equipment_repository.patch_equipment(equipment_id, equipment_data)

        if not equipment_response:
            raise ConflictException(detail=f"Equipment {EquipmentUpdateSchema.name} already exists")

        return equipment_response

    @classmethod
    async def delete_equipment(
            cls,
            equipment_id: UUID
    ) -> None:
        """
        Deletes specific equipment by its ID.
        """
        await cls.get_specific_equipment(equipment_id)
        return await cls.equipment_repository.delete_equipment(equipment_id)

    @classmethod
    async def get_equipment_status_logs(cls) -> List[EquipmentStatusLogResponseSchema]:
        """
        Retrieves a list of all equipment status logs from the database.
        """
        return await cls.equipment_repository.get_equipment_status_logs()

    @classmethod
    async def get_specific_equipment_status_logs(
            cls,
            equipment_id: UUID,
    ) -> List[EquipmentStatusLogResponseSchema]:
        """
        Retrieves a list of specific equipment status logs from the database.
        """
        return await cls.equipment_repository.get_specific_equipment_status_logs(equipment_id)
