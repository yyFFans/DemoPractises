# -*- coding: utf-8 -*-
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

    def info(self,msg):
        self._logger.info(msg)

    def error(self, msg):
        self._logger.error(msg)

    def warning(self, msg):
        self._logger.warning(msg)

    def debug(self, msg):
        self._logger.debug(msg)


if __name__ == "__main__":
    moduleA_logfile = "moduleA-" + time.strftime("%Y%m%d%H%M%S") + '.log'
    moduleB_logfile = "moduleB-" + time.strftime("%Y%m%d%H%M%S") + '.log'

    moduleALogger = AppLogger("moduleA", moduleA_logfile)
    moduleBLogger = AppLogger("moduleB", moduleB_logfile)
    moduleALogger.info(" start xxxx")
    moduleBLogger.error("test error")