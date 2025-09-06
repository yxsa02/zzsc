# lib/item_system.py
import json
import os

class ItemSystem:
    def __init__(self):
        self.items = {}
        self.recipes = {}
        self.load_items()
    
    def load_items(self):
        try:
            with open("res/items.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                self.items = data.get("items", {})
                self.recipes = data.get("crafting_recipes", {})
        except FileNotFoundError:
            print("物品数据文件未找到!")
            self.items = {}
            self.recipes = {}
    
    def get_item(self, category, item_id):
        """获取特定物品的详细信息"""
        if category in self.items and item_id in self.items[category]:
            return self.items[category][item_id]
        return None
    
    def get_recipe(self, recipe_id):
        """获取特定配方的详细信息"""
        if recipe_id in self.recipes:
            return self.recipes[recipe_id]
        return None
    
    def get_all_items_in_category(self, category):
        """获取特定类别的所有物品"""
        if category in self.items:
            return self.items[category]
        return {}
    
    def get_all_categories(self):
        """获取所有物品类别"""
        return list(self.items.keys())
    
    def get_all_recipes(self):
        """获取所有制作配方"""
        return self.recipes
    
    def can_craft(self, recipe_id, inventory):
        """检查是否满足制作条件"""
        recipe = self.get_recipe(recipe_id)
        if not recipe:
            return False
        
        for item_id, amount in recipe["requirements"].items():
            # 在库存中查找物品
            found = False
            for category in self.items:
                if item_id in self.items[category]:
                    # 检查库存中是否有足够数量的物品
                    if inventory.get(item_id, 0) < amount:
                        return False
                    found = True
                    break
            
            if not found:
                return False
        
        return True
    
    def craft(self, recipe_id, inventory):
        """执行制作过程"""
        if not self.can_craft(recipe_id, inventory):
            return False, "材料不足"
        
        recipe = self.get_recipe(recipe_id)
        
        # 消耗材料
        for item_id, amount in recipe["requirements"].items():
            inventory[item_id] = inventory.get(item_id, 0) - amount
            if inventory[item_id] <= 0:
                del inventory[item_id]
        
        # 添加制作结果
        for item_id, amount in recipe["results"].items():
            inventory[item_id] = inventory.get(item_id, 0) + amount
        
        return True, f"成功制作了 {recipe['name']}"