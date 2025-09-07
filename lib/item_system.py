# lib/item_system.py
import json
import os
from datetime import datetime

class Item:
    """物品类，表示游戏中的一个具体物品"""
    def __init__(self, item_id, item_data, quantity=1, durability=None):
        self.id = item_id
        self.name = item_data.get("name", "未知物品")
        self.description = item_data.get("description", "")
        self.category = item_data.get("category", "misc")
        self.weight = item_data.get("weight", 0)
        self.durability = durability if durability is not None else item_data.get("durability", 1)
        self.max_durability = item_data.get("durability", 1)
        self.stackable = item_data.get("stackable", True)
        self.max_stack = item_data.get("max_stack", 1)
        self.value = item_data.get("value", 0)
        self.quantity = quantity
        
        # 类别特定属性
        self.nutrition = item_data.get("nutrition", 0)  # 食物
        self.hydration = item_data.get("hydration", 0)  # 水
        self.health_effect = item_data.get("health_effect", 0)  # 医疗
        self.damage = item_data.get("damage", 0)  # 武器/工具
        self.ammo_type = item_data.get("ammo_type", None)  # 武器
        self.battery_required = item_data.get("battery_required", False)  # 工具
    
    def use(self, player):
        """使用物品并应用效果"""
        if self.category == "food":
            player["hunger"] = max(0, player["hunger"] - self.nutrition)
            player["health"] = min(100, player["health"] + self.health_effect)
            return f"食用了 {self.name}"
            
        elif self.category == "water":
            player["thirst"] = max(0, player["thirst"] - self.hydration)
            player["health"] = min(100, player["health"] + self.health_effect)
            return f"饮用了 {self.name}"
            
        elif self.category == "medical":
            player["health"] = min(100, player["health"] + self.health_effect)
            return f"使用了 {self.name}"
            
        elif self.category in ["tools", "weapons"]:
            return f"装备了 {self.name}"
            
        else:
            return f"{self.name} 无法直接使用"
    
    def degrade(self, amount=1):
        """降低物品耐久度"""
        if self.durability > 0:
            self.durability -= amount
            return self.durability <= 0  # 返回是否完全损坏
        return True
    
    def repair(self, amount=1):
        """修复物品耐久度"""
        self.durability = min(self.max_durability, self.durability + amount)
    
    def to_dict(self):
        """将物品转换为字典格式，用于保存"""
        return {
            "id": self.id,
            "quantity": self.quantity,
            "durability": self.durability
        }
    
    @classmethod
    def from_dict(cls, item_dict, item_data):
        """从字典创建物品实例"""
        return cls(
            item_dict["id"],
            item_data,
            item_dict.get("quantity", 1),
            item_dict.get("durability", None)
        )
    
    def __str__(self):
        if self.stackable and self.quantity > 1:
            return f"{self.name} x{self.quantity}"
        elif self.durability != self.max_durability:
            return f"{self.name} ({self.durability}/{self.max_durability})"
        return self.name


class Inventory:
    """库存类，管理玩家的物品集合"""
    def __init__(self, capacity=50):
        self.items = {}  # 格式: {item_id: Item实例}
        self.capacity = capacity
        self.current_weight = 0
    
    def add_item(self, item_id, item_data, quantity=1):
        """添加物品到库存"""
        # 检查物品是否已存在且可堆叠
        if item_id in self.items and self.items[item_id].stackable:
            # 检查是否会超过堆叠限制
            if self.items[item_id].quantity + quantity <= self.items[item_id].max_stack:
                self.items[item_id].quantity += quantity
                self.current_weight += item_data.get("weight", 0) * quantity
                return True, f"获得了 {quantity} 个 {item_data['name']}"
            else:
                # 计算可以添加的数量
                can_add = self.items[item_id].max_stack - self.items[item_id].quantity
                if can_add > 0:
                    self.items[item_id].quantity += can_add
                    self.current_weight += item_data.get("weight", 0) * can_add
                    remaining = quantity - can_add
                    return False, f"获得了 {can_add} 个 {item_data['name']}，{remaining} 个无法添加（超过堆叠限制）"
                else:
                    return False, f"无法添加 {item_data['name']}（超过堆叠限制）"
        else:
            # 检查库存是否已满
            if len(self.items) >= self.capacity:
                return False, "库存已满"
            
            # 创建新物品实例
            new_item = Item(item_id, item_data, quantity)
            self.items[item_id] = new_item
            self.current_weight += item_data.get("weight", 0) * quantity
            return True, f"获得了 {quantity} 个 {item_data['name']}"
    
    def remove_item(self, item_id, quantity=1):
        """从库存中移除物品"""
        if item_id not in self.items:
            return False, "物品不存在"
        
        item = self.items[item_id]
        
        if item.stackable:
            if item.quantity < quantity:
                return False, "数量不足"
            
            item.quantity -= quantity
            self.current_weight -= item.weight * quantity
            
            if item.quantity <= 0:
                del self.items[item_id]
                
            return True, f"移除了 {quantity} 个 {item.name}"
        else:
            del self.items[item_id]
            self.current_weight -= item.weight
            return True, f"移除了 {item.name}"
    
    def use_item(self, item_id, player):
        """使用物品"""
        if item_id not in self.items:
            return False, "物品不存在"
        
        item = self.items[item_id]
        result = item.use(player)
        
        # 消耗性物品使用后减少数量或移除
        if item.category in ["food", "water", "medical"]:
            if item.stackable:
                self.remove_item(item_id, 1)
            else:
                if item.degrade():
                    self.remove_item(item_id)
        
        return True, result
    
    def get_item(self, item_id):
        """获取特定物品"""
        return self.items.get(item_id, None)
    
    def get_items_by_category(self, category):
        """获取特定类别的所有物品"""
        return [item for item in self.items.values() if item.category == category]
    
    def get_total_weight(self):
        """获取库存总重量"""
        return self.current_weight
    
    def get_remaining_capacity(self):
        """获取剩余容量"""
        return self.capacity - len(self.items)
    
    def to_dict(self):
        """将库存转换为字典格式，用于保存"""
        return {
            "capacity": self.capacity,
            "current_weight": self.current_weight,
            "items": [item.to_dict() for item in self.items.values()]
        }
    
    @classmethod
    def from_dict(cls, inventory_dict, item_manager):
        """从字典创建库存实例"""
        inventory = cls(inventory_dict.get("capacity", 50))
        inventory.current_weight = inventory_dict.get("current_weight", 0)
        
        for item_dict in inventory_dict.get("items", []):
            item_data = item_manager.get_item(item_dict["id"])
            if item_data:
                item = Item.from_dict(item_dict, item_data)
                inventory.items[item.id] = item
        
        return inventory
    
    def display(self):
        """显示库存内容"""
        if not self.items:
            print("库存为空")
            return
        
        # 按类别分组物品
        categorized = {}
        for item in self.items.values():
            if item.category not in categorized:
                categorized[item.category] = []
            categorized[item.category].append(item)
        
        # 显示库存
        for category, items in categorized.items():
            print(f"\n{category.upper()}:")
            for item in items:
                print(f"  {item}")
                if item.description:
                    print(f"    {item.description}")


