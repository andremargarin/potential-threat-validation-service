# Potential Threat Validation Service
Microservice for validating potential threats, with the purpose of discarding legitimate URLs using a regular expression whitelist.

The whitelist consists of expressions applicable to specific customers and global expressions, applicable to all customers. The microservice is made available through operations based on asynchronous messages.

Microservice developed in Python and integrated with the message broker RabbitMQ and with a MySQL database. The three components (microservice, RabbitMQ and MySQL) are executed in Docker containers.

## Building and running
```
docker-compose up --build
```

## Operations
The interaction with the microservice is done through asynchronous messages.

The application provides two operations:

### 1. Insertion of regular expression in the whitelist
Upon receiving a request message from the queue __$INSERTION_QUEUE__, the application inserts a new record in its database. A request with the field "client" null (null) is interpreted as an insertion in the global whitelist, applicable to all clients.

Request message format:

```json
{
  "client": <string/nullable>,
  "regex": <string>
}
```

Response: None

### 2. URL validation

Upon receiving a request message from the queue __$VALIDATION_QUEUE__, the application uses the appropriate whitelist to determine whether the URL is in the whitelist or not.

Request message format:

```json
{
  "client": <string>,
  "url": <string>,
  "correlationId": <integer>
}
```

The "client" field is used to select the applicable regular expressions. A whitelist regular expression is applicable to a request if it was entered for the same customer as the request or if it was entered in the global whitelist.

Response: the response is sent to the __$RESPONSE_EXCHANGE__ exchange with routing key __$RESPONSE_ROUTING_KEY__.

Response message format:
```json
{
  "match": <boolean>,
  "regex": <string/nullable>,
  "correlationId": <integer>
}
```

The "match" field of the response has a value of true if at least one regular expression from the whitelist is compatible with the URL provided in the request, in which case the "regex" field must contain that regular expression; if no whitelist regular expression is compatible with the URL, the "match" field must have the value false, and the "regex" field must be null (null); in case of multiple compatible regular expressions, the "regex" field contains any one of them.

The "correlationId" field of the response has the same value contained in the request, being relevant only for the microservice user to be able to correlate a request message with a response message.
