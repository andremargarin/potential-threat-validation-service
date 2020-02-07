import json
from abstract_worker import AbstractWorker
from settings import INSERTION_QUEUE
from utils import get_mysql_connection


class InsertionWorker(AbstractWorker):

    QUEUE = INSERTION_QUEUE

    def on_message(self, channel, method, properties, body):
        self.logger.debug(f'{self.name} receive message: {body}')

        body = json.loads(body)
        client = body.get('client')
        regex = body.get('regex')

        cnx = get_mysql_connection()
        cursor = cnx.cursor()
        add_whitelist_entry = ("INSERT INTO whitelist (client, regex) VALUES (%s, %s)")
        data_entry = (client, regex)
        cursor.execute(add_whitelist_entry, data_entry)
        cnx.commit()
        cursor.close()
        cnx.close()
