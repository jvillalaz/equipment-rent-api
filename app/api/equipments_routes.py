from typing import List
from uuid import UUID

from fastapi import APIRouter, status, Path, Body

from app.schemas.equipment_schemas import EquipmentResponseSchema, \
    EquipmentRequestSchema, EquipmentUpdateSchema
from app.services.equipment_service import EquipmentService

equipments_router = APIRouter(
    prefix="/equipments",
    tags=["Equipments"]
)

@equipments_router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=List[EquipmentResponseSchema],
    summary="List all equipments",
    description="Returns a list of all registered equipments."
)
async def get_equipments() -> List[EquipmentResponseSchema]:
    """
    Returns a list of all registered equipments.
    """
    return await EquipmentService.get_equipments()


@equipments_router.get(
    "/{equipmentId}",
    status_code=status.HTTP_200_OK,
    response_model=EquipmentResponseSchema,
    summary="Get equipment details",
    description="Returns details of a specific equipment by equipment_id."
)
async def get_specific_equipment(
        equipment_id: UUID = Path(..., description="Unique identifier of the equipment.", alias="equipmentId"),
) -> EquipmentResponseSchema:
    """
    Retrieves details of the specified equipment.
    \f
    :param equipment_id: Unique identifier of the equipment.
    """
    return await EquipmentService.get_specific_equipment(equipment_id)


@equipments_router.post(
    "",
    response_model=EquipmentResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Add new equipment",
    description="Adds a new equipment to the system."
)
async def post_equipment(
        equipment_data: EquipmentRequestSchema = Body(..., description="Data information of the equipment."),
) -> EquipmentResponseSchema:
    """
    Creates a new equipment.
    \f
    :param equipment_data: Data information of the equipment.
    """
    return await EquipmentService.post_equipment(equipment_data)


@equipments_router.patch(
    "/{equipmentId}",
    response_model=EquipmentResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Update equipment",
    description="Updates equipment data such as name or location."
)
async def patch_equipment(
        equipment_id: UUID = Path(..., description="Unique identifier of the equipment.", alias="equipmentId"),
        equipment_data: EquipmentUpdateSchema = Body(..., description="Data information of the equipment."),
):
    """
    Updates the specified equipment.
    \f
    :param equipment_id: Unique identifier of the equipment.
    :param equipment_data: Data information of the equipment.
    """
    return await EquipmentService.patch_equipment(equipment_id, equipment_data)


@equipments_router.delete(
    "/{equipmentId}",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete equipment",
    description="Removes an equipment from the system."
)
async def delete_equipment(
        equipment_id: UUID = Path(..., description="Unique identifier of the equipment.", alias="equipmentId"),
):
    """
    Deletes the specified equipment.
    \f
    :param equipment_id: Unique identifier of the equipment.
    """
    return await EquipmentService.delete_equipment(equipment_id)


@equipments_router.get(
    "/{equipmentId}/status",
    status_code=status.HTTP_200_OK,
    summary="Get equipment current status",
    description="Returns the current status of the specified equipment."
)
async def get_equipment_status(
        equipment_id: str = Path(..., description="Unique identifier of the equipment.", alias="equipmentId"),
):
    """
    Retrieves current status of the equipment.
    """
    return f"get status for equipment {equipment_id}"
