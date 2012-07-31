#import sys
#import time
#import logging

#if sys.argv[1] == 'client':
#    import logging.config
#
#    logging.config.fileConfig("logging.conf")
#
#    #create logger
#    logger = logging.getLogger("simpleExample")
#
#    #while 1:
#    for x in range(10):
#        logger.debug("debug message")
#        logger.info("info message")
#        logger.warn("warn message")
#        logger.error("error message")
#        logger.critical("critical message")
#        time.sleep(0.5)
#
#elif sys.argv[1] == 'server':
if 1:
    import pickle
    import logging
    import logging.handlers
    import SocketServer
    import struct
    
    
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
            while True:
                chunk = self.connection.recv(4)
                if len(chunk) < 4:
                    break
                slen = struct.unpack('>L', chunk)[0]
                chunk = self.connection.recv(slen)
                while len(chunk) < slen:
                    chunk = chunk + self.connection.recv(slen - len(chunk))
                obj = self.unPickle(chunk)
                record = logging.makeLogRecord(obj)
                self.handleLogRecord(record)
    
        def unPickle(self, data):
            return pickle.loads(data)
    
        def handleLogRecord(self, record):
            # if a name is specified, we use the named logger rather than the one
            # implied by the record.
            if self.server.logname is not None:
                name = self.server.logname
            else:
                name = record.name
            logger = logging.getLogger(name)
            # N.B. EVERY record gets logged. This is because Logger.handle
            # is normally called AFTER logger-level filtering. If you want
            # to do filtering, do it at the client end to save wasting
            # cycles and network bandwidth!
            logger.handle(record)
    
    class LogRecordSocketReceiver(SocketServer.ThreadingTCPServer):
        """
        Simple TCP socket-based logging receiver suitable for testing.
        """
    
        allow_reuse_address = 1
    
        def __init__(self, host='localhost',
                     port=logging.handlers.DEFAULT_TCP_LOGGING_PORT,
                     handler=LogRecordStreamHandler):
            SocketServer.ThreadingTCPServer.__init__(self, (host, port), handler)
            self.abort = 0
            self.timeout = 1
            self.logname = None
    
        def serve_until_stopped(self):
            import select
            abort = 0
            while not abort:
                rd, wr, ex = select.select([self.socket.fileno()],
                                           [], [],
                                           self.timeout)
                if rd:
                    self.handle_request()
                abort = self.abort
    
    def main():
        logging.basicConfig(
            format='%(name)-15s %(filename)25s:%(lineno)-5d %(levelname)-8s %(message)s')
        tcpserver = LogRecordSocketReceiver()
        print('About to start TCP server...')
        tcpserver.serve_until_stopped()
    
    main()
    
