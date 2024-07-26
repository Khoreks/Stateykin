import json

import pika
import uuid

from tools import settings

connection_params = pika.ConnectionParameters(
    host=settings.RABBITMQ_HOST,
    port=settings.RABBITMQ_PORT,
    virtual_host=settings.RABBITMQ_VIRTUAL_HOST,
    credentials=pika.PlainCredentials(
        username=settings.RABBITMQ_USERNAME,
        password=settings.RABBITMQ_PASSWORD
    ),
    heartbeat=30,
    blocked_connection_timeout=60 # Было 2
)


def worker_generation(user_message):
    response = None
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()
    channel.queue_declare(queue='agent')
    result_queue = channel.queue_declare(queue='', exclusive=True).method.queue
    correlation_id = str(uuid.uuid4())
    channel.basic_publish(
        exchange='',
        routing_key='agent',
        properties=pika.BasicProperties(reply_to=result_queue, correlation_id=correlation_id),
        body=user_message)

    def on_response(ch, method, properties, body):
        if properties.correlation_id == correlation_id:
            channel.basic_cancel(consumer_tag=consumer_tag)
            channel.queue_delete(queue=result_queue)
            connection.close()
            nonlocal response
            response = body

    consumer_tag = channel.basic_consume(queue=result_queue, on_message_callback=on_response, auto_ack=True)
    channel.start_consuming()

    response = json.loads(response.decode('utf-8'))
    return response
