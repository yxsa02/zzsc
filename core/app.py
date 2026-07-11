from . import dp

class Activity:
    def __init__(self, name):
        self.name = name
        self.path = ["start"]
        self.p = {}
        self.status = {}
        self.action = Action(self)
        self.dp = dp.displayer()
        self.cAction()
        self.loop()
    def loop(self):
        while self.path[-1] != "exit":
            action = 
    def cAction(self,actionId):
        a = self.action.actions[actionId]
        

class Action:
    
    def __init__(self,activity):
        #self.a = Activity()
        self.a = activity
        self.actions = {
        "start":{"init":self.start,"loop":self.start},"reader":{}
    }
    def start(self):
        self.a.dp.makeScreen()
