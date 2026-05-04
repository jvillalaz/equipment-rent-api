from typing import List, Optional
from uuid import UUID

from app.database import Equipment, EquipmentStatusLog
from app.interfaces.equipment_interface import IEquipmentService

from app.database import EquipmentStatus
from app.schemas.equipment_schemas import EquipmentResponseSchema, EquipmentStatusResponseSchema, \
    EquipmentRequestSchema, EquipmentUpdateSchema
from app.schemas.equipment_status_log_schemas import EquipmentStatusLogResponseSchema


class EquipmentPersistence(IEquipmentService):
    """
    Persistence class responsible for equipment-related operations.
    """
    @classmethod
    async def get_equipment_statuses(cls) -> List[EquipmentStatusResponseSchema]:
        """
        Retrieves all possible equipment statuses.
        """
        status_record = await EquipmentStatus.all()
        status_list: List[EquipmentStatusResponseSchema] = []

        for equipment_status in status_record:
            status_response = EquipmentStatusResponseSchema(
                id=equipment_status.id,
                name=equipment_status.name,
                created_at=equipment_status.created_at,
            )
            status_list.append(status_response)

        return status_list

    @classmethod
    async def get_equipments(cls) -> List[EquipmentResponseSchema]:
        """
        Returns a list of all registered equipments
        """
        equipments_record = await Equipment.all().select_related('current_status')
        equipments_list: List[EquipmentResponseSchema] = []

        for equipment in equipments_record:
            equipment_response = EquipmentResponseSchema(
                id=equipment.id,
                name=equipment.name,
                current_status_name=equipment.current_status.name,
                location=equipment.location,
                last_heartbeat=equipment.last_heartbeat,
                created_at=equipment.created_at
            )
            equipments_list.append(equipment_response)

        return equipments_list


    @classmethod
    async def get_specific_equipment(
            cls,
            equipment_id: UUID
    ) -> Optional[EquipmentResponseSchema]:
        """
        Retrieves specific equipment by its ID.
        """
        equipment = await Equipment.get_or_none(id=equipment_id).select_related('current_status')

        if not equipment:
            return None

        equipment_response = EquipmentResponseSchema(
            id=equipment.id,
            name=equipment.name,
            current_status_name=equipment.current_status.name,
            location=equipment.location,
            last_heartbeat=equipment.last_heartbeat,
            created_at=equipment.created_at
        )

        return equipment_response

    @classmethod
    async def get_equipment_status_by_id(
            cls,
            status_id: UUID
    ) -> Optional[EquipmentStatusResponseSchema]:
        """
        Retrieves an equipment status by its status_id.
        """
        status_exists = await EquipmentStatus.get_or_none(id=status_id).select_related('current_status')

        status_response = EquipmentStatusResponseSchema(
            id=status_exists.id,
            name=status_exists.name,
            created_at=status_exists.created_at,
        )

        return status_response

    @classmethod
    async def get_equipment_by_name(
            cls,
            equipment_name: str,
    ) -> Optional[EquipmentResponseSchema]:
        """
        Retrieves equipment by its name.
        """
        equipment = await Equipment.get_or_none(name=equipment_name).select_related('current_status')

        if not equipment:
            return None

        return EquipmentResponseSchema(
            id=equipment.id,
            name=equipment.name,
            current_status_name=equipment.current_status.name,
            location=equipment.location,
            last_heartbeat=equipment.last_heartbeat,
            created_at=equipment.created_at
        )

    @classmethod
    async def post_equipment(
            cls,
            equipment_data: EquipmentRequestSchema,
    ) -> EquipmentResponseSchema:
        """
        Creates a new equipment.
        """
        equipment = await Equipment.create(
            name=equipment_data.name,
            current_status_id=equipment_data.current_status_id,
            location=equipment_data.location,
        )

        return EquipmentResponseSchema(
            id=equipment.id,
            name=equipment.name,
            current_status_name=equipment.current_status.name,
            location=equipment.location,
            last_heartbeat=equipment.last_heartbeat,
            created_at=equipment.created_at
        )

    @classmethod
    async def patch_equipment(
            cls,
            equipment_id: UUID,
            equipment_data: EquipmentUpdateSchema,
    ) -> Optional[EquipmentResponseSchema]:

        equipment = await Equipment.get_or_none(id=equipment_id).select_related('current_status')

        if equipment_data.name and equipment_data.name != equipment.name:
            existing = await Equipment.get_or_none(name=equipment_data.name)
            if existing and existing.id != equipment.id:
                return None
            equipment.name = equipment_data.name

        if equipment_data.current_status_id is not None:
            equipment.current_status_id = equipment_data.current_status_id

        if equipment_data.location is not None:
            equipment.location = equipment_data.location

        if equipment_data.last_heartbeat is not None:
            equipment.last_heartbeat = equipment_data.last_heartbeat

        await equipment.save()

        return EquipmentResponseSchema(
            id=equipment.id,
            name=equipment.name,
            current_status_name=equipment.current_status.name,
            location=equipment.location,
            last_heartbeat=equipment.last_heartbeat,
            created_at=equipment.created_at
        )

    @classmethod
    async def delete_equipment(
            cls,
            equipment_id: UUID
    ) -> None:

        equipment = await Equipment.get_or_none(id=equipment_id)
        return await equipment.delete()

    @classmethod
    async def _fetch_and_map_status_logs(
            cls,
            equipment_id: Optional[UUID] = None
    ) -> List[EquipmentStatusLogResponseSchema]:
        """
        Internal helper to fetch and map equipment status logs,
        optionally filtered by equipment_id.
        """
        query = EquipmentStatusLog.all().select_related("equipment", "status")

        if equipment_id:
            query = query.filter(equipment_id=equipment_id)

        status_logs = await query

        result_list = []
        for log in status_logs:
            mapped_log = EquipmentStatusLogResponseSchema(
                id=log.id,
                equipment_status=log.status.name,
                equipment_name=log.equipment.name,
                details=log.details,
                reported_at=log.reported_at,
                created_at=log.created_at
            )
            result_list.append(mapped_log)

        return result_list

    @classmethod
    async def get_equipment_status_logs(cls) -> List[EquipmentStatusLogResponseSchema]:
        """
        Retrieves a list of all equipment status logs from the database.
        """
        return await cls._fetch_and_map_status_logs()

    @classmethod
    async def get_specific_equipment_status_logs(
            cls,
            equipment_id: UUID,
    ) -> List[EquipmentStatusLogResponseSchema]:
        """
        Retrieves a list of specific equipment status logs from the database.
        """
        return await cls._fetch_and_map_status_logs(equipment_id=equipment_id)
