#-*-coding:utf-8-*-
from os import path as osPath
from io import createPath


class Settings:

    # Class that contains program-settings.
    # If a path != "" is given, settings will
    # try to be loaded from that location.
    # Otherwise, settings will try to be loaded from
    # standard-path.
    #
    # Optionally takes a path as parameter.
    #
    # Raises IOError, if log-path cannot be
    # created.

    SETTINGS_FILE = "programmer.conf"

    def __init__(self, path = ""):
        self.log = False
        self.logSize = 1024**2
        if path == "":
            self.setPath(osPath.dirname(osPath.realpath(__file__)))
        else:
            self.setPath(path)
        self.load()

    def setPath(self, path):
        if path.endswith("/"):
            self.path = path
        else:
            self.path = path + "/"
        self.logDir = self.path + "logs/"
        if not createPath(self.logDir):
            raise IOError("Log-Pfad konnte nicht erstellt werden.") #translate
        self.settingsPath = self.path + Settings.SETTINGS_FILE

    def save(self):
        if self.path != "":
            f = open(self.settingsPath, "w")
            f.write("log={0}".format(self.log))
            f.write("\n")
            f.write("logSize={0}".format(self.logSize))
            f.close()

    def load(self):
        try:
            f = open(self.settingsPath, "r")
        except IOError:
            return False
        else:
            contents = f.read()
            f.close()
            lines = [l for l in contents.split("\n") if (l != "")
                     and (not l.startswith("#"))]
            sDict = {}
            for l in lines:
                sDict[l.split("=")[0].strip()] = l.split("=",1)[-1].strip()

            # set wether logging is enabled
            if "log" in sDict.keys():
                self.log = toBool(sDict["log"])
            # set logSize
            if "logSize" in sDict.keys():
                self.logSize = int(sDict["logSize"])

            return True


def userInput(prompt, number = False, **kwargs):
    if "standard" in kwargs.keys():
        standard = kwargs["standard"]
    else:
        standard = ""

    if not number:
        raw = raw_input(prompt + " ")
        if raw == "":
            return standard
        else:
            return raw

    while True:
        raw = raw_input(prompt + " ")
        if standard == "":
            standard = 0
        if raw == "":
            return standard
        try:
            n = int(raw)
        except ValueError:
            print("Die Eingabe muss eine Zahl sein.") #translate
            continue
        except:
            print("Unbekannter Fehler.") #tranlate
            continue
        else:
            break
    return n

def toBool(bStr):
    if type(bStr) == bool:
        return bStr
    if str(bStr) == "True":
        return True
    else:
        return False