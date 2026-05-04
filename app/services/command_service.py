from typing import Type, List
from uuid import UUID

from app.core.exceptions import NotFoundException
from app.interfaces.command_interface import ICommandService
from app.schemas.command_schemas import CommandRequestSchema, CommandResponseSchema, CommandTypeRequestSchema, \
    CommandTypeResponseSchema
from app.services.equipment_service import EquipmentService
from tools.application import Service


class CommandService(Service):
    command_repository: Type[ICommandService]
    equipment_service: Type[EquipmentService]

    def __new__(
            cls,
            command_repository: Type[ICommandService],
            equipment_service: Type[EquipmentService],
    ):
        # Assign the equipment repository implementation to the class.
        cls.command_repository = command_repository
        cls.equipment_service = equipment_service
        return cls

    @classmethod
    async def get_command_types(cls) -> List[CommandTypeResponseSchema]:
        """
        Retrieves all available command types.
        """
        return await cls.command_repository.get_command_types()

    @classmethod
    async def post_command(
            cls,
            command_data: CommandRequestSchema,
    ) -> CommandResponseSchema:
        """
        Validates the existence of the equipment and create/post command.
        """
        equipment_data = await cls.equipment_service.get_specific_equipment(command_data.equipment_id)

        if not equipment_data:
            raise NotFoundException(detail=f"Equipment with id '{equipment_data.equipment_id}' not found")

        return await cls.command_repository.post_command(command_data)

    @classmethod
    async def get_commands(
            cls
    ) -> List[CommandResponseSchema]:
        """
        Retrieves the list of all commands that have been executed in the system.
        """
        return await cls.command_repository.get_commands()

    @classmethod
    async def get_specific_command(
            cls,
            command_id: UUID,
    ) -> CommandResponseSchema:
        """
        Retrieves a specific command that have been executed in the system.
        """
        command_response = await cls.command_repository.get_specific_command(command_id)

        if not command_response:
            raise NotFoundException(detail=f"Command with ID '{command_id}' not found")

        return command_response
