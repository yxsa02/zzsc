# loop.py
import time
from datetime import datetime
from .memu import *
from .item import ItemManager

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
        self.world_data = world_data
        self.inventory = inventory
        
        # 游戏主循环
        while self.running:
            # 显示游戏状态并获取玩家操作
            action = memu_game_main(self.world_data, self.inventory)  # 直接使用函数名
            
            # 处理游戏逻辑
            self.process_action(action)
            
            # 更新游戏状态（时间流逝、资源消耗等）
            self.update_game_state()
            
            # 自动保存
            if self.world_data["game_settings"]["autosave"]:
                self.world_manager.save_world(self.world_data, self.inventory)
            
            # 检查游戏结束条件
            if self.check_game_over():
                break
    
    def process_action(self, action):
        """处理玩家行动"""
        if action == "explore":
            self.explore()
        elif action == "rest":
            self.rest()
        elif action == "inventory":
            self.show_inventory()
        elif action == "craft":
            self.show_crafting()
        elif action == "quests":
            self.show_quests()
        elif action == "settings":
            self.show_world_settings()
        elif action == "save_and_exit":
            self.running = False
            self.world_manager.save_world(self.world_data, self.inventory)
    
    def explore(self):
        """探索行动"""
        # 探索逻辑
        player = self.world_data["player"]
        difficulty = self.world_data["game_settings"]["difficulty"]
        
        # 消耗精力
        player["energy"] = max(0, player["energy"] - 15)
        
        # 随机物品掉落
        item_drop = {
            "easy": {"canned_food": 2, "bottled_water": 2, "scrap_metal": 4, "bandage": 1},
            "normal": {"canned_food": 1, "bottled_water": 1, "scrap_metal": 3, "bandage": 0},
            "hard": {"canned_food": 1, "bottled_water": 0, "scrap_metal": 2, "bandage": 0}
        }[difficulty]
        
        # 添加物品到库存
        results = []
        for item_id, qty in item_drop.items():
            item_data = self.item_manager.get_item(item_id)
            if item_data:
                success, msg = self.inventory.add_item(item_id, item_data, qty)
                results.append(msg)
        
        # 显示探索结果
        memu_show_explore_results(results, player["energy"])  # 直接使用函数名
    
    def rest(self):
        """休息行动"""
        player = self.world_data["player"]
        
        # 恢复精力，消耗饥饿/口渴
        player["energy"] = min(100, player["energy"] + 35)
        player["hunger"] = min(100, player["hunger"] + 8)
        player["thirst"] = min(100, player["thirst"] + 10)
        
        # 健康惩罚
        penalty = ""
        if player["hunger"] >= 90 or player["thirst"] >= 90:
            player["health"] = max(0, player["health"] - 5)
            penalty = "（健康因饥渴下降5！）"
        
        # 显示休息结果
        memu_show_rest_results(player["energy"], player["hunger"], player["thirst"], penalty)  # 直接使用函数名
    
    def show_inventory(self):
        """显示库存"""
        # 获取库存物品列表
        item_list = list(self.inventory.items.values())
        
        if not item_list:
            memu_show_message("库存为空", "没有可查看的物品")  # 直接使用函数名
            return
        
        # 显示库存并获取用户选择
        selected_item_idx = memu_show_inventory(item_list)  # 直接使用函数名
        
        if selected_item_idx is not None:
            # 使用选中的物品
            selected_item = item_list[selected_item_idx]
            success, msg = self.inventory.use_item(selected_item.id, self.world_data["player"])
            
            # 显示使用结果
            player = self.world_data["player"]
            memu_show_item_use_result(  # 直接使用函数名
                msg, 
                player["health"], 
                player["hunger"], 
                player["thirst"]
            )
    
    def show_crafting(self):
        """显示制作菜单"""
        craftable_items = self.item_manager.get_craftable_items(self.inventory)
        
        if not craftable_items:
            memu_show_message("制作", "没有足够材料制作任何物品")  # 直接使用函数名
            return
        
        # 显示制作菜单并获取用户选择
        selected_recipe_idx = memu_show_crafting(craftable_items, self.item_manager, self.inventory)  # 直接使用函数名
        
        if selected_recipe_idx is not None:
            # 执行制作
            recipe_id, recipe = craftable_items[selected_recipe_idx]
            success, msg = self.item_manager.craft(recipe_id, self.inventory)
            
            # 显示制作结果
            memu_show_craft_result(msg)  # 直接使用函数名
    
    def show_quests(self):
        """显示任务"""
        world_state = self.world_data["world_state"]
        active = world_state["active_quests"]
        completed = world_state["completed_quests"]
        
        memu_show_quests(active, completed)  # 直接使用函数名
    
    def show_world_settings(self):
        """显示世界设置"""
        world_id = self.world_manager.current_world
        memu_world_settings(world_id)  # 直接使用函数名
    
    def update_game_state(self):
        """更新游戏状态"""
        player = self.world_data["player"]
        
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
            
            # 显示新的一天
            memu_show_new_day(player["day"])  # 直接使用函数名
    
    def check_game_over(self):
        """检查游戏结束条件"""
        if self.world_data["player"]["health"] <= 0:
            # 显示游戏结束画面
            memu_show_game_over(self.world_data["player"]["day"])  # 直接使用函数名
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