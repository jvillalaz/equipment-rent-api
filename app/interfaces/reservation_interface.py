from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from app.schemas.reservation_schemas import ReservationStatusResponseSchema, ReservationRequestSchema, \
    ReservationResponseSchema, ReservationUpdateSchema


class IReservationService(ABC):
    """
    Interface class responsible for reservation-related operations.
    """
    @classmethod
    @abstractmethod
    async def get_reservation_statuses(cls) -> List[ReservationStatusResponseSchema]:
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
    async def get_reservations(cls) -> List[ReservationResponseSchema]:
        """
        Lists all reservations.
        """
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    async def get_specific_reservation(
            cls,
            reservation_id: UUID,
    ) -> Optional[ReservationResponseSchema]:
        """
        Retrieves a specific reservation by its ID.
        """
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    async def get_specific_reservation_status(
            cls,
            status_id: UUID,
    ) -> Optional[ReservationStatusResponseSchema]:
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
