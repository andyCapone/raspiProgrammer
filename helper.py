#-*-coding:utf-8-*-


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