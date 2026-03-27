import aio_pika
from aio_pika.abc import (
    AbstractRobustConnection,
    AbstractRobustChannel,
    AbstractExchange,
)
from aio_pika.exceptions import AMQPConnectionError, DeliveryError

from src.models.order import OrderCreateEvent


class QueueProducer:
    def __init__(self, rabbitmq_url, exchange_name: str):
        self.connection: AbstractRobustConnection | None = None
        self.channel: AbstractRobustChannel | None = None
        self.exchange: AbstractExchange | None = None

        self.rabbitmq_url: str = rabbitmq_url
        self.exchange_name: str = exchange_name

    async def connect(self):
        try:
            self.connection = await aio_pika.connect_robust(url=self.rabbitmq_url)
            self.channel = await self.connection.channel()
            await self.channel.set_qos(prefetch_count=10)

            self.exchange = await self.channel.declare_exchange(
                name=self.exchange_name, type=aio_pika.ExchangeType.DIRECT, durable=True
            )
        except AMQPConnectionError as e:
            print(f"RabbitMQ connection error: {e}")

    async def send_order_task(self, task_type: str, order_data: dict) -> None:
        if self.connection is None:
            await self.connect()

        try:
            event = OrderCreateEvent.model_validate(order_data)
            data = event.model_dump_json().encode("utf-8")

            message = aio_pika.Message(
                body=data,
                content_type="application/json",
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                message_id=event.event_id,
                headers={"task_type": task_type},
            )
            await self.exchange.publish(message=message, routing_key=task_type)
        except DeliveryError as e:
            print(f"The message was not delivered. Failed to publish: {e}")
            raise
        except Exception as e:
            print(f"Error when posting a message: {e}")

    async def close(self):
        if self.channel is not None and not self.channel.is_closed:
            await self.channel.close()

        if self.connection is not None and not self.connection.is_closed:
            await self.connection.close()
