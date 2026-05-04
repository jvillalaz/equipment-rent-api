from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import Field

from tools.application import DTO


class CommandTypeRequestSchema(DTO):
    """
    Request schema for creating a new command type.
    """
    name: str = Field(..., max_length=60, description="Name of the command type")


class CommandTypeResponseSchema(DTO):
    """
    Response schema for newly created command type.
    """
    id: UUID = Field(..., description="Unique identifier of the command type")
    name: str = Field(..., description="Name of the command type")
    created_at: datetime = Field(..., description="Timestamp when the command type was created")


class CommandTypeEnum(str, Enum):
    """
    Enum representing the possible command types for equipment control.
    \f
    :param START: Command to start the equipment.
    :param STOP: Command to stop the equipment.
    :param TURN_ON: Command to turn on the equipment.
    :param TURN_OFF: Command to turn off the equipment.
    :param ACTION: Command to set a parameter on the equipment.
    :param RESTART: Command to restart the equipment.
    """
    START = "Start"
    STOP = "Stop"
    TURN_ON = "Turn On"
    TURN_OFF = "Turn Off"
    ACTION = "Action"
    RESTART = "Restart"


class CommandPayloadSchema(DTO):
    """
    Model representing the payload for commands.
    """
    command_type: CommandTypeEnum = Field(..., description="Name of the command type")
    payload: Optional[str] = Field(None, description="Command payload as a string")


class CommandRequestSchema(DTO):
    """
    Request schema for creating a new command solicitation.
    """
    equipment_id: UUID = Field(..., description="Unique identifier of the equipment that received the command")
    command_type_id: UUID = Field(..., description="Unique identifier of the command type")
    payload: Optional[str] = Field(None, description="Optional command payload sent to the equipment")


class CommandResponseSchema(DTO):
    """
    Response schema for newly created command solicitation.
    """
    id: UUID = Field(..., description="Unique identifier for the command solicitation")
    equipment_id: UUID = Field(..., description="Unique identifier of the equipment that received the command")
    equipment_name: str = Field(..., description="Name of the equipment that received the command")
    command_type_id: UUID = Field(..., description="Unique identifier of the command type")
    command_name: str = Field(..., description="Name of the command solicitation")
    payload: Optional[str] = Field(None, description="Optional command payload sent to the equipment")
    created_at: datetime = Field(..., description="Timestamp of command solicitation creation")
