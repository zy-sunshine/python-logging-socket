def initlog():
    import logging
    
    logging.config.fileConfig("logging.conf")
    #logfile = 'all.log'
    #logger = logging.getLogger()
    #hdlr = logging.FileHandler(logfile)
    #formatter = logging.Formatter('%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(levelname)s]- %(message)s')
    #formatter = logging.Formatter('%(levelname)-8s %(asctime)s %(module)s %(process)d %(thread)d %(message)s')
    #hdlr.setFormatter(formatter)
    #logger.addHandler(hdlr)
    #logger.setLevel(logging.NOTSET)
    
    return logger

if __name__ == '__main__':
    logger = initlog()
    logger.info('info message')
    logger.warning('warning message')
    logger.error('error message')

