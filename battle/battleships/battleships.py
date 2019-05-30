#!/usr/bin/python3
import logging
import sys
print (sys.version)


if __name__ == "__main__":
    from app import app
    from app.logconfig import ch
    logging.getLogger('werkzeug').addHandler(ch)
    app.logger.error('bollocks')
    app.debug = True
    app.run(host='0.0.0.0', port=8085, threaded=True, extra_files=[])
