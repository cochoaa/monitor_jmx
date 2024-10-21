import logging
from logging.handlers import TimedRotatingFileHandler

FORMAT = "%(asctime)s.%(msecs)03d  [%(levelname)-8.8s] [%(module)-12.12s]  [%(funcName)-12.12s] [%(lineno)-3s]   %(message)s"
LEVEL= logging.DEBUG
FILENAME='logs/app.log'

def getLogger():
    logger = logging.getLogger('logger')
    logger.setLevel(LEVEL)
    logHandler = TimedRotatingFileHandler(filename=FILENAME, when="midnight")
    logFormatter = logging.Formatter(FORMAT)
    logHandler.setFormatter(logFormatter)

    if not logger.handlers:
        streamhandler = logging.StreamHandler()
        formatter = logging.Formatter(FORMAT)
        streamhandler.setFormatter(formatter)

        logger.addHandler(streamhandler)
        logger.addHandler(logHandler)

    return logger