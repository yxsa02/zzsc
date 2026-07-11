class game:
    
    def __init__(self,do="create",data={}):
        # 初始化
        # do: "create" or "load"
        # data: dict with keys "name", "description", "itemReps", "rules"
        if do == "create":
            self.name = ""
            self.description = ""
            self.itemReps = []
            self.rules = []
        elif do == "load":
            try:
                self.name = data['name']
                self.description = data['description']
                self.itemReps = data['itemReps']
                self.rules = data['rules']
            except KeyError as e:
                print(f"[E]Error loading data: missing key {e}")

    def save(self):
        return {
            'name': self.name,
            'description': self.description,
            'itemReps': self.itemReps,
            'rules': self.rules
        }

