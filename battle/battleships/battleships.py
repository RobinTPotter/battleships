import logging


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    from app import app
    app.debug = True
    logger.info('created app {0}'.format(app))
    app.run(host='0.0.0.0', port=8085, threaded=True, extra_files=[])
