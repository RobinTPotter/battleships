#!/usr/bin/python3
"""
battleships server
"""
import logging
import sys
print(sys.version)
from config import Config

class ContextFilter(logging.Filter):
    def filter(self, record):
        if 'GET /socket.io/?EIO' in str(record) or 'POST /socket.io/?EIO' in str(record): return False
        else: return True

if Config.TEST_MODE:
    from testing import Test 
    gogog = Test()
    gogog.start()
    

if __name__ == "__main__":
    from app import app
    from app.logconfig import handler
    logmehere = logging.getLogger('werkzeug')
    logmehere.addFilter(ContextFilter())
    logmehere.addHandler(handler)
    
    logging.getLogger('socketio').setLevel(logging.ERROR)
    logging.getLogger('engineio').setLevel(logging.ERROR)
    app.logger.error('bollocks')
    app.debug = True
    app.run(host='0.0.0.0', port=Config.PORT, threaded=True, extra_files=['templates'], use_reloader=False)
