from abc import ABC, abstractmethod
from uuid import UUID

from app.schemas.equipment_schemas import EquipmentResponseSchema, EquipmentStatusResponseSchema, \
    EquipmentRequestSchema, EquipmentUpdateSchema
from app.schemas.equipment_status_log_schemas import EquipmentStatusLogResponseSchema


class IEquipmentService(ABC):
    """
    Interface class responsible for equipment-related operations.
    """
    @classmethod
    @abstractmethod
    async def get_equipment_statuses(cls) -> list[EquipmentStatusResponseSchema]:
        """
        Retrieves all possible equipment statuses.
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def get_equipments(cls) -> list[EquipmentResponseSchema]:
        """
        Returns a list of all registered equipments
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def get_specific_equipment(
            cls,
            equipment_id: UUID
    ) -> EquipmentResponseSchema | None:
        """
        Retrieves specific equipment by its ID.
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def post_equipment(
            cls,
            equipment_data: EquipmentRequestSchema,
    ) -> EquipmentResponseSchema:
        """
        Creates a new equipment.
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def patch_equipment(
            cls,
            equipment_id: UUID,
            equipment_data: EquipmentUpdateSchema,
    ) -> EquipmentResponseSchema | None:
        """
        Updates equipment information.
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def get_equipment_status_by_id(
            cls,
            status_id: UUID,
    ) -> EquipmentStatusResponseSchema | None:
        """
        Retrieves an equipment status by its status_id.
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def get_equipment_by_name(
            cls,
            equipment_name: str,
    ) -> EquipmentResponseSchema | None:
        """
        Retrieves equipment by its name.
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def delete_equipment(
            cls,
            equipment_id: UUID
    ) -> None:
        """
        Deletes specific equipment by its ID.
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def get_equipment_status_logs(cls) -> list[EquipmentStatusLogResponseSchema]:
        """
        Retrieves a list of all equipment status logs from the database.
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def get_specific_equipment_status_logs(
            cls,
            equipment_id: UUID,
    ) -> list[EquipmentStatusLogResponseSchema]:
        """
        Retrieves a list of specific equipment status logs from the database.
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def get_equipment_availability(cls, equipment_id: UUID) -> bool:
        raise NotImplementedError