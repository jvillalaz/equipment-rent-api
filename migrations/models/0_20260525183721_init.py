from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "CommandTypes" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "name" VARCHAR(60) NOT NULL UNIQUE,
    "created_at" TIMESTAMPTZ NOT NULL
);
COMMENT ON TABLE "CommandTypes" IS 'Defines the different types of commands that can be sent to equipment.';
CREATE TABLE IF NOT EXISTS "EquipmentStatuses" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "name" VARCHAR(60) NOT NULL UNIQUE,
    "created_at" TIMESTAMPTZ NOT NULL
);
COMMENT ON TABLE "EquipmentStatuses" IS 'Stores information about the system''s users.';
CREATE TABLE IF NOT EXISTS "location" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL UNIQUE,
    "created_at" TIMESTAMPTZ NOT NULL
);
CREATE TABLE IF NOT EXISTS "Equipments" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "name" VARCHAR(60) NOT NULL UNIQUE,
    "last_heartbeat" TIMESTAMPTZ NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL,
    "current_status_id" UUID REFERENCES "EquipmentStatuses" ("id") ON DELETE CASCADE,
    "location_id" UUID REFERENCES "location" ("id") ON DELETE SET NULL
);
COMMENT ON TABLE "Equipments" IS 'Stores the equipment available in the system.';
CREATE TABLE IF NOT EXISTS "Commands" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "payload" VARCHAR(200),
    "created_at" TIMESTAMPTZ NOT NULL,
    "command_type_id" UUID NOT NULL REFERENCES "CommandTypes" ("id") ON DELETE CASCADE,
    "equipment_id" UUID NOT NULL REFERENCES "Equipments" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "Commands" IS 'Records commands sent to equipment.';
CREATE TABLE IF NOT EXISTS "EquipmentStatusLogs" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "details" VARCHAR(300),
    "reported_at" TIMESTAMPTZ NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL,
    "equipment_id" UUID NOT NULL REFERENCES "Equipments" ("id") ON DELETE CASCADE,
    "status_id" UUID NOT NULL REFERENCES "EquipmentStatuses" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "EquipmentStatusLogs" IS 'Stores the status change logs of the equipment.';
CREATE TABLE IF NOT EXISTS "ReservationStatuses" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "name" VARCHAR(60) NOT NULL UNIQUE,
    "created_at" TIMESTAMPTZ NOT NULL
);
COMMENT ON TABLE "ReservationStatuses" IS 'Stores the different statuses of a reservation.';
CREATE TABLE IF NOT EXISTS "Users" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "name" VARCHAR(60) NOT NULL,
    "email" VARCHAR(60) NOT NULL UNIQUE,
    "is_active" BOOL NOT NULL  DEFAULT True,
    "created_at" TIMESTAMPTZ NOT NULL
);
COMMENT ON TABLE "Users" IS 'Stores information about the system''s users.';
CREATE TABLE IF NOT EXISTS "Reservations" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "start_time" TIMESTAMPTZ NOT NULL,
    "end_time" TIMESTAMPTZ NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL,
    "equipment_id" UUID NOT NULL REFERENCES "Equipments" ("id") ON DELETE CASCADE,
    "status_id" UUID NOT NULL REFERENCES "ReservationStatuses" ("id") ON DELETE CASCADE,
    "user_id" UUID NOT NULL REFERENCES "Users" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "Reservations" IS 'Stores information about reservations made by users.';
CREATE TABLE IF NOT EXISTS "UserAuth" (
    "id" UUID NOT NULL  PRIMARY KEY,
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
