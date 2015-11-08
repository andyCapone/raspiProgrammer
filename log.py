#-*-coding:utf-8-*-
from helper import Settings
from traceback import format_exc
from datetime import datetime
from io import getFileSize
from subprocess import call


class Log:
    LOG_FILE = "log.txt"

    class Body:
        MAX_LINE_LEN = 64
        TIME_FORMAT_de_DE = "%d.%m.%Y, %H:%M:%S"
        TIME_FORMAT_en_US = "%m/%d/%Y, %I:%M:%S %p"

        def __init__(self, datetimeObj, content):
            self.format = Log.Body.TIME_FORMAT_de_DE
            self.time = datetimeObj
            self.text = content
            self.indent = len(list(self.time.strftime(self.format))) + 2
            self.body = self.createBody()

        def createBody(self):
            wordList = self.text.split()
            content = self.time.strftime(self.format) + ": "
            position = self.indent

            for word in wordList:
                wordLength = len(list(word)) + 1
                if wordLength > Log.Body.MAX_LINE_LEN - self.indent:
                    if Log.Body.MAX_LINE_LEN - position <= 0:
                        content += "\n" + self.indent * " "
                        position = self.indent
                    tmpList = [word[:Log.Body.MAX_LINE_LEN - position - 1]]
                    word = word[Log.Body.MAX_LINE_LEN - position - 1:]
                    while len(list(word)) > Log.Body.MAX_LINE_LEN - self.indent:
                        tmpList.append(word[:Log.Body.MAX_LINE_LEN - self.indent - 1])
                        word = word[Log.Body.MAX_LINE_LEN - self.indent - 1:]
                    tmpList.append(word)
                    for tmpWord in tmpList[:-1]:
                        content += tmpWord + "\n" + self.indent * " "
                    content += tmpList[-1] + " "
                    position = self.indent + len(list(tmpList[-1])) + 1
                else:
                    if position + wordLength > Log.Body.MAX_LINE_LEN:
                        content += "\n" + self.indent * " "
                        position = self.indent
                    content += word + " "
                    position += wordLength

            content += "\n"
            return content

        def __str__(self):
            return self.body

    def __init__(self, content, forceOldLog = False):
        self.settings = Settings()
        if not self.settings.log:
            return

        if not forceOldLog:
            if self.getLogSize() > self.settings.logSize:
                if self.backup():
                    Log("Größengrenze der Logdatei erreicht, wurde zurückgesetzt.") #tranlate
                else:
                    Log("Größengrenze der Logdatei erreicht, konnte nicht zurückgesetzt werden.", True) #translate

        if "Error" in content.__class__.__name__:
            self.content = format_exc()
        else:
            try:
                self.content = str(content)
            except:
                self.content = format_exc()

        self.body = Log.Body(datetime.today(), self.content)
        self.log()

    def log(self):
        with open(self.settings.logDir + Log.LOG_FILE, "a") as file:
            file.write(str(self.body))

    def backup(self):
        if call(["tar", "-czf", self.settings.logDir + "log.bak.tar.gz",
                 "-C", self.settings.logDir, Log.LOG_FILE]) == 0:
            if call(["rm", self.settings.logDir + Log.LOG_FILE]) == 0:
                return True
            else:
                return False
        else:
            return False

    def getLogSize(self):
        return getFileSize(self.settings.logDir + Log.LOG_FILE)