class ItemManager:
    """物品管理器，加载和管理物品数据"""
    def __init__(self):
        self.items = {}
        self.crafting_recipes = {}
        self.load_items()
    
    def load_items(self):
        """从JSON文件加载物品数据"""
        try:
            with open("res/items.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                self.items = data.get("items", {})
                self.crafting_recipes = data.get("crafting_recipes", {})
                
                # 为每个物品添加类别信息
                for category, category_items in self.items.items():
                    for item_id, item_data in category_items.items():
                        item_data["category"] = category
        except FileNotFoundError:
            print("物品数据文件未找到!")
            self.items = {}
            self.crafting_recipes = {}
    
    def get_item(self, item_id):
        """获取物品数据"""
        for category, category_items in self.items.items():
            if item_id in category_items:
                return category_items[item_id]
        return None
    
    def get_recipe(self, recipe_id):
        """获取制作配方"""
        return self.crafting_recipes.get(recipe_id, None)
    
    def get_all_recipes(self):
        """获取所有制作配方"""
        return self.crafting_recipes
    
    def get_craftable_items(self, inventory):
        """获取可制作的物品列表"""
        craftable = []
        
        for recipe_id, recipe in self.crafting_recipes.items():
            if self.can_craft(recipe_id, inventory):
                craftable.append((recipe_id, recipe))
        
        return craftable
    
    def can_craft(self, recipe_id, inventory):
        """检查是否满足制作条件"""
        recipe = self.get_recipe(recipe_id)
        if not recipe:
            return False
        
        for required_item, required_amount in recipe["requirements"].items():
            # 检查库存中是否有足够数量的物品
            if required_item not in inventory.items or inventory.items[required_item].quantity < required_amount:
                return False
        
        return True
    
    def craft(self, recipe_id, inventory):
        """执行制作过程"""
        if not self.can_craft(recipe_id, inventory):
            return False, "材料不足"
        
        recipe = self.get_recipe(recipe_id)
        
        # 消耗材料
        for required_item, required_amount in recipe["requirements"].items():
            inventory.remove_item(required_item, required_amount)
        
        # 添加制作结果
        for result_item, result_amount in recipe["results"].items():
            item_data = self.get_item(result_item)
            if item_data:
                inventory.add_item(result_item, item_data, result_amount)
        
        return True, f"成功制作了 {recipe['name']}"


class InventoryManager:
    """库存管理器，处理库存的保存和加载"""
    def __init__(self, world_id, item_manager):
        self.world_id = world_id
        self.item_manager = item_manager
        self.inventory_file = f"worlds/{world_id}/inventory.json"
    
    def save_inventory(self, inventory):
        """保存库存数据到文件"""
        # 确保目录存在
        os.makedirs(os.path.dirname(self.inventory_file), exist_ok=True)
        
        # 转换为字典格式
        inventory_data = inventory.to_dict()
        
        # 保存到文件
        with open(self.inventory_file, "w", encoding="utf-8") as f:
            json.dump(inventory_data, f, indent=2, ensure_ascii=False)
        
        return True
    
    def load_inventory(self):
        """从文件加载库存数据"""
        try:
            with open(self.inventory_file, "r", encoding="utf-8") as f:
                inventory_data = json.load(f)
            
            # 从字典创建库存实例
            return Inventory.from_dict(inventory_data, self.item_manager)
        except FileNotFoundError:
            # 如果文件不存在，创建新的库存
            print("库存文件未找到，创建新库存")
            return Inventory()
        except Exception as e:
            print(f"加载库存时出错: {e}")
            return Inventory()