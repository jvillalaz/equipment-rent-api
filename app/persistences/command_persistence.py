from typing import List, Optional
from uuid import UUID

from app.database import CommandType, Command
from app.interfaces.command_interface import ICommandService
from app.mqqt_client.mqtt_service import publish_command
from app.schemas.command_schemas import CommandTypeResponseSchema, CommandRequestSchema, CommandResponseSchema, \
    CommandPayloadSchema


class CommandPersistence(ICommandService):
    """
    Persistence class responsible for authentication-related operations.
    """
    @classmethod
    async def get_command_types(cls) -> List[CommandTypeResponseSchema]:
        """R
        Retrieves all available command types.
        """
        command_types = await CommandType.all()
        commands_list: List[CommandTypeResponseSchema] = []

        for command in command_types:
            command_response = CommandTypeResponseSchema(
                id=command.id,
                name=command.name,
                created_at=command.created_at,
            )
            commands_list.append(command_response)

        return commands_list

    @classmethod
    async def post_command(
            cls,
            command_data: CommandRequestSchema,
    ) -> CommandResponseSchema:
        """
        Creates a new command record in the database and publishes it to the corresponding MQTT topic.
        """
        # Save command to database
        command = await Command.create(
            equipment_id=command_data.equipment_id,
            command_type_id=command_data.command_type_id,
            payload=command_data.payload
        )

        # Retrieves the command name type
        command_type = await CommandType.get(id=command_data.command_type_id)

        # Define payload for publish
        command_payload = CommandPayloadSchema(
            command_type=command_type.name,
            payload=command_data.payload
        )

        # Publish command to MQTT using helper
        publish_command(command_data.equipment_id, command_payload.model_dump())

        # Fetch relations to use .name
        await command.fetch_related("equipment", "command_type")

        # Return response schema
        return CommandResponseSchema(
            id=command.id,
            equipment_id=command.equipment_id,
            equipment_name=command.equipment.name,
            command_type_id=command.command_type_id,
            command_name=command.command_type.name,
            payload=command.payload,
            created_at=command.created_at
        )

    @classmethod
    async def get_commands(
            cls
    ) -> List[CommandResponseSchema]:
        """
        Retrieves the list of all commands that have been executed in the system.
        """
        commands = await Command.all().prefetch_related("command_type", "equipment")

        commands_list = []
        for cmd in commands:
            command_schema = CommandResponseSchema(
                id=cmd.id,
                equipment_id=cmd.equipment_id,
                equipment_name=cmd.equipment.name,
                command_type_id=cmd.command_type_id,
                command_name=cmd.command_type.name,
                payload=cmd.payload,
                created_at=cmd.created_at
            )
            commands_list.append(command_schema)

        return commands_list

    @classmethod
    async def get_specific_command(
            cls,
            command_id: UUID,
    ) -> Optional[CommandResponseSchema]:
        cmd = await Command.get_or_none(id=command_id).prefetch_related("command_type", "equipment")

        if not cmd:
            return None

        command_schema = CommandResponseSchema(
            id=cmd.id,
            equipment_id=cmd.equipment_id,
            equipment_name=cmd.equipment.name,
            command_type_id=cmd.command_type_id,
            command_name=cmd.command_type.name,
            payload=cmd.payload,
            created_at=cmd.created_at
        )

        return command_schema
