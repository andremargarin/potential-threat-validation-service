import json
import re
from abstract_worker import AbstractWorker
from settings import VALIDATION_QUEUE, AMQP_URL
from utils import get_mysql_connection


class ValidationWorker(AbstractWorker):

    QUEUE = VALIDATION_QUEUE

    def on_message(self, ch, method, properties, body):
        self.logger.info(f'Validation: {self.name} receive message')

        body = json.loads(body)
        url = body.get('url')
        client = body.get('client')
        correlation_id = body.get('correlationId')

        cnx = mysql.connector.connect(user='root', password='root', host='mysql', database='axur')
        cursor = cnx.cursor()
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
        return response
