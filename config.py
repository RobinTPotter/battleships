import os
import logging

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    LOGNAME = 'battleships'
    LOGLEVEL = logging.INFO
    PORT = 8085
    NOPASSWORD_CHECK = True
    TEST_MODE = True
    CHROME_DRIVER = '../Downloads/chromedriver.exe'