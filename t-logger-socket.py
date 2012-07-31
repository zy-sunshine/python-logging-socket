import sys
import time
import logging

if sys.argv[1] == 'client':
    import logging.config

    logging.config.fileConfig("logging.conf")

    #create logger
    logger = logging.getLogger("simpleExample")

    #while 1:
    for x in range(10):
        logger.debug("debug message")
        logger.info("info message")
        logger.warn("warn message")
        logger.error("error message")
        logger.critical("critical message")
        time.sleep(0.5)

elif sys.argv[1] == 'server':
    import cPickle
    import logging.handlers
    import SocketServer
    import struct
    import signal
    import datetime
    def initlog():
        import logging.config, logging
        
        logger = logging.getLogger('all')

        logfile = 'all.log'
        hdlr = logging.FileHandler(logfile)
        formatter = logging.Formatter('%(message)s')
        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr)

        logger.setLevel(logging.NOTSET)
        
        return logger

    def initlog_brief():
        import logging.config, logging
        
        logger = logging.getLogger('brief')
        formatter = logging.Formatter('%(message)s')
        logfile = 'brief.log'
        hdlr_brief = logging.FileHandler(logfile)
        hdlr_brief.setFormatter(formatter)
        logger.addHandler(hdlr_brief)

        logger.setLevel(logging.NOTSET)
        
        return logger
    
    Log = initlog()
    Log_brief = initlog_brief()
    format="%(levelname)s %(name)s %(asctime)s %(module)s [%(filename)s:%(lineno)d] [%(processName)s -> %(process)d] [%(threadName)s -> %(thread)d] %(message)s"
    format_brief = "%(levelname)s %(asctime)s [%(filename)s:%(lineno)d] %(message)s"
    class LogRecordStreamHandler(SocketServer.StreamRequestHandler):
        """Handler for a streaming logging request.

        This basically logs the record using whatever logging policy is
        configured locally.
        """

        def handle(self):
            """
            Handle multiple requests - each expected to be a 4-byte length,
            followed by the LogRecord in pickle format. Logs the record
            according to whatever policy is configured locally.
            """
            while 1:
                chunk = self.connection.recv(4)
                if len(chunk) < 4:
                    break

                slen = struct.unpack(">L", chunk)[0]
                chunk = self.connection.recv(slen)
                while len(chunk) < slen:
                    chunk = chunk + self.connection.recv(slen - len(chunk))

                obj = self.unPickle(chunk)
                
                self.handleLogRecord(obj)

        def unPickle(self, data):
            return cPickle.loads(data)

        def formatTime(self, created, msecs):
            ct = datetime.datetime.fromtimestamp(created)
            t = ct.strftime("%Y-%m-%d %H:%M:%S")
            s = "%s,%03d" % (t, msecs)
            return s

        def handleLogRecord(self, obj):
            # record = logging.makeLogRecord(obj)
            # t = time.strftime('%a, %d %b %y %H:%M:%S',
            # time.localtime(record.created))
            obj['asctime'] = self.formatTime(obj['created'], obj['msecs'])
            obj['message'] = obj['msg']
            Log.info(format % obj)
            Log_brief.info(format_brief % obj)

    class LogRecordSocketReceiver(SocketServer.ThreadingTCPServer):
        """simple TCP socket-based logging receiver suitable for testing.
        """

        allow_reuse_address = 1

        def __init__(self, host='localhost', port=logging.handlers.DEFAULT_TCP_LOGGING_PORT, handler=LogRecordStreamHandler):

            SocketServer.ThreadingTCPServer.__init__(self, (host, port), handler)
            self.abort = 0
            self.timeout = 1
            self.logname = None

        def serve_until_stopped(self):
            import select
            abort = 0
            while not abort:
                rd, wr, ex = select.select([self.socket.fileno()], [], [], self.timeout)
                if rd:
                    self.handle_request()

                abort = self.abort

            print "serve_until_stopped exiting"

    #
    # Start ThreadingTCPServer instance to accept SocketHandler log
    # messages from client.
    #
    tcpserver = LogRecordSocketReceiver()
    print "Starting ThreadingTCPServer..."
    tcpserver.serve_until_stopped()
