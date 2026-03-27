import asyncio
import json
import logging

import aio_pika
from aio_pika.abc import (
    AbstractRobustChannel,
    AbstractRobustConnection,
    AbstractRobustQueue,
    AbstractExchange,
    AbstractIncomingMessage,
)
from aio_pika.exceptions import CONNECTION_EXCEPTIONS
from pydantic import ValidationError

from src.models.order import OrderCreateEvent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QueueConsumer:
    def __init__(
        self,
        rabbitmq_url: str,
        exchange_name: str,
        tasks_type: list[str],
        max_retry: int = 3,
    ):
        self.rabbitmq_url: str = rabbitmq_url
        self.exchange_name: str = exchange_name
        self.tasks_type: list[str] = tasks_type
        self.max_retry: int = max_retry

        self.connection: AbstractRobustConnection | None = None
        self.channel: AbstractRobustChannel | None = None
        self.main_exchange: AbstractExchange | None = None
        self.retry_exchange: AbstractExchange | None = None
        self.dead_letter_exchange: AbstractExchange | None = None

        self.main_queue: AbstractRobustQueue | None = None
        self.retry_queue: AbstractRobustQueue | None = None
        self.dead_letter_queue: AbstractRobustQueue | None = None

    async def connect(self) -> None:
        try:
            self.connection = await aio_pika.connect_robust(url=self.rabbitmq_url)
            self.channel = await self.connection.channel()
            await self.channel.set_qos(prefetch_count=1)

            self.main_exchange = await self.channel.declare_exchange(
                name=self.exchange_name, type=aio_pika.ExchangeType.DIRECT, durable=True
            )

            self.retry_exchange = await self.channel.declare_exchange(
                name="retry", type=aio_pika.ExchangeType.DIRECT, durable=True
            )

            self.dead_letter_exchange = await self.channel.declare_exchange(
                name="dlx", type=aio_pika.ExchangeType.DIRECT, durable=True
            )

            self.main_queue = await self.channel.declare_queue(
                name="main", durable=True
            )
            for task_type in self.tasks_type:
                await self.main_queue.bind(
                    exchange=self.main_exchange, routing_key=task_type
                )
            await self.main_queue.bind(
                exchange=self.main_exchange, routing_key="retry.return"
            )

            self.retry_queue = await self.channel.declare_queue(
                name="retry_queue",
                durable=True,
                arguments={
                    "x-message-ttl": 10 * 1000,
                    "x-dead-letter-exchange": self.exchange_name,
                    "x-dead-letter-routing-key": "retry.return",
                },
            )
            await self.retry_queue.bind(
                exchange=self.retry_exchange, routing_key="retry"
            )

            self.dead_letter_queue = await self.channel.declare_queue(
                name="dlq", durable=True
            )
            await self.dead_letter_queue.bind(
                exchange=self.dead_letter_exchange, routing_key="dlq"
            )
        except CONNECTION_EXCEPTIONS as e:
            logger.info(f"RabbitMQ Consumer connection error: {e}")
            raise

    async def _handle_send_email(self, event: OrderCreateEvent):
        logger.info(
            "Start send_email message: event_id=%s, user_id=%s",
            event.event_id,
            event.data.user_id,
        )
        await asyncio.sleep(2)

        logger.info(
            "DONE send_email message: event_id=%s, user_id=%s",
            event.event_id,
            event.data.user_id,
        )

    async def _handle_update_stock(self, event: OrderCreateEvent):
        logger.info(
            "Start update_stock message: event_id=%s, user_id=%s",
            event.event_id,
            event.data.user_id,
        )
        await asyncio.sleep(2)

        logger.info(
            "DONE update_stock message: event_id=%s, user_id=%s",
            event.event_id,
            event.data.user_id,
        )

    async def _handle_generate_report(self, event: OrderCreateEvent):
        logger.info(
            "Start generate_report message: event_id=%s, user_id=%s",
            event.event_id,
            event.data.user_id,
        )
        await asyncio.sleep(2)

        logger.info(
            "DONE generate_report message: event_id=%s, user_id=%s",
            event.event_id,
            event.data.user_id,
        )

    async def _get_retry_count(self, message: AbstractIncomingMessage) -> int:
        headers = message.headers or {}
        retry_count = headers.get("x-retry-count", 0)

        try:
            return int(retry_count)
        except (ValueError, TypeError):
            return 0

    async def process_message(self, message: AbstractIncomingMessage):
        retry_count = await self._get_retry_count(message)
        task_type = message.headers.get("task_type", "unknown")
        try:
            event = OrderCreateEvent.model_validate_json(message.body)

            if task_type == "send_email":
                await self._handle_send_email(event)
            elif task_type == "update_stock":
                await self._handle_update_stock(event)
            elif task_type == "generate_report":
                await self._handle_generate_report(event)
            else:
                logger.info("Unknown task_type=%s", task_type)
                await self._publish_to_dlq(message, reason="unknown_task_type")
            await message.ack()
        except (json.JSONDecodeError, ValidationError) as e:
            logger.info(f"NON-Retryable error. Publish in DLQ. Error: {e}")
            await self.dead_letter_exchange.publish(message=message, routing_key="dlq")
            await message.ack()
        except Exception as e:
            # Имитация временных ошибок (сеть/бд/падение нашего сервиса)
            logger.info(f"Retryable processing ERROR: {e}")

            if retry_count < self.max_retry:
                logger.info(
                    "Send to retry-dlx. Retry_count=%s, message_id=%s",
                    retry_count,
                    message.message_id,
                )

                new_message = aio_pika.Message(
                    body=message.body,
                    content_type="application/json",
                    delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                    correlation_id=message.correlation_id,
                    message_id=message.message_id,
                    headers={
                        **(message.headers or {}),
                        "x-original-routing-key": message.headers.get("task_type"),
                        "x-retry-count": retry_count + 1,
                    },
                )

                await self.retry_exchange.publish(
                    message=new_message, routing_key="retry"
                )
            else:
                logger.info(
                    "Exceeded retry_count=%s, send to DLQ.",
                    retry_count,
                )
                await self._publish_to_dlq(message, reason="exceeded_retry_count")
            await message.ack()

    async def _publish_to_dlq(self, message: AbstractIncomingMessage, reason: str):
        logger.info(
            "Added message in DLQ reason=%s",
            reason,
        )
        new_message = aio_pika.Message(
            body=message.body,
            content_type="application/json",
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            correlation_id=message.correlation_id,
            message_id=message.message_id,
            headers={
                **(message.headers or {}),
                "x-original-routing-key": message.headers.get("task_type"),
                "x-reason": reason,
            },
        )
        await self.dead_letter_exchange.publish(message=new_message, routing_key="dlq")

    async def consume(self) -> None:
        if self.connection is None:
            await self.connect()
        if self.channel is None:
            raise RuntimeError("RabbitMQ channel is not initialized")

        logger.info(f"Worker waiting for messages...")
        async with self.main_queue.iterator() as q_iter:
            async for message in q_iter:
                await self.process_message(message)
