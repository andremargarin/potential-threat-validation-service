if __name__ == "__main__":
    import logging
    from validation_worker import ValidationWorker
    from insertion_worker import InsertionWorker
    from settings import (
        AMQP_URL, DEBUG, INSERTION_WORKER_THREADS, VALIDATION_WORKER_THREADS
    )

    level = logging.DEBUG if DEBUG else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s %(name)s : %(message)s'
    )

    threads_insertion = [
        InsertionWorker(AMQP_URL, f'insertion_worker_{i+1}')
        for i in range(0, INSERTION_WORKER_THREADS + 1)
    ]

    threads_validation = [
        ValidationWorker(AMQP_URL, f'validation_worker_{i+1}')
        for i in range(0, VALIDATION_WORKER_THREADS + 1)
    ]

    for thread in threads_insertion + threads_validation:
        thread.start()
