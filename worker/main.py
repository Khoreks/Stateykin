import pika
import json
from pydantic import ValidationError, BaseModel
from dotenv import dotenv_values

from config import settings

from agent import Agent

tokens_config = eval(dotenv_values("tokens.env")[settings.MODEL_TYPE])


# class AgentInput(BaseModel):
#     first_token: str = tokens_config.get("first_token", None)
#     start_header: str = tokens_config.get("start_header", None)
#     end_header: str = tokens_config.get("end_header", None)
#     end_message: str = tokens_config.get("end_message", None)
#     user_message: str


connection_params = pika.ConnectionParameters(
    host=settings.RABBITMQ_HOST,
    port=settings.RABBITMQ_PORT,
    virtual_host=settings.RABBITMQ_VIRTUAL_HOST,
    credentials=pika.PlainCredentials(
        username=settings.RABBITMQ_USERNAME,
        password=settings.RABBITMQ_PASSWORD
    ),
    heartbeat=500,
    blocked_connection_timeout=500
)


def input_validation_handler(ch, method, properties, body):
    try:
        model_input = {
            "first_token": tokens_config.get("first_token", None),
            "start_header": tokens_config.get("start_header", None),
            "end_header": tokens_config.get("end_header", None),
            "end_message": tokens_config.get("end_message", None),
            "user_message": json.loads(body.decode('utf-8'))["user_message"]
        }
        generation_handler(ch, method, properties, model_input)
    except ValidationError as error:
        msg = f"Invalid data structure: {error}"
        ch.basic_publish(
            exchange='',
            routing_key=properties.reply_to,
            properties=pika.BasicProperties(correlation_id=properties.correlation_id),
            body=msg
        )


def generation_handler(ch, method, properties, model_input):
    results = Agent.invoke(model_input)
    response_handler(ch, method, properties, results)


def response_handler(ch, method, properties, results):
    data = json.dumps(results)
    ch.basic_publish(
        exchange='',
        routing_key=properties.reply_to,
        properties=pika.BasicProperties(correlation_id=properties.correlation_id),
        body=data
    )


def callback(ch, method, properties, body):
    input_validation_handler(ch, method, properties, body)


def worker():
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()
    channel.queue_declare(queue='agent')
    channel.basic_consume(queue='agent', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()


if __name__ == "__main__":
    worker()
