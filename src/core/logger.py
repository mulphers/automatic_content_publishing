import logging


def _disable_another_logger() -> None:
    for logger in logging.Logger.manager.loggerDict:
        logging.getLogger(logger).disabled = True


def init_logger() -> None:
    _disable_another_logger()

    logging.basicConfig(
        filename='py_log.log',
        format='[%(asctime)s] %(levelname)s [%(threadName)s %(pathname)s %(funcName)s:%(lineno)d] %(message)s',
        datefmt='%Y.%m.%d %H:%M:%S',
        level=logging.DEBUG
    )

    logging.info('Application is running')
