try:
    from biothings import config
    logger = config.logger
except ImportError:
    import logging
    logger = logging.getLogger('dataverse')
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler('dataverse_log.log')
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

