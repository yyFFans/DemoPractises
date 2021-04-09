# -*- coding: utf-8 -*-
"""
待处理数据队列 长度N，M个在运行调度器处理
"""

from queue import Queue, Empty
from threading import Lock, Thread, BoundedSemaphore, current_thread, activeCount
import logging
import time


class AppLogger:
    def __init__(self, moduleName, logfile):
        self._logger = logging.getLogger(moduleName)
        handler = logging.FileHandler(logfile)
        fmt = "%(asctime)-15s %(levelname)s %(filename)s %(lineno)d %(message)s"
        formatter = logging.Formatter(fmt)
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)
        self._logger.setLevel(logging.INFO)

        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        console.setFormatter(formatter)
        self._logger.addHandler(console)

        self.warnning = self._logger.warning
        self.error = self._logger.error
        self.info = self._logger.info
        self.debug = self._logger.debug


dataQueueMaxLen = 100
schedulerMaxCount = 4


lock = Lock()

scheduleSources = BoundedSemaphore(schedulerMaxCount)

dataQueue = Queue(dataQueueMaxLen)

myLogger = AppLogger("myapp","test.log")

class Scheduler:
    def __init__(self, func, data):
        self._thread = Thread(target=func, args=data)
        self.record = "Scheduler(%s, %s)" % (func.__name__, *data)

    def __str__(self):
        return self.record

    def start(self):
        # myLogger.info(("START ", self.record))
        self._thread.start()

    def join(self):
        self._thread.join()

dataList = range(dataQueueMaxLen)

for data in dataList:
    dataQueue.put(data)

def testFunc(data):
    thd = current_thread()
    myLogger.info("Thread %s start testFunc %s sleep 5 seconds" % (thd , data))

    time.sleep(5)
    scheduleSources.release()
    myLogger.info("Thread %s exit testFunc %s" % (thd, data))

runningProcList = []

def startScheduler(func, data):
    if scheduleSources.acquire():
        proc = Scheduler(func, [data])
        proc.start()
        runningProcList.append(proc)


timeoutSignal = BoundedSemaphore(1)

def monitor():
    timeoutSignal.acquire()
    time.sleep(12)
    timeoutSignal.release()

if __name__ == "__main__":
    monitorThd = Thread(target=monitor)
    monitorThd.start()

    while not dataQueue.empty():
        if timeoutSignal.acquire(timeout=0):
            myLogger.warnning("timeout wait other thread end and Exit main process")
            break
        data = dataQueue.get()
        startScheduler(testFunc, data)
        myLogger.info("current running thread count %d " % activeCount())

    for proc in runningProcList:
        proc.join()

    myLogger.info("main proc exit")