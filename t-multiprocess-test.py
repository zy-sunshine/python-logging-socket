from multiprocessing import Process, Lock
import time

def f(l, i):
    #l.acquire()
    import logging.config

    logging.config.fileConfig("logging.conf")

    #create logger
    logger = logging.getLogger("simpleExample")


    logger.debug("debug message %s" % i)
    time.sleep(2)
    logger.info("info message %s" % i)
    time.sleep(2)
    logger.warn("warn message %s" % i)
    time.sleep(2)
    logger.error("error message %s" % i)
    time.sleep(2)
    logger.critical("critical message %s" % i)
    time.sleep(2)
    #print 'hello world', i
    #l.release()

if __name__ == '__main__':
    lock = Lock()

    for num in range(10):
        Process(target=f, args=(lock, num)).start()