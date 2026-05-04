import asyncio
import json
from uuid import UUID

from app.core.config import mqtt
from app.database import EquipmentStatus, Equipment, EquipmentStatusLog
from app.schemas.command_schemas import CommandPayloadSchema, CommandTypeEnum
from app.schemas.equipment_schemas import EquipmentStatusEnum


def on_connect(client, flags, rc, properties):
    print("[MQTT] Connected. Subscribing...")
    client.subscribe("equipments/+/status")
    client.subscribe("equipments/+/feedback")
    client.subscribe("equipments/+/commands")

mqtt.on_connect = on_connect

def publish_command(equipment_id: UUID, command: CommandPayloadSchema):
    topic = f"equipments/{equipment_id}/commands"
    mqtt.publish(topic, json.dumps(command))
    print(f"[MQTT] Command published for {topic}: {command}")


async def on_message(client, topic, payload, qos, properties):
    print(f"[MQTT] Message received - Topic: {topic}")

    if "commands" in topic:
        await handle_command_message(topic, payload)
    elif "status" in topic:
        await handle_status_message(topic, payload)
    elif "feedback" in topic:
        await handle_feedback_message(topic, payload)
    else:
        print("[MQTT] Topic not recognized.")

mqtt.on_message = on_message

async def handle_command_message(topic: str, payload: bytes):
    try:
        equipment_id = UUID(topic.split("/")[1])
        message = json.loads(payload.decode())
        command_type_str = message.get("command_type")
        command_type_enum = CommandTypeEnum(command_type_str)
        command_payload = message.get("payload")

        print(f"[COMMAND] {command_type_str} received for equipment {equipment_id}: payload {command_payload}")

        # Define behavior based on the command type
        await simulate_command_behavior(equipment_id, command_type_enum, command_payload)

    except Exception as e:
        print(f"[ERROR] Failed to process command: {e}")


async def simulate_command_behavior(equipment_id: UUID, command_type: CommandTypeEnum, payload: str):
    command_behaviors = {
        CommandTypeEnum.START: (10, f"Equipment started: {payload}"),
        CommandTypeEnum.STOP: (5, f"Equipment stopped: {payload}"),
        CommandTypeEnum.TURN_ON: (3, f"Equipment turned on: {payload}"),
        CommandTypeEnum.TURN_OFF: (3, f"Equipment turned off: {payload}"),
        CommandTypeEnum.ACTION: (20, f"Action executed: {payload}"),
        CommandTypeEnum.RESTART: (15, f"Equipment restarted: {payload}")
    }

    duration, message = command_behaviors.get(command_type, (5, f"Unknown command: {command_type}"))

    # Publish status as occupied
    publish_status(equipment_id, EquipmentStatusEnum.OCCUPIED)
    print(f"[STATUS] Equipment {equipment_id} → Occupied")

    # Wait for execution time
    await asyncio.sleep(duration)

    # Publish status as available
    publish_status(equipment_id, EquipmentStatusEnum.AVAILABLE)
    print(f"[STATUS] Equipment {equipment_id} → Available")

    # Publish feedback
    feedback = {
        "message": f"{message} (Duration: {duration}s, Equipment: {equipment_id})"
    }
    publish_feedback(equipment_id, f"{message} (Duration: {duration}s, equipmentId: {equipment_id})")
    print(f"[FEEDBACK] {feedback['message']}")


def publish_status(equipment_id: UUID, status: EquipmentStatusEnum):
    topic = f"equipments/{equipment_id}/status"
    payload = json.dumps({"status": status})
    mqtt.publish(topic, payload)


def publish_feedback(equipment_id: UUID, message: str):
    topic = f"equipments/{equipment_id}/feedback"
    payload = json.dumps({"message": message})
    mqtt.publish(topic, payload)


async def handle_status_message(topic: str, payload: bytes):
    print(f"[MQTT] Status: {topic} -> {payload.decode()}")

    equipment_id = UUID(topic.split("/")[1])
    status_json = json.loads(payload.decode())
    status_name = status_json.get("status")

    status_data = await EquipmentStatus.get(name=status_name)
    await Equipment.filter(id=equipment_id).update(current_status_id=status_data.id)

    await EquipmentStatusLog.create(
        equipment_id=equipment_id,
        status=status_data,
        details=None,
    )

    print(f"[DB] Equipment {equipment_id} status updated to {status_name}")


async def handle_feedback_message(topic: str, payload: bytes):
    equipment_id = UUID(topic.split("/")[1])
    feedback_json = json.loads(payload.decode())
    feedback_message = feedback_json.get("message", "")

    last_log = await EquipmentStatusLog.filter(equipment_id=equipment_id).order_by("-reported_at").first()

    if last_log:
        await EquipmentStatusLog.filter(id=last_log.id).update(details=feedback_message)
        print(f"[DB] Feedback saved to log id {last_log.id} for equipment {equipment_id}")
    else:
        print(f"[WARN] No status log found for equipment {equipment_id} to save feedback")
