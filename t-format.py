import datetime, time
format="%(levelname)s %(name)s %(asctime)s %(module)s [%(filename)s:%(lineno)d] [%(processName)s -> %(process)d] [%(threadName)s -> %(thread)d] %(message)s"
data = {'msecs': 35.78495979309082, 'args': (), 'name': 'simpleExample', 'thread': -1221907712, 'created': 1343705174.035785, 'process': 26768, 'threadName': 'MainThread', 'module': 't-logger-socket', 'filename': 't-logger-socket.py', 'levelno': 10, 'processName': 'MainProcess', 'pathname': 't-logger-socket.py', 'lineno': 14, 'exc_text': None, 'exc_info': None, 'funcName': '<module>', 'relativeCreated': 8.868932723999023, 'levelname': 'DEBUG', 'msg': 'debug message'}
def format_time(created, msecs):
    ct = datetime.datetime.fromtimestamp(created)
    t = ct.strftime("%Y-%m-%d %H:%M:%S")
    s = "%s,%03d" % (t, msecs)
    return s
data['asctime'] = format_time(data['created'], data['msecs'])
data['message'] = data['msg']
msg = format % data
print msg
