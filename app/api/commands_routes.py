from typing import List
from uuid import UUID

from fastapi import APIRouter, status, Body, Path

from app.schemas.command_schemas import CommandRequestSchema, CommandResponseSchema, CommandTypeResponseSchema
from app.services.command_service import CommandService

commands_router = APIRouter(
    prefix="/commands",
    tags=["Commands"]
)

@commands_router.get(
    "/available-types",
    response_model=List[CommandTypeResponseSchema]
)
async def get_command_types() -> List[CommandTypeResponseSchema]:
    """
    Retrieves all available command types that can be issued to equipment.
    \f
    :return: List of all available command types.
    """
    return await CommandService.get_command_types()


@commands_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=CommandResponseSchema,
    summary="Send command to equipment",
    description="Sends a command to an equipment via MQTT. "
                "Requires equipment_id, command_type_id, and optional payload."
)
async def post_command(
        command_data: CommandRequestSchema = Body(..., description="Data information of the command solicitation."),
) -> CommandResponseSchema:
    """
    Post a command to equipment.
    \f
    :param command_data: Data information of the command solicitation.
    """
    return await CommandService.post_command(command_data)


@commands_router.get(
    "",
    status_code=status.HTTP_200_OK,
    summary="List all commands",
    description="Returns all commands sent."
)
async def get_commands():
    """
    Retrieves the list of all commands that have been executed in the system.
    """
    return await CommandService.get_commands()


@commands_router.get(
    "/{commandId}",
    status_code=status.HTTP_200_OK,
    summary="Get command details",
    description="Returns details of a specific command."
)
async def get_specific_command(
        command_id: UUID = Path(..., description="Unique identifier of the command.", alias="commandId"),
):
    """
    Retrieves a specific command that have been executed in the system.
    \f
    :param command_id: Unique identifier of the command.
    """
    return await CommandService.get_specific_command(command_id)
