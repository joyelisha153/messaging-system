from celery import Celery
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# RabbitMQ configuration
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "guest")
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = os.getenv("RABBITMQ_PORT", "5672")

BROKER_URL = f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_HOST}:{RABBITMQ_PORT}//"

celery_app = Celery(
    "messaging_system",
    broker=BROKER_URL,
    include=["tasks"]   # 🔥 IMPORTANT FIX
)

# 🔥 VERY important for autodiscovery
celery_app.autodiscover_tasks(['tasks'])

