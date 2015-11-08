#-*-coding:utf-8-*-
from subprocess import call
from os import path as ospath, devnull

def createPath(path, **kwargs):

    # This function creates a non-existing directory at given path.
    # Owner and owner-group can be specified as keyword-arguments
    # using 'owner' and 'group'. Owner and owner-group will remain
    # untouched for existing directories.
    #
    # raises ValueError if given path is not absolute.
    #
    # returns True on success or False otherwise.

    if not path.startswith("/"):
        raise ValueError("Pfad ist nicht absolut. Bitte absoluten Pfad angeben.\n{0}".format(path)) #translate

    ## get kwargs
    # get owner of directory to be created
    if "owner" in kwargs.keys():
        owner = kwargs["owner"]
    else:
        owner = 0

    #get group of directory to be created
    if "group" in kwargs.keys():
        group = kwargs["group"]
    else:
        group = 0

    # list single directories
    dNull = open(devnull, "wb")
    dirList = [d for d in path.split("/") if d != ""]
    for i in range(1, len(dirList) + 1):
        try:
            tmp = "/"
            for j in range(i):
                tmp += dirList[j] + "/"
            if call(["ls", tmp], stderr=dNull, stdout=dNull) == 2:
                # directory does not exist
                if call(["mkdir", tmp], stdout=dNull, stderr=dNull) != 0:
                    dNull.close()
                    return False
                # set owner and group, if given
                if owner != 0:
                    call(["chown", owner, tmp], stderr=dNull, stdout=dNull)
                if group != 0:
                    call(["chown", ":"+group, tmp], stderr=dNull, stdout=dNull)
        except:
            dNull.close()
            return False
    dNull.close()
    return True

def getFileSize(path):

    # returns size of file or directory.
    # returns 0 if error occurs.

    try:
        return ospath.getsize(path)
    except:
        return 0