import json
def loadfile(opt,data,fname="data.json"):
    with open(fname, "w", encoding="utf-8") as f:
        if opt == 0 or opt == "load":
            data = json.load(f)
            return data
        if opt == 1 or opt == "dump":
            json.dump(data, f, indent=2)
            

   
    