from typing import List, Optional
from uuid import UUID

from app.interfaces.reservation_interface import IReservationService
from app.database import ReservationStatus, Reservation
from app.schemas.reservation_schemas import ReservationResponseSchema, ReservationUpdateSchema, \
    ReservationRequestSchema, ReservationStatusResponseSchema


class ReservationPersistence(IReservationService):
    """
    Persistence class responsible for equipment-related operations.
    """

    @classmethod
    async def get_reservation_statuses(cls) -> List[ReservationStatusResponseSchema]:
        """
        Returns all possible reservation statuses.
        """
        statuses = await ReservationStatus.all().order_by("created_at")
        response: List[ReservationStatusResponseSchema] = []

        for reservation_status in statuses:
            response.append(ReservationStatusResponseSchema(
                id=reservation_status.id,
                name=reservation_status.name,
                created_at=reservation_status.created_at
            ))

        return response

    @classmethod
    async def post_reservation(
            cls,
            reservation_data: ReservationRequestSchema,
    ) -> ReservationResponseSchema:
        """
        Creates a new reservation.
        """

        # Set reservation status to default "Active"
        reservation_status = await ReservationStatus.get_or_none(name="Active")

        # Create reservation record
        reservation = await Reservation.create(
            user_id=reservation_data.user_id,
            equipment_id=reservation_data.equipment_id,
            status_id=reservation_status.id,
        )

        # Return response schema
        return ReservationResponseSchema(
            id=reservation.id,
            user_name=reservation.user.name,
            equipment_name=reservation.equipment.name,
            start_time=reservation.start_time,
            end_time=reservation.end_time,
            status_name=reservation.status.name,
            created_at=reservation.created_at,
        )

    @classmethod
    async def get_reservations(cls) -> List[ReservationResponseSchema]:
        """
        Lists all reservations.
        """
        reservations = Reservation.all().prefetch_related('user', 'equipment', 'status')
        result: List[ReservationResponseSchema] = []

        async for reservation in reservations:
            result.append(
                ReservationResponseSchema(
                    id=reservation.id,
                    user_name=reservation.user.name,
                    equipment_name=reservation.equipment.name,
                    start_time=reservation.start_time,
                    end_time=reservation.end_time,
                    status_name=reservation.status.name,
                    created_at=reservation.created_at,
                )
            )

        return result

    @classmethod
    async def get_specific_reservation(
            cls,
            reservation_id: UUID,
    ) -> Optional[ReservationResponseSchema]:
        """
        Retrieves a specific reservation by its ID.
        """
        reservation = await Reservation.get_or_none(id=reservation_id).prefetch_related('user', 'equipment', 'status')

        if not reservation:
            return None

        return ReservationResponseSchema(
            id=reservation.id,
            user_name=reservation.user.name,
            equipment_name=reservation.equipment.name,
            start_time=reservation.start_time,
            end_time=reservation.end_time,
            status_name=reservation.status.name,
            created_at=reservation.created_at,
        )

    @classmethod
    async def get_specific_reservation_status(
            cls,
            status_id: UUID,
    ) -> Optional[ReservationStatusResponseSchema]:
        """
        Retrieves a reservation status by its status_id.
        """
        reservation_status = await ReservationStatus.get_or_none(id=status_id)

        if not reservation_status:
            return None

        reservation_response = ReservationStatusResponseSchema(
            id=reservation_status.id,
            name=reservation_status.name,
            created_at=reservation_status.created_at
        )

        return reservation_response

    @classmethod
    async def patch_reservation(
            cls,
            reservation_id: UUID,
            reservation_data: ReservationUpdateSchema,
    ) -> ReservationResponseSchema:
        """
        Updates the status of a specific reservation identified by its UUID.
        """
        reservation = await Reservation.get_or_none(id=reservation_id)
        reservation.status_id = reservation_data.status_id
        await reservation.save(update_fields=["status_id"])

        reservation_response = ReservationResponseSchema(
            id=reservation.id,
            user_name=reservation.user.name,
            equipment_name=reservation.equipment.name,
            start_time=reservation.start_time,
            end_time=reservation.end_time,
            status_name=reservation.status.name,
            created_at=reservation.created_at,
        )

        return reservation_response

    @classmethod
    async def delete_reservation(
            cls,
            reservation_id: UUID
    ) -> None:
        """
        Cancels the specified reservation by setting its status to "Canceled".
        """
        reservation = await Reservation.get_or_none(id=reservation_id)
        canceled_status = await ReservationStatus.get_or_none(name="Canceled")
        reservation.status_id = canceled_status.id
        await reservation.save(update_fields=["status_id"])
        return None
