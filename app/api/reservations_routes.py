from typing import List
from uuid import UUID

from fastapi import APIRouter, status, Body, Path

from app.schemas.reservation_schemas import ReservationStatusResponseSchema, ReservationRequestSchema, \
    ReservationResponseSchema, ReservationUpdateSchema
from app.services.reservation_service import ReservationService

reservations_router = APIRouter(
    prefix="/reservations",
    tags=["Reservations"]
)


@reservations_router.get(
    "/status-reservation",
    response_model=List[ReservationStatusResponseSchema],
    status_code=status.HTTP_200_OK,
    summary="List reservation statuses",
    description="Returns all reservation statuses."
)
async def get_reservation_statuses() -> List[ReservationStatusResponseSchema]:
    """
    Returns all possible reservation statuses.
    """
    return await ReservationService.get_reservation_statuses()


@reservations_router.post(
    "",
    response_model=ReservationResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new reservation",
    description="Creates a new equipment reservation."
)
async def post_reservation(
        reservation_data: ReservationRequestSchema = Body(..., description="Data information of the reservation."),
) -> ReservationResponseSchema:
    """
    Creates a new reservation.
    """
    return await ReservationService.post_reservation(reservation_data)


@reservations_router.get(
    "",
    response_model=List[ReservationResponseSchema],
    status_code=status.HTTP_200_OK,
    summary="List all reservations",
    description="Returns a list of all reservations."
)
async def get_reservations():
    """
    Lists all reservations.
    """
    return await ReservationService.get_reservations()


@reservations_router.get(
    "/{reservationId}",
    response_model=ReservationResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Get reservation details",
    description="Returns details of a specific reservation by reservation_id."
)
async def get_specific_reservation(
        reservation_id: UUID = Path(..., description="Unique identifier of the reservation.", alias="reservationId"),
):
    """
    Retrieves details of the specified reservation.
    """
    return await ReservationService.get_specific_reservation(reservation_id)


@reservations_router.patch(
    "/{reservationId}",
    response_model=ReservationResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Update reservation status",
    description="Updates the status of a reservation."
)
async def patch_reservation(
        reservation_id: UUID = Path(..., description="Unique identifier of the reservation.", alias="reservationId"),
        reservation_data: ReservationUpdateSchema = Body(...,
                                                         description="Data to update the status of a reservation."),
) -> ReservationResponseSchema:
    """
    Updates the status of the specified reservation.
    \f
    :param reservation_id: Unique identifier of the reservation.
    :param reservation_data: Data to update the status of a reservation.
    """
    return await ReservationService.patch_reservation(reservation_id, reservation_data)


@reservations_router.delete(
    "/{reservationId}",
    response_model=None,
    status_code=status.HTTP_200_OK,
    summary="Cancel reservation",
    description="Cancels a reservation."
)
async def delete_reservation(
        reservation_id: UUID = Path(..., description="Unique identifier of the reservation.", alias="reservationId"),
) -> None:
    """
    Cancels the specified reservation.
    \f
    :param reservation_id: Unique identifier of the reservation.
    """
    return await ReservationService.delete_reservation(reservation_id)
