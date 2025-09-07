# lib/game_loop.py
import time
from datetime import datetime
from .item_system import ItemManager

class GameLoop:
    def __init__(self, world_manager):
        self.world_manager = world_manager
        self.running = False
        self.start_time = None
        self.item_manager = ItemManager()
    
    def start(self, world_data, inventory):
        """开始游戏循环"""
        self.running = True
        self.start_time = time.time()
        
        # 游戏主循环
        while self.running:
            # 显示游戏状态
            self.display_status(world_data, inventory)
            
            # 获取玩家输入
            action = self.get_player_action()
            
            # 处理游戏逻辑
            self.process_action(action, world_data, inventory)
            
            # 更新游戏状态（时间流逝、资源消耗等）
            self.update_game_state(world_data)
            
            # 自动保存
            if world_data["game_settings"]["autosave"]:
                self.world_manager.save_world(world_data, inventory)
            
            # 检查游戏结束条件
            if self.check_game_over(world_data):
                break
    
    def display_status(self, world_data, inventory):
        """显示游戏状态"""
        player = world_data["player"]
        print(f"=== Day {player['day']} ===")
        print(f"健康: {player['health']}/100  饥饿: {player['hunger']}/100")
        print(f"口渴: {player['thirst']}/100  精力: {player['energy']}/100")
        print(f"位置: {player['location']}")
        print(f"负重: {inventory.get_total_weight()}/{inventory.capacity}")
        print("=" * 30)
        
        # 显示可用行动
        print("1. 探索")
        print("2. 休息")
        print("3. 物品")
        print("4. 制作")
        print("5. 移动")
        print("6. 保存并退出")
    
    def get_player_action(self):
        """获取玩家行动"""
        return input("选择行动: ")
    
    def process_action(self, action, world_data, inventory):
        """处理玩家行动"""
        if action == "1":
            self.explore(world_data, inventory)
        elif action == "2":
            self.rest(world_data)
        elif action == "3":
            self.show_inventory(world_data, inventory)
        elif action == "4":
            self.show_crafting(inventory)
        elif action == "6":
            self.running = False
    
    def explore(self, world_data, inventory):
        """探索行动"""
        print("探索中...")
        # 这里添加探索逻辑，包括发现物品
        
        # 模拟发现物品
        found_items = {
            "canned_food": 2,
            "bottled_water": 1,
            "scrap_metal": 3
        }
        
        for item_id, quantity in found_items.items():
            item_data = self.item_manager.get_item(item_id)
            if item_data:
                success, message = inventory.add_item(item_id, item_data, quantity)
                print(message)
        
        # 消耗能量
        world_data["player"]["energy"] = max(0, world_data["player"]["energy"] - 10)
        
        input("按回车继续...")
    
    def rest(self, world_data):
        """休息行动"""
        print("休息中...")
        # 恢复能量，但消耗资源
        world_data["player"]["energy"] = min(100, world_data["player"]["energy"] + 30)
        world_data["player"]["hunger"] += 5
        world_data["player"]["thirst"] += 7
        
        input("按回车继续...")
    
    def show_inventory(self, world_data, inventory):
        """显示库存"""
        inventory.display()
        
        # 提供使用物品的选项
        if inventory.items:
            item_id = input("输入要使用的物品ID（或按回车返回）: ")
            if item_id and item_id in inventory.items:
                success, message = inventory.use_item(item_id, world_data["player"])
                print(message)
        
        input("按回车继续...")
    
    def show_crafting(self, inventory):
        """显示制作菜单"""
        craftable_items = self.item_manager.get_craftable_items(inventory)
        
        if not craftable_items:
            print("没有可制作的物品")
            input("按回车继续...")
            return
        
        print("可制作的物品:")
        for i, (recipe_id, recipe) in enumerate(craftable_items):
            print(f"{i+1}. {recipe['name']}")
            for req_item, req_amount in recipe["requirements"].items():
                req_data = self.item_manager.get_item(req_item)
                if req_data:
                    print(f"  需要: {req_data['name']} x{req_amount}")
        
        choice = input("选择要制作的物品（或按回车返回）: ")
        if choice and choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(craftable_items):
                recipe_id, recipe = craftable_items[index]
                success, message = self.item_manager.craft(recipe_id, inventory)
                print(message)
        
        input("按回车继续...")
    
    def update_game_state(self, world_data):
        """更新游戏状态"""
        player = world_data["player"]
        
        # 时间流逝，资源消耗
        player["hunger"] += 1
        player["thirst"] += 2
        player["energy"] -= 0.5
        
        # 确保数值在合理范围内
        player["hunger"] = min(100, max(0, player["hunger"]))
        player["thirst"] = min(100, max(0, player["thirst"]))
        player["energy"] = min(100, max(0, player["energy"]))
        
        # 如果饥饿或口渴过高，健康值下降
        if player["hunger"] >= 90 or player["thirst"] >= 90:
            player["health"] -= 2
        
        # 确保健康值在合理范围内
        player["health"] = min(100, max(0, player["health"]))
        
        # 每天增加一天
        if player["energy"] <= 0:
            player["day"] += 1
            player["energy"] = 50  # 恢复部分能量
            print(f"新的一天开始了! 第 {player['day']} 天")
    
    def check_game_over(self, world_data):
        """检查游戏结束条件"""
        if world_data["player"]["health"] <= 0:
            print("游戏结束 - 你已死亡")
            return True
        return False
    
    def calculate_play_time(self):
        """计算游戏时间"""
        if self.start_time:
            elapsed = time.time() - self.start_time
            hours = int(elapsed // 3600)
            minutes = int((elapsed % 3600) // 60)
            seconds = int(elapsed % 60)
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        return "00:00:00"