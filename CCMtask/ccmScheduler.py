# -*- coding: utf-8 -*-
import time
from threading import Thread,BoundedSemaphore
from queue import Queue

MaxBranchCount = 40
MaxScheduler = 4
CCMTaskQue = Queue(MaxBranchCount)

SchedulerRes = BoundedSemaphore(MaxScheduler)

class CCMTaskScheduler:
    def __init__(self, func, *args):
        self._thread = Thread(target=func, args=args)

    def start(self):
        self._thread.start()

    def join(self):
        self._thread.join()

def taskfunc(*args):
    ## 每成功处理一个参数，就从任务参数中剔除一个参数
    ## 遇到异常，保留剩余参数，入任务队列
    ccmtask = args[0]
    def proc():
        pass
    try:
        proc()
    except Exception:
        CCMTaskQue.put(ccmtask)
    finally:
        SchedulerRes.release()
    pass

def initCCMTaskQue():
    ## 生成所有初始任务队列
    pass

timeoutSignal = BoundedSemaphore(1)

def monitor():
    time.sleep(3600)
    timeoutSignal.acquire()

monitorThd = Thread(target=monitor)
monitorThd.start()
while not CCMTaskQue.empty():
    if timeoutSignal.acquire(timeout=60) == False:
        break
    ccmTask = CCMTaskQue.get()
    if SchedulerRes.acquire():
        task = CCMTaskScheduler(taskfunc, ccmTask)
        task.start()
        task.join()

