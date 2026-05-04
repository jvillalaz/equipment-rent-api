CREATE TABLE "Users" (
  "id" uuid PRIMARY KEY,
  "name" varchar(60) NOT NULL,
  "email" varchar(60) UNIQUE NOT NULL,
  "is_active" boolean DEFAULT TRUE,
  "created_at" timestamp DEFAULT now()
);

CREATE TABLE "Equipments" (
  "id" uuid PRIMARY KEY,
  "name" varchar(60) UNIQUE NOT NULL,
  "current_status_id" uuid,
  "location" uuid,
  "last_heartbeat" timestamp,
  "created_at" timestamp DEFAULT now()
);

CREATE TABLE "EquipmentStatusLogs" (
  "id" uuid PRIMARY KEY,
  "status_id" uuid NOT NULL,
  "equipment_id" uuid NOT NULL,
  "details" varchar(300),
  "reported_at" timestamp DEFAULT now(),
  "created_at" timestamp DEFAULT now()
);

CREATE TABLE "EquipmentStatuses" (
  "id" uuid PRIMARY KEY,
  "name" varchar(60) UNIQUE NOT NULL,
  "created_at" timestamp DEFAULT now()
);

CREATE TABLE "ReservationStatuses" (
  "id" uuid PRIMARY KEY,
  "name" varchar(60) UNIQUE NOT NULL,
  "created_at" timestamp DEFAULT now()
);

CREATE TABLE "CommandTypes" (
  "id" uuid PRIMARY KEY,
  "name" varchar(60) UNIQUE NOT NULL,
  "created_at" timestamp DEFAULT now()
);

CREATE TABLE "Commands" (
  "id" uuid PRIMARY KEY,
  "command_type_id" uuid NOT NULL,
  "equipment_id" uuid NOT NULL,
  "payload" varchar(200),
  "created_at" timestamp DEFAULT now()
);

CREATE TABLE "Reservations" (
  "id" uuid PRIMARY KEY,
  "user_id" uuid NOT NULL,
  "equipment_id" uuid NOT NULL,
  "start_time" timestamp NOT NULL,
  "end_time" timestamp NOT NULL,
  "status_id" uuid NOT NULL,
  "created_at" timestamp DEFAULT now()
);

CREATE TABLE "UserAuth" (
  "id" uuid PRIMARY KEY,
  "username" varchar(60) UNIQUE NOT NULL,
  "password_hash" varchar(100) NOT NULL,
  "user_id" uuid NOT NULL,
  "created_at" timestamp DEFAULT now()
);

-- Foreign Key Definitions
ALTER TABLE "Equipments" ADD CONSTRAINT fk_equipments_status FOREIGN KEY ("current_status_id") REFERENCES "EquipmentStatuses" ("id");

ALTER TABLE "EquipmentStatusLogs" ADD CONSTRAINT fk_status_logs_status FOREIGN KEY ("status_id") REFERENCES "EquipmentStatuses" ("id");

ALTER TABLE "EquipmentStatusLogs" ADD CONSTRAINT fk_status_logs_equipment FOREIGN KEY ("equipment_id") REFERENCES "Equipments" ("id");

ALTER TABLE "Commands" ADD CONSTRAINT fk_commands_type FOREIGN KEY ("command_type_id") REFERENCES "CommandTypes" ("id");

ALTER TABLE "Commands" ADD CONSTRAINT fk_commands_equipment FOREIGN KEY ("equipment_id") REFERENCES "Equipments" ("id");

ALTER TABLE "Reservations" ADD CONSTRAINT fk_reservations_user FOREIGN KEY ("user_id") REFERENCES "Users" ("id");

ALTER TABLE "Reservations" ADD CONSTRAINT fk_reservations_equipment FOREIGN KEY ("equipment_id") REFERENCES "Equipments" ("id");

ALTER TABLE "Reservations" ADD CONSTRAINT fk_reservations_status FOREIGN KEY ("status_id") REFERENCES "ReservationStatuses" ("id");

ALTER TABLE "UserAuth" ADD CONSTRAINT fk_user_auth FOREIGN KEY ("user_id") REFERENCES "Users" ("id");
