#-*-coding:utf-8-*-
from os import path
from io import createPath

class Settings:
    def __init__(self, path = ""):
        self.setPath(path)
        self.log = True
        self.logSize = 1024

    def setPath(self, path):
        if path.endswith("/"):
            self.path = path
        else:
            self.path = path + "/"
        self.logDir = path + "logs/"
        if not createPath(self.logDir):
            raise IOError("Log-Pfad konnte nicht erstellt werden.") #translate


    def save(self):
        if self.path != "":
            pass

def userInput(prompt, number = False):
    if not number:
        return raw_input(prompt + " ")
    while True:
        raw = raw_input(prompt + " ")
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



def setup():

    # create Settings-instance
    settings = Settings()

    # set main path as the path of the source-code
    settings.setPath(path.dirname(path.realpath(__file__)))

    # log events?
    while True:
        s = userInput("Soll geloggt werden? Y/n:") #translate
        if s.lower() in ["n", "no"]:
            settings.log = False
            break
        elif s.lower() in ["", "y", "yes"]:
            settings.log = True
            # choose maximum log size in KiB
            while True:
                n = userInput("Bitte die maximale Größe der Log-Datei in KiB eingeben (1024):", True) #translate
                if n > 0:
                    break
                else:
                    print("Zahl zu klein.") #translate
                    continue
            settings.logSize = n
            break
        else:
            print("Eingabe nicht korrekt.") #translate
            continue
    return settings

if __name__ == "__main__":
    settings = setup()
    print settings.path, settings.log, settings.logSize