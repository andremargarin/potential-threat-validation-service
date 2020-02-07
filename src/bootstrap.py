#!/bin/python

if __name__ == "__main__":
    import os
    from validation_worker import ValidationWorker
    from insertion_worker import InsertionWorker
    from settings import AMQP_URL

    INSERTION_WORKERS = int(os.environ.get('INSERTION_WORKER_THREADS', 1))
    VALIDATION_WORKERS = int(os.environ.get('VALIDATION_WORKER_THREADS', 1))

    threads_insertion = [
        InsertionWorker(AMQP_URL, f'insertion_worker_{i+1}')
        for i in range(0, INSERTION_WORKERS + 1)
    ]

    threads_validation = [
        ValidationWorker(AMQP_URL, f'validation_worker_{i+1}')
        for i in range(0, VALIDATION_WORKERS + 1)
    ]

    for thread in threads_insertion + threads_validation:
        thread.start()
