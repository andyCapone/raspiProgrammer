#-*-coding:utf-8-*-
from os import path as osPath
from io import createPath
from helper import toBool, userInput


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
        if path == "":
            self.setPath(osPath.dirname(osPath.realpath(__file__)))
        else:
            self.setPath(path)
        if not self.load():
            self.setStandard()

    def setStandard(self):
        self.log = False
        self.logSize = 1024**2

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
            else:
                self.log = False
            # set logSize
            if "logSize" in sDict.keys():
                self.logSize = int(sDict["logSize"])
            else:
                self.logSize = 1024**2

            return True

def setup():

    # create Settings-instance
    settings = Settings()
    # log events?
    while True:
        s = userInput("Soll geloggt werden? Y/n:", standard="y") #translate
        if s.lower() in ["n", "no"]:
            settings.log = False
            break
        elif s.lower() in ["y", "yes"]:
            settings.log = True
            # choose maximum log size in KiB
            while True:
                n = userInput("Bitte die maximale Größe der Log-Datei in KiB eingeben (1024):", True, standard=1024) #translate
                if n > 0:
                    break
                else:
                    print("Zahl zu klein.") #translate
                    continue
            settings.logSize = n*1024
            break
        else:
            print("Eingabe nicht korrekt.") #translate
            continue
    return settings

if __name__ == "__main__":
    s = setup()
    s.save()