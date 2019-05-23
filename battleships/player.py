import logging
from config import LOGNAME
FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(LOGNAME)


class Player():
    def __init__(self,name):
        self.name = name
        logger.info('created {0}'.format(name))