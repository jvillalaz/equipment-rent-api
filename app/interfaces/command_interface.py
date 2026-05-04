from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from app.schemas.command_schemas import CommandRequestSchema, CommandResponseSchema, CommandTypeResponseSchema


class ICommandService(ABC):
    """
    Interface class responsible for command-related operations.
    """
    @classmethod
    @abstractmethod
    async def get_command_types(cls) -> List[CommandTypeResponseSchema]:
        """
        Retrieves all available command types.
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def post_command(
            cls,
            command_data: CommandRequestSchema,
    ) -> CommandResponseSchema:
        """
        Validates the existence of the equipment and create/post command.
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def get_commands(
            cls
    ) -> List[CommandResponseSchema]:
        """
        Retrieves the list of all commands that have been executed in the system.
        """
        raise NotImplementedError
    @classmethod
    @abstractmethod
    async def get_specific_command(
            cls,
            command_id: UUID,
    ) -> Optional[CommandResponseSchema]:
        """
        Retrieves a specific command that have been executed in the system.
        """
        raise NotImplementedError
