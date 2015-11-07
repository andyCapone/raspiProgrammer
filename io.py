__author__ = 'andreas'


from subprocess import call

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
        raise ValueError("Pfad ist nicht absolut. Bitte absoluten Pfad angeben.") #translate

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
    dirList = [d for d in path.split("/") if d != ""]
    for i in range(1, len(dirList) + 1):
        try:
            tmp = "/"
            for j in range(i):
                tmp += dirList[j] + "/"
            if call(["ls", tmp]) == 2:
                # directory does not exist
                if call(["mkdir", tmp]) != 0:
                    return False
                # set owner and group, if given
                if owner != 0:
                    call(["chown", owner, tmp])
                if group != 0:
                    call(["chown", ":"+group, tmp])
        except:
            return False
    return True
