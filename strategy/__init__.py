from os import listdir
for filename in listdir("./strategy/"):
    try:
        if filename[-9:] == "Player.py":
            player = "from " + filename[:-3] + " import " + filename[:-3]
            exec player
    except ImportError:
        print "Could not execute \"from " + filename[:-3] + " import " + filename[:-3] + "\""
        print "The file name and the class must be the same."