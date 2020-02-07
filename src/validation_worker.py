import json
import re
from abstract_worker import AbstractWorker
from settings import VALIDATION_QUEUE, RESPONSE_EXCHANGE, RESPONSE_ROUTING_KEY
from utils import get_mysql_connection


class ValidationWorker(AbstractWorker):

    QUEUE = VALIDATION_QUEUE

    def __init__(self, amqp_url, name):
        super(ValidationWorker, self).__init__(amqp_url, name)
        self.channel.exchange_declare(exchange=RESPONSE_EXCHANGE)
        self.channel.queue_declare(queue=RESPONSE_ROUTING_KEY)
        self.channel.queue_bind(
            exchange=RESPONSE_EXCHANGE,
            queue=RESPONSE_ROUTING_KEY
        )

    def on_message(self, channel, method, properties, body):
        self.logger.debug(f'{self.name} receive message: {body}')

        body = json.loads(body)
        url = body.get('url')
        client = body.get('client')
        correlation_id = body.get('correlationId')

        cnx = get_mysql_connection()
        cursor = cnx.cursor(buffered=True)
        query = ("SELECT client, regex FROM whitelist WHERE client IS NULL OR client = %s")
        cursor.execute(query, (client,))

        response = {
            'correlationId': correlation_id,
            'regex': None,
            'match': False
        }

        match = False
        for (client, regex) in cursor:
            match = re.match(regex, url)
            if match:
                response['regex'] = regex
                response['match'] = True
                break

        cursor.close()
        cnx.close()

        self.logger.debug(response)
        self.channel.basic_publish(
            exchange=RESPONSE_EXCHANGE,
            routing_key=RESPONSE_ROUTING_KEY,
            body=json.dumps(response)
        )
