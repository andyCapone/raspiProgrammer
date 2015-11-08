#-*-coding:utf-8-*-
from helper import userInput, Settings
from subprocess import Popen, PIPE, call
from log import Log
from sys import exit
from os import chdir, getcwd


class InstalledPackages:

    # This class provides a list of installed packages and
    # makes them searchable.
    #
    # Raises OSError if 'dpkg -l' outputs any error.

    def __init__(self):
        output = Popen(["dpkg", "-l"], stderr=PIPE, stdout=PIPE).communicate()
        if output[1] != "":
            raise OSError("dpkg konnte nicht ausgeführt werden.") #translate
        lines = [l for l in output[0].split("\n") if l != ""]
        i = 0
        for l in lines:
            if not l.startswith("+++"):
                i += 1
            else:
                break
        splitLines = [l.split() for l in lines[i+1:]]
        self.packages = [l[1] for l in splitLines]

    def search(self, name):
        if name in self.packages:
            return True
        return False

def setup():

    print("Bitte sicherstellen, dass eine Internetverbindung verfügbar ist.") #translate
    print("Setup kann sonst womöglich nicht durchgeführt werden.") #translate

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
    # to enable logging, settings will be saved now
    settings.save()
    Log("Logging aktiviert, maximale Größe: {0} KiB".format(settings.logSize)) #translate

    # perform update?
    while True:
        s = userInput("Ein Update sollte durchgeführt werden. Jetzt updaten? Y/n:", standard="y") #translate
        if s.lower() in ["n", "no"]:
            Log("Update soll nicht durchgeführt werden.") #translate
            break
        elif s.lower() in ["y", "yes"]:
            Log("Update wird durchgeführt.") #translate
            err = call(["sudo", "apt-get", "update"])
            if err == 0:
                Log("Update der Paketquellen erfolgreich beendet.") #translate
            else:
                Log("Fehler beim Update; Exit-Code: {0}".format(err)) #translate
            break
        else:
            print("Eingabe nicht korrekt.") #translate
            continue

    # get installed packages and check for needed new installs
    neededPackages = ["gcc", "make", "bison", "autoconf", "flex", "gcc-avr",
                      "binutils-avr", "avr-libc"]
    installedPackages = InstalledPackages()
    newPackages = []
    for p in neededPackages:
        if not installedPackages.search(p):
            newPackages.append(p)
    print("Folgende Pakete müssen installiert werden:") #translate
    for p in newPackages:
        print "- " + p

    while True:
        s = userInput("Jetzt installieren? Y/n:") #translate
        if s.lower() in ["n", "no"]:
            print("Installation abgebrochen, Setup wird beendet.") #translate
            Log("Installation abgebrochen, Setup wird beendet. 1") #translate
            exit(1)
        elif s.lower() in ["y", "yes"]:
            for p in newPackages:
                err = call(["sudo", "apt-get", "-y", "install", p])
                if err == 0:
                    print(p + " erfolgreich installiert.") #translate
                    Log(p + " erfolgreich installiert.") #translate
                else:
                    print(p + " konnte nicht installiert werden. Setup wird beendet.") #translate
                    Log(p + " konnte nicht installiert werden. Exit-Code: {0}."
                            " Setup wird beendet. 2") #translate
                    exit(2)
            break
        else:
            print("Eingabe nicht korrekt.") #translate
            continue

    # install avrdude
    while True:
        s = userInput("avrdude von kcuzner muss von github geholt und installiert werden."
                      " Jetzt installieren? Y/n:", standard="y") #translate
        if s.lower() in ["n", "no"]:
            print("Installation abgebrochen, Setup wird beendet.") #translate
            Log("Installation abgebrochen, Setup wird beendet. 3") #translate
            exit(3)
        elif s.lower() in ["y", "yes"]:
            cwd = getcwd()
            chdir("~/")
            err = call(["git", "clone", "https://github.com/kcuzner/avrdude"])
            if err == 0:
                print("Download erfolgreich.") #translate
                Log("Download erfolgreich.") #translate
            else:
                print("Download nicht erfolgreich. Setup wird abgebrochen.") #translate
                Log("Download nicht erfolgreich. Exit-Code: {0}. "
                    "Setup wird abgebrochen. 4".format(err)) #translate
                exit(4)
            chdir("~/avrdude/avrdude/")
            err = call("./bootstrap", shell=True)
            if err == 0:
                print("bootstrap erfolgreich.") #translate
                Log("bootstrap erfolgreich.") #translate
            else:
                print("bootstrap nicht erfolgreich. Setup wird abgebrochen.") #translate
                Log("bootstrap nicht erfolgreich. Exit-Code: {0}. "
                    "Setup wird abgebrochen. 5".format(err)) #translate
                exit(5)
            err = call("./configure", shell=True)
            if err == 0:
                print("configure erfolgreich.") #translate
                Log("configure erfolgreich.") #translate
            else:
                print("configure nicht erfolgreich. Setup wird abgebrochen.") #translate
                Log("configure nicht erfolgreich. Exit-Code: {0}. "
                    "Setup wird abgebrochen. 6".format(err)) #translate
                exit(6)
            err = call(["sudo", "make"])
            if err == 0:
                print("make erfolgreich.") #translate
                Log("make erfolgreich.") #translate
            else:
                print("make nicht erfolgreich. Setup wird abgebrochen.") #translate
                Log("make nicht erfolgreich. Exit-Code: {0}. "
                    "Setup wird abgebrochen. 7".format(err)) #translate
                exit(7)
            err = call(["sudo", "make", "install"])
            if err == 0:
                print("make install erfolgreich.") #translate
                Log("make install erfolgreich.") #translate
            else:
                print("make install nicht erfolgreich. Setup wird abgebrochen.") #translate
                Log("make install nicht erfolgreich. Exit-Code: {0}. "
                    "Setup wird abgebrochen. 8".format(err)) #translate
                exit(8)
            break
        else:
            print("Eingabe nicht korrekt.") #translate
            continue

if __name__ == "__main__":
    setup()