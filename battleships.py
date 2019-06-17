#!/usr/bin/python3
"""
battleships server
"""
import logging
import sys
print(sys.version)


if __name__ == "__main__":
    from app import app
    from app.logconfig import handler
    logging.getLogger('werkzeug').addHandler(handler)
    app.logger.error('bollocks')
    app.debug = True
    app.run(host='0.0.0.0', port=8085, threaded=True, extra_files=['templates'])
