#-*-coding:utf-8-*-
from setup import Settings

class Log:
    LOG_FILE = "log.txt"
    def __init__(self):
        settings = Settings()
        print settings.logDir, settings.logSize, settings.log

Log()