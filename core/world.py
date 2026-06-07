import os, json

def listWorlds():
    if not os.path.isdir("world"):
        os.mkdir("world")
        return []
    dir = os.listdir("world")
    worlds = []
    for i in dir:
        try:
            with open(os.path.join("world", i, "meta.json"), "r", encoding="utf-8") as f:
                world = json.load(f)
                world['dir'] = i
                worlds.append(world)
        except:
            continue
    return worlds

def createWorld(name):
    pass

def deleteWorld(name):
    pass

def loadWorld(name):
    pass