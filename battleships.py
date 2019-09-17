#!/usr/bin/python3
"""
battleships server
"""
import logging
import sys
print(sys.version)

class ContextFilter(logging.Filter):
    def filter(self, record):
        if 'GET /socket.io/?EIO' in str(record) or 'POST /socket.io/?EIO' in str(record): return False
        else: return True

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
    app.run(host='0.0.0.0', port=8085, threaded=True, extra_files=['templates'])
