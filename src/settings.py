import os

################################################################################
# App configuration
################################################################################

INSERTION_QUEUE = os.environ.get('INSERTION_QUEUE')
VALIDATION_QUEUE = os.environ.get('VALIDATION_QUEUE')
RESPONSE_EXCHANGE = os.environ.get('RESPONSE_EXCHANGE')
RESPONSE_ROUTING_KEY = os.environ.get('RESPONSE_ROUTING_KEY')

################################################################################
# Database configuration
################################################################################

MYSQL_ROOT_PASSWORD = os.environ.get('MYSQL_ROOT_PASSWORD')
MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE')
MYSQL_USER = os.environ.get('MYSQL_USER')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')
MYSQL_HOST = os.environ.get('MYSQL_HOST')

################################################################################
# Rabbitmq
################################################################################

AMQP_URL = os.environ.get('AMQP_URL')
