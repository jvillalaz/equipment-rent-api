from typing import ClassVar
from uuid import UUID

from app.core.exceptions import NotFoundException
from app.interfaces.equipment_interface import IEquipmentService
from app.interfaces.reservation_interface import IReservationService
from app.interfaces.user_interface import IUserService
from app.schemas.reservation_schemas import ReservationStatusResponseSchema, ReservationResponseSchema, \
    ReservationRequestSchema, ReservationUpdateSchema
from tools.application import Service


class ReservationService(Service):
    """
    Service class responsible for reservation-related operations.
    """
    reservation_repository: ClassVar[type[IReservationService]]
    equipment_repository: ClassVar[type[IEquipmentService]]
    user_repository: ClassVar[type[IUserService]]

    def __new__(
        cls,
        reservation_repository: type[IReservationService],
        equipment_repository: type[IEquipmentService],
        user_repository: type[IUserService],
    ):
        cls.reservation_repository = reservation_repository
        cls.equipment_repository = equipment_repository
        cls.user_repository = user_repository
        return cls

    @classmethod
    async def get_reservation_statuses(cls) -> list[ReservationStatusResponseSchema]:
        """
        Returns all possible reservation statuses.
        """
        return await cls.reservation_repository.get_reservation_statuses()

    @classmethod
    async def post_reservation(
            cls,
            reservation_data: ReservationRequestSchema,
    ) -> ReservationResponseSchema:
        """
        Creates a new reservation.
        """
        user_data = await cls.user_repository.get_specific_user(reservation_data.user_id)

        if not user_data:
            raise NotFoundException(detail=f"User with id '{reservation_data.user_id}' not found")

        equipment_data = await cls.equipment_repository.get_specific_equipment(reservation_data.equipment_id)

        if not equipment_data:
            raise NotFoundException(detail=f"Equipment with id '{reservation_data.equipment_id}' not found")

        return await cls.reservation_repository.post_reservation(reservation_data)

    @classmethod
    async def get_reservations(cls) -> list[ReservationResponseSchema]:
        """
        Lists all reservations.
        """
        return await cls.reservation_repository.get_reservations()

    @classmethod
    async def get_specific_reservation(
            cls,
            reservation_id: UUID,
    ) -> ReservationResponseSchema:
        """
        Retrieves a specific reservation by its ID.
        """
        reservation_response = await cls.reservation_repository.get_specific_reservation(reservation_id)

        if not reservation_response:
            raise NotFoundException(detail=f"Reservation '{reservation_id}' not found")

        return reservation_response

    @classmethod
    async def get_specific_reservation_status(
            cls,
            status_id: UUID,
    ) -> ReservationStatusResponseSchema:
        """
        Validates the existence of a reservation status raises NotFoundException if not found.
        """
        status_exists = await cls.reservation_repository.get_specific_reservation_status(status_id)

        if not status_exists:
            raise NotFoundException(detail=f"Reservation status {status_id} not found")

        return status_exists

    @classmethod
    async def patch_reservation(
            cls,
            reservation_id: UUID,
            reservation_data: ReservationUpdateSchema,
    ) -> ReservationResponseSchema:
        """
        Updates the status of a specific reservation identified by its UUID.
        """
        _ = await cls.get_specific_reservation(reservation_id)
        _ = await cls.get_specific_reservation_status(reservation_data.status_id)
        result = await cls.reservation_repository.patch_reservation(reservation_id, reservation_data)
        if result is None:
            raise NotFoundException(detail=f"Reservation '{reservation_id}' not found")
        return result

    @classmethod
    async def delete_reservation(
            cls,
            reservation_id: UUID
    ) -> None:
        """
        Cancels the specified reservation by setting its status to "Canceled".
        """
        _ = await cls.get_specific_reservation(reservation_id)
        return await cls.reservation_repository.delete_reservation(reservation_id)
