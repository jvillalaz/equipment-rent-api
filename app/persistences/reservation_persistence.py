from datetime import datetime

from typing_extensions import override
from uuid import UUID

from app.interfaces.reservation_interface import IReservationService
from app.database import ReservationStatus, Reservation
from app.schemas.reservation_schemas import ReservationResponseSchema, ReservationStatusEnum, ReservationUpdateSchema, \
    ReservationRequestSchema, ReservationStatusResponseSchema
from tortoise.queryset import Q

class ReservationPersistence(IReservationService):
    """
    Persistence class responsible for equipment-related operations.
    """

    @override
    @classmethod
    async def get_reservation_statuses(cls) -> list[ReservationStatusResponseSchema]:
        """
        Returns all possible reservation statuses.
        """
        statuses = await ReservationStatus.all().order_by("created_at")
        response: list[ReservationStatusResponseSchema] = []

        for reservation_status in statuses:
            response.append(ReservationStatusResponseSchema(
                id=reservation_status.id,
                name=reservation_status.name,
                created_at=reservation_status.created_at
            ))

        return response

    @override
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

        if not reservation_status:
            raise ValueError("Reservation status 'Active' not found. Run seeds first.")

        # Create reservation record
        reservation = await Reservation.create(
            user_id=reservation_data.user_id,
            equipment_id=reservation_data.equipment_id,
            status_id=reservation_status.id,
            start_time=reservation_data.start_time,
            end_time=reservation_data.end_time
        )

        await reservation.fetch_related("user", "equipment", "status")

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
    async def get_specific_reservation_by_equipment(cls, equipment_id: UUID) -> bool:
        return await Reservation.filter(equipment_id=equipment_id).exists()

    @override
    @classmethod
    async def get_reservations(cls) -> list[ReservationResponseSchema]:
        """
        Lists all reservations.
        """
        reservations = Reservation.all().prefetch_related('user', 'equipment', 'status')
        result: list[ReservationResponseSchema] = []

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

    @override
    @classmethod
    async def get_specific_reservation(
            cls,
            reservation_id: UUID,
    ) -> ReservationResponseSchema | None:
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
    async def get_equipment_reservation_status(cls, equipment_id: UUID, started_time: datetime, ended_time: datetime) -> bool:
        print(started_time)
        print(ended_time)

        status_filter = Q(status__name=ReservationStatusEnum.ACTIVE.value)
        range_datetime = Q(start_time__range=(started_time, ended_time))
        equipment_filter = Q(equipment_id=equipment_id)

        return ( await Reservation
            .filter(status_filter & equipment_filter & range_datetime)
            .exists()
        )
        

    @override
    @classmethod
    async def get_specific_reservation_status(
            cls,
            status_id: UUID,
    ) -> ReservationStatusResponseSchema | None:
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
    

    @override
    @classmethod
    async def patch_reservation(
            cls,
            reservation_id: UUID,
            reservation_data: ReservationUpdateSchema,
    ) -> ReservationResponseSchema | None:
        """
        Updates the status of a specific reservation identified by its UUID.
        """
        reservation = await Reservation.get_or_none(id=reservation_id).prefetch_related("user", "equipment", "status")

        if not reservation:
            return None

        reservation.status_id = reservation_data.status_id
        await reservation.save(update_fields=["status_id"])
        await reservation.fetch_related("status")

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

    @override
    @classmethod
    async def delete_reservation(
            cls,
            reservation_id: UUID
    ) -> None:
        """
        Cancels the specified reservation by setting its status to "Canceled".
        """
        reservation = await Reservation.get_or_none(id=reservation_id)

        if not reservation:
            return None

        canceled_status = await ReservationStatus.get_or_none(name="Canceled")

        if not canceled_status:
            return None

        reservation.status_id = canceled_status.id
        await reservation.save(update_fields=["status_id"])
        return None
