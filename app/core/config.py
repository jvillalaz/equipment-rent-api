import asyncio
from tortoise import Tortoise
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
import os
from gmqtt import Client as MQTTClient

# MQTT Broker host and port (default values for local Docker setup)
MQTT_BROKER_HOST = os.getenv("MQTT_BROKER_HOST", "rent-mosquitto")
MQTT_BROKER_PORT = int(os.getenv("MQTT_BROKER_PORT", 1883))

# MQTT client ID (must be unique per client connected to the broker)
MQTT_CLIENT_ID = os.getenv("MQTT_CLIENT_ID", "equipment-rent-api")
mqtt = MQTTClient(MQTT_CLIENT_ID)


# Connects to the MQTT broker with retry logic
async def connect_mqtt(retries=5, delay=2):
    for attempt in range(retries):
        try:
            await mqtt.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT)
            print(f"[MQTT] Connected to {MQTT_BROKER_HOST}:{MQTT_BROKER_PORT}")
            return
        except Exception as e:
            if attempt == retries - 1:
                raise
            print(f"[MQTT] Connection attempt {attempt + 1} failed: {e}")
            await asyncio.sleep(delay)


# Initializes the Postgres database with retry logic
async def init_db(app: FastAPI, retries=10, delay=3):
    db_url = "postgres://rentdb:rentdb@rent-postgres:5432/rent"
    for attempt in range(retries):
        try:
            await Tortoise.init(
                db_url=db_url,
                modules={"models": ["app.database"]},
            )
            await Tortoise.generate_schemas(safe=True)
            print("Database connected!")
            return
        except Exception as e:
            print(f"Database connection failed (attempt {attempt + 1}/{retries}): {e}")
            await asyncio.sleep(delay)
    raise Exception("Could not connect to the database after multiple retries")


# Secret key and algorithm used to sign JWT tokens
SECRET_KEY = "ffc2c1bf196a3a3ebbfcf731f4b03fe57239c2e81be50bd23a36e472ef3913b2"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing configuration using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 configuration for extracting the token from requests
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
