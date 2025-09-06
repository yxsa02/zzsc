# lib/inventory.py
from . import item_system

class Inventory:
    def __init__(self):
        self.items = {}  # 格式: {item_id: quantity}
        self.capacity = 50  # 初始容量
        self.item_system = item_system.ItemSystem()
    
    def add_item(self, item_id, quantity=1):
        """添加物品到库存"""
        # 首先检查物品是否存在
        item_info = None
        for category in self.item_system.items:
            if item_id in self.item_system.items[category]:
                item_info = self.item_system.items[category][item_id]
                break
        
        if not item_info:
            return False, "未知物品"
        
        # 检查是否可堆叠
        if item_info.get("stackable", True):
            current_quantity = self.items.get(item_id, 0)
            max_stack = item_info.get("max_stack", 1)
            
            # 检查是否会超过堆叠限制
            if current_quantity + quantity > max_stack:
                # 计算需要创建多少个新堆叠
                stacks_needed = (current_quantity + quantity + max_stack - 1) // max_stack
                if self.get_total_items() + stacks_needed > self.capacity:
                    return False, "库存已满"
                
                self.items[item_id] = max_stack
                remaining = current_quantity + quantity - max_stack
                
                # 添加额外的堆叠
                while remaining > 0:
                    add_amount = min(remaining, max_stack)
                    self.items[f"{item_id}_{len(self.items)}"] = add_amount
                    remaining -= add_amount
            else:
                self.items[item_id] = current_quantity + quantity
        else:
            # 不可堆叠物品
            if self.get_total_items() + quantity > self.capacity:
                return False, "库存已满"
            
            # 为每个物品创建唯一ID
            for i in range(quantity):
                unique_id = f"{item_id}_{len(self.items)}"
                self.items[unique_id] = 1
        
        return True, f"获得了 {quantity} 个 {item_info['name']}"
    
    def remove_item(self, item_id, quantity=1):
        """从库存中移除物品"""
        if item_id not in self.items:
            return False, "物品不存在"
        
        if self.items[item_id] < quantity:
            return False, "数量不足"
        
        self.items[item_id] -= quantity
        if self.items[item_id] <= 0:
            del self.items[item_id]
        
        return True, f"移除了 {quantity} 个物品"
    
    def get_item_count(self, item_id):
        """获取特定物品的数量"""
        count = 0
        for key, value in self.items.items():
            if key.startswith(item_id):
                count += value
        return count
    
    def get_total_items(self):
        """获取库存中物品的总数"""
        return sum(self.items.values())
    
    def get_inventory_weight(self):
        """计算库存总重量"""
        total_weight = 0
        for item_id, quantity in self.items.items():
            base_item_id = item_id.split('_')[0]  # 获取基础物品ID
            for category in self.item_system.items:
                if base_item_id in self.item_system.items[category]:
                    item_info = self.item_system.items[category][base_item_id]
                    total_weight += item_info.get("weight", 0) * quantity
                    break
        
        return total_weight
    
    def display(self):
        """显示库存内容"""
        if not self.items:
            print("库存为空")
            return
        
        # 按类别分组物品
        categorized = {}
        for item_id, quantity in self.items.items():
            base_item_id = item_id.split('_')[0]
            for category in self.item_system.items:
                if base_item_id in self.item_system.items[category]:
                    if category not in categorized:
                        categorized[category] = []
                    
                    item_info = self.item_system.items[category][base_item_id]
                    categorized[category].append({
                        "id": item_id,
                        "name": item_info["name"],
                        "quantity": quantity,
                        "info": item_info
                    })
                    break
        
        # 显示库存
        for category, items in categorized.items():
            print(f"\n{category.upper()}:")
            for item in items:
                print(f"  {item['name']} x{item['quantity']}")
                if "description" in item["info"]:
                    print(f"    {item['info']['description']}")