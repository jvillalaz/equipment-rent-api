from typing_extensions import override
from uuid import UUID

from app.database import Equipment, EquipmentStatusLog
from app.database.location import Location
from app.interfaces.equipment_interface import IEquipmentService

from app.database import EquipmentStatus
from app.schemas.equipment_schemas import EquipmentResponseSchema, EquipmentStatusResponseSchema, \
    EquipmentRequestSchema, EquipmentUpdateSchema, EquipmentStatusEnum
from app.schemas.equipment_status_log_schemas import EquipmentStatusLogResponseSchema
from app.schemas.location_schema import LocationResponseSchema
from tortoise.queryset import Q

class EquipmentPersistence(IEquipmentService):
    """
    Persistence class responsible for equipment-related operations.
    """
    @override
    @classmethod
    async def get_equipment_statuses(cls) -> list[EquipmentStatusResponseSchema]:
        """
        Retrieves all possible equipment statuses.
        """
        status_record = await EquipmentStatus.all()
        status_list: list[EquipmentStatusResponseSchema] = []

        for equipment_status in status_record:
            status_response = EquipmentStatusResponseSchema(
                id=equipment_status.id,
                name=equipment_status.name,
                created_at=equipment_status.created_at,
            )
            status_list.append(status_response)

        return status_list

    @override
    @classmethod
    async def get_equipments(cls) -> list[EquipmentResponseSchema]:
        """
        Returns a list of all registered equipments
        """
        equipments_record = await Equipment.all().select_related('current_status', 'location')
        equipments_list: list[EquipmentResponseSchema] = []

        for equipment in equipments_record:
            equipment_response = EquipmentResponseSchema(
                id=equipment.id,
                name=equipment.name,
                current_status_name=equipment.current_status.name if equipment.current_status else EquipmentStatusEnum.OFFLINE,
                location= LocationResponseSchema(id=equipment.location.id, name=equipment.location.name, created_at=equipment.location.created_at) if equipment.location else None,
                last_heartbeat=equipment.last_heartbeat,
                created_at=equipment.created_at
            )
            equipments_list.append(equipment_response)

        return equipments_list


    @override
    @classmethod
    async def get_specific_equipment(
            cls,
            equipment_id: UUID
    ) -> EquipmentResponseSchema | None:
        """
        Retrieves specific equipment by its ID.
        """
        equipment = await Equipment.get_or_none(id=equipment_id).select_related('current_status', 'location')

        if not equipment:
            return None

        equipment_response = EquipmentResponseSchema(
            id=equipment.id,
            name=equipment.name,
            current_status_name=equipment.current_status.name if equipment.current_status else EquipmentStatusEnum.OFFLINE,
            location=LocationResponseSchema(id=equipment.location.id, name=equipment.location.name, created_at=equipment.location.created_at) if equipment.location else None,
            last_heartbeat=equipment.last_heartbeat,
            created_at=equipment.created_at
        )

        return equipment_response

    @override
    @classmethod
    async def get_equipment_status_by_id(
            cls,
            status_id: UUID
    ) -> EquipmentStatusResponseSchema | None:
        """
        Retrieves an equipment status by its status_id.
        """
        status_exists = await EquipmentStatus.get_or_none(id=status_id)

        if not status_exists:
            return None

        status_response = EquipmentStatusResponseSchema(
            id=status_exists.id,
            name=status_exists.name,
            created_at=status_exists.created_at,
        )

        return status_response

    @override
    @classmethod
    async def get_equipment_by_name(
            cls,
            equipment_name: str,
    ) -> EquipmentResponseSchema | None:
        """
        Retrieves equipment by its name.
        """
        equipment = await Equipment.get_or_none(name=equipment_name).select_related('current_status')

        if not equipment:
            return None

        return EquipmentResponseSchema(
            id=equipment.id,
            name=equipment.name,
            current_status_name=equipment.current_status.name if equipment.current_status else EquipmentStatusEnum.OFFLINE,
            location=equipment.location,
            last_heartbeat=equipment.last_heartbeat,
            created_at=equipment.created_at
        )

    @override
    @classmethod
    async def post_equipment(
            cls,
            equipment_data: EquipmentRequestSchema,
    ) -> EquipmentResponseSchema:
        """
        Creates a new equipment.
        """

        location: Location | None = await Location.get_or_none(id=equipment_data.location)

        equipment = await Equipment.create(
            name=equipment_data.name,
            current_status_id=equipment_data.current_status_id,
            location=location,
        )

        await equipment.fetch_related("current_status")

        return EquipmentResponseSchema(
            id=equipment.id,
            name=equipment.name,
            current_status_name=equipment.current_status.name if equipment.current_status else EquipmentStatusEnum.OFFLINE,
            location=LocationResponseSchema(id=equipment.location.id, name=equipment.location.name, created_at=equipment.location.created_at) if equipment.location else None,
            last_heartbeat=equipment.last_heartbeat,
            created_at=equipment.created_at
        )

    @override
    @classmethod
    async def patch_equipment(
            cls,
            equipment_id: UUID,
            equipment_data: EquipmentUpdateSchema,
    ) -> EquipmentResponseSchema | None:

        equipment = await Equipment.get_or_none(id=equipment_id).select_related('current_status')

        if not equipment:
            return None

        fields_to_update: list[str] = []

        if equipment_data.name and equipment_data.name != equipment.name:
            existing = await Equipment.get_or_none(name=equipment_data.name)
            if existing and existing.id != equipment.id:
                return None
            equipment.name = equipment_data.name
            fields_to_update.append("name")

        if equipment_data.current_status_id is not None:
            equipment.current_status_id = equipment_data.current_status_id
            fields_to_update.append("current_status_id")

        if equipment_data.location is not None:
            equipment.location = equipment_data.location
            fields_to_update.append("location")

        if equipment_data.last_heartbeat is not None:
            equipment.last_heartbeat = equipment_data.last_heartbeat
            fields_to_update.append("last_heartbeat")

        if fields_to_update:
            await equipment.save(update_fields=fields_to_update)
        await equipment.fetch_related("current_status")

        return EquipmentResponseSchema(
            id=equipment.id,
            name=equipment.name,
            current_status_name=equipment.current_status.name if equipment.current_status else EquipmentStatusEnum.OFFLINE,
            location=None,
            last_heartbeat=equipment.last_heartbeat,
            created_at=equipment.created_at
        )

    @override
    @classmethod
    async def delete_equipment(
            cls,
            equipment_id: UUID
    ) -> None:

        equipment = await Equipment.get_or_none(id=equipment_id)

        if not equipment:
            return None

        return await equipment.delete()

    @classmethod
    async def _fetch_and_map_status_logs(
            cls,
            equipment_id: UUID | None = None
    ) -> list[EquipmentStatusLogResponseSchema]:
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
    async def get_equipment_availability(cls, equipment_id: UUID) -> bool:

        status_filter = Q(current_status__name=EquipmentStatusEnum.AVAILABLE)
        equipment_filter = Q(id=equipment_id)

        return ( await Equipment
            .filter(status_filter & equipment_filter)
            .select_related("current_status")
            .exists()
        )

    @override
    @classmethod
    async def get_equipment_status_logs(cls) -> list[EquipmentStatusLogResponseSchema]:
        """
        Retrieves a list of all equipment status logs from the database.
        """
        return await cls._fetch_and_map_status_logs()

    @override
    @classmethod
    async def get_specific_equipment_status_logs(
            cls,
            equipment_id: UUID,
    ) -> list[EquipmentStatusLogResponseSchema]:
        """
        Retrieves a list of specific equipment status logs from the database.
        """
        return await cls._fetch_and_map_status_logs(equipment_id=equipment_id)

