from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "CommandTypes" (
    "id" UUID NOT NULL PRIMARY KEY,
    "name" VARCHAR(60) NOT NULL UNIQUE,
    "created_at" TIMESTAMPTZ NOT NULL
);
COMMENT ON TABLE "CommandTypes" IS 'Defines the different types of commands that can be sent to equipment.';
CREATE TABLE IF NOT EXISTS "EquipmentStatuses" (
    "id" UUID NOT NULL PRIMARY KEY,
    "name" VARCHAR(60) NOT NULL UNIQUE,
    "created_at" TIMESTAMPTZ NOT NULL
);
COMMENT ON TABLE "EquipmentStatuses" IS 'Stores information about the system''s users.';
CREATE TABLE IF NOT EXISTS "location" (
    "id" UUID NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL UNIQUE,
    "created_at" TIMESTAMPTZ NOT NULL
);
CREATE TABLE IF NOT EXISTS "Equipments" (
    "id" UUID NOT NULL PRIMARY KEY,
    "name" VARCHAR(60) NOT NULL UNIQUE,
    "last_heartbeat" TIMESTAMPTZ NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL,
    "current_status_id" UUID REFERENCES "EquipmentStatuses" ("id") ON DELETE CASCADE,
    "location_id" UUID UNIQUE REFERENCES "location" ("id") ON DELETE SET NULL
);
COMMENT ON TABLE "Equipments" IS 'Stores the equipment available in the system.';
CREATE TABLE IF NOT EXISTS "Commands" (
    "id" UUID NOT NULL PRIMARY KEY,
    "payload" VARCHAR(200),
    "created_at" TIMESTAMPTZ NOT NULL,
    "command_type_id" UUID NOT NULL REFERENCES "CommandTypes" ("id") ON DELETE CASCADE,
    "equipment_id" UUID NOT NULL REFERENCES "Equipments" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "Commands" IS 'Records commands sent to equipment.';
CREATE TABLE IF NOT EXISTS "EquipmentStatusLogs" (
    "id" UUID NOT NULL PRIMARY KEY,
    "details" VARCHAR(300),
    "reported_at" TIMESTAMPTZ NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL,
    "equipment_id" UUID NOT NULL REFERENCES "Equipments" ("id") ON DELETE CASCADE,
    "status_id" UUID NOT NULL REFERENCES "EquipmentStatuses" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "EquipmentStatusLogs" IS 'Stores the status change logs of the equipment.';
CREATE TABLE IF NOT EXISTS "ReservationStatuses" (
    "id" UUID NOT NULL PRIMARY KEY,
    "name" VARCHAR(60) NOT NULL UNIQUE,
    "created_at" TIMESTAMPTZ NOT NULL
);
COMMENT ON TABLE "ReservationStatuses" IS 'Stores the different statuses of a reservation.';
CREATE TABLE IF NOT EXISTS "Users" (
    "id" UUID NOT NULL PRIMARY KEY,
    "name" VARCHAR(60) NOT NULL,
    "email" VARCHAR(60) NOT NULL UNIQUE,
    "is_active" BOOL NOT NULL DEFAULT True,
    "created_at" TIMESTAMPTZ NOT NULL
);
COMMENT ON TABLE "Users" IS 'Stores information about the system''s users.';
CREATE TABLE IF NOT EXISTS "Reservations" (
    "id" UUID NOT NULL PRIMARY KEY,
    "start_time" TIMESTAMPTZ NOT NULL,
    "end_time" TIMESTAMPTZ NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL,
    "equipment_id" UUID NOT NULL REFERENCES "Equipments" ("id") ON DELETE CASCADE,
    "status_id" UUID NOT NULL REFERENCES "ReservationStatuses" ("id") ON DELETE CASCADE,
    "user_id" UUID NOT NULL REFERENCES "Users" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "Reservations" IS 'Stores information about reservations made by users.';
CREATE TABLE IF NOT EXISTS "UserAuth" (
    "id" UUID NOT NULL PRIMARY KEY,
    "username" VARCHAR(60) NOT NULL UNIQUE,
    "password_hash" VARCHAR(100) NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL,
    "user_id" UUID NOT NULL REFERENCES "Users" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "UserAuth" IS 'Stores user credential information.';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "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"
)
