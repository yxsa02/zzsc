class itemRep:
    # 物品存储容器
    def __init__(self,do="create",data={}):
        # 初始化物品容器
        if do == "create":
            self._item = []
            self._heavAll = 0
            self._spaceAll = 0
            self._heavUsed = 0
            self._spaceUsed = 0
        elif do == "load":
            try:
                self._item = data['item']
                self._heavAll = data['heavAll']
                self._spaceAll = data['spaceAll']
                self._heavUsed = data['heavUsed']
                self._spaceUsed = data['spaceUsed']
            except KeyError as e:
                print(f"[E]Error loading data: missing key {e}")

    def space(self,key):
        # 物品容器空间查询
        if key == 'all':
            return self._spaceAll
        elif key == 'used':
            return self._spaceUsed
        elif key == 'remain':
            return self._spaceAll - self._spaceUsed
        else:
            return 0
        
    def heav(self,key):
        # 物品容器重量查询
        if key == 'all':
            return self._heavAll
        elif key == 'used':
            return self._heavUsed
        elif key == 'remain':
            return self._heavAll - self._heavUsed
        else:
            return 0
        
    def save(self):
        # 物品容器数据保存
        return {
            'item': self._item,
            'heavAll': self._heavAll,
            'spaceAll': self._spaceAll,
            'heavUsed': self._heavUsed,
            'spaceUsed': self._spaceUsed
        }
    
    def inItem(self,item):
        # 物品存入容器
        self._item.append(item)
        self._heavUsed += item.heav
        self._spaceUsed += item.space

    def outItem(self,item):
        # 物品取出容器
        if item in self._item:
            self._item.remove(item)
            self._heavUsed -= item.heav
            self._spaceUsed -= item.space

    def listItem(self):
        # 列出容器内所有物品
        return self._item
    
    def selectItem(self,type,key):
        # 通过物品信息（标签）查询物品
        for item in self._item:
            if type == 'name' and item.name == key:
                return item
            elif type == 'id' and item.id == key:
                return item
        return None