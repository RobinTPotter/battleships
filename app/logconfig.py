import logging
from config import Config 

logger = logging.getLogger(Config.LOGNAME)
handler = logging.StreamHandler()
handler.setLevel(Config.LOGLEVEL)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(Config.LOGLEVEL)
logger.error('test just kidding!')
