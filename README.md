# Potential Threat Validation Service

Microservice for validating potential threats, with the
purpose of discarding legitimate URLs using a regular expression whitelist.

The whitelist consists of expressions applicable to specific customers and global expressions, applicable to all customers. The microservice is made available through operations based on asynchronous messages.

Microservice developed in Python and integrated with the message broker RabbitMQ and with a MySQL database. The three components (microservice, RabbitMQ and MySQL) are executed in Docker containers.
