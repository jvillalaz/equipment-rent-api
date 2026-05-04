from abc import ABC, abstractmethod
from uuid import UUID

from app.schemas.reservation_schemas import ReservationStatusResponseSchema, ReservationRequestSchema, \
    ReservationResponseSchema, ReservationUpdateSchema


class IReservationService(ABC):
    """
    Interface class responsible for reservation-related operations.
    """
    @classmethod
    @abstractmethod
    async def get_reservation_statuses(cls) -> list[ReservationStatusResponseSchema]:
        """
         Returns all possible reservation statuses.
        """
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    async def post_reservation(
            cls,
            reservation_data: ReservationRequestSchema,
    ) -> ReservationResponseSchema:
        """
        Creates a new reservation.
        """
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    async def get_reservations(cls) -> list[ReservationResponseSchema]:
        """
        Lists all reservations.
        """
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    async def get_specific_reservation(
            cls,
            reservation_id: UUID,
    ) -> ReservationResponseSchema | None:
        """
        Retrieves a specific reservation by its ID.
        """
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    async def get_specific_reservation_status(
            cls,
            status_id: UUID,
    ) -> ReservationStatusResponseSchema | None:
        """
        Retrieves a reservation status by its status_id.
        """
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    async def patch_reservation(
            cls,
            reservation_id: UUID,
            reservation_data: ReservationUpdateSchema,
    ) -> ReservationResponseSchema:
        """
        Updates the status of a specific reservation identified by its UUID.
        """
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    async def delete_reservation(
            cls,
            reservation_id: UUID
    ) -> None:
        """
        Cancels the specified reservation by setting its status to "Canceled".
        """
        raise NotImplementedError()
