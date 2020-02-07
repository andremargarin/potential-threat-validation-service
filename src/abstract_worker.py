import logging
import threading
import pika


class AbstractWorker(threading.Thread):

    QUEUE = None

    def __init__(self, amqp_url, name):
        super(AbstractWorker, self).__init__()
        self.name = name
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=amqp_url)
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.QUEUE)
        self.logger = self.get_logger()

    def get_logger(self):
        return logging.getLogger(f'{self.name}')

    def on_message(self, channel, method, properties, body):
        raise Exception('Not implemented')

    def run(self):
        self.channel.basic_consume(
            queue=self.QUEUE,
            on_message_callback=self.on_message,
            auto_ack=True
        )
        self.logger.info(f'Starting consumption of queue "{self.QUEUE}"')
        self.channel.start_consuming()
