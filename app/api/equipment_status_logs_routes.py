from typing import List
from uuid import UUID

from fastapi import APIRouter, status, Path

from app.schemas.equipment_status_log_schemas import EquipmentStatusLogResponseSchema
from app.services.equipment_service import EquipmentService


equipment_status_logs_router = APIRouter(
    prefix="/equipment-status-logs",
    tags=["EquipmentStatusLogs"]
)


@equipment_status_logs_router.get(
    "",
    response_model=List[EquipmentStatusLogResponseSchema],
    status_code=status.HTTP_200_OK,
    summary="List all equipment status logs",
    description="Returns all equipment status logs."
)
async def get_equipment_status_logs() -> List[EquipmentStatusLogResponseSchema]:
    """
    Lists all equipment status logs.
    """
    return await EquipmentService.get_equipment_status_logs()


@equipment_status_logs_router.get(
    "/{equipmentId}",
    response_model=List[EquipmentStatusLogResponseSchema],
    status_code=status.HTTP_200_OK,
    summary="Get status logs for a specific equipment",
    description="Returns status logs for the specified equipment."
)
async def get_specific_equipment_status_logs(
        equipment_id: UUID = Path(..., description="Unique identifier of the equipment.", alias="equipmentId"),
) -> List[EquipmentStatusLogResponseSchema]:
    """
    Retrieves status logs for a specific equipment.
    """
    return await EquipmentService.get_specific_equipment_status_logs(equipment_id)
