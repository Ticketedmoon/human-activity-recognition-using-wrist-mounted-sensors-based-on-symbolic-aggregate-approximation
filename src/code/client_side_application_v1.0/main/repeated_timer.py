from threading import Timer

try:
    from PyQt5 import QtGui, QtCore
except:
    pass

class Repeated_Timer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            #self._timer = QtCore.QTimer(self.interval, self._run)
            self._timer = QtCore.QTimer()
            self._timer.timeout.connect(self._run)
            self._timer.start(self.interval * 1000)
            #self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.stop()
        self.is_running = False