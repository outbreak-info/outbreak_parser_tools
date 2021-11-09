def get_logger(name):
    try:
        from biothings import config
        logger = config.logger
    except ImportError:
        import logging
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler(f'{name}_log.log')
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
