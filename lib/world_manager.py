# lib/world_manager.py
# lib/world_manager.py
import os
import json
import time
from datetime import datetime
from .item_system import ItemManager, InventoryManager, Inventory  # 确保 Inventory 被导入

class WorldManager:
    def __init__(self):
        self.worlds_dir = "worlds"
        self.meta_file = os.path.join(self.worlds_dir, "world_meta.json")
        self.current_world = None
        self.item_manager = ItemManager()
        
        # 确保世界目录存在
        if not os.path.exists(self.worlds_dir):
            os.makedirs(self.worlds_dir)
        
        # 确保元数据文件存在
        if not os.path.exists(self.meta_file):
            self._init_meta_file()
    
    def _init_meta_file(self):
        """初始化元数据文件"""
        meta_data = {
            "version": "1.0",
            "worlds": {}
        }
        with open(self.meta_file, "w", encoding="utf-8") as f:
            json.dump(meta_data, f, indent=2, ensure_ascii=False)
    
    def load_meta_data(self):
        """加载元数据"""
        try:
            with open(self.meta_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            self._init_meta_file()
            return self.load_meta_data()
    
    def save_meta_data(self, meta_data):
        """保存元数据"""
        with open(self.meta_file, "w", encoding="utf-8") as f:
            json.dump(meta_data, f, indent=2, ensure_ascii=False)
    
    def get_world_list(self):
        """获取世界列表"""
        meta_data = self.load_meta_data()
        return meta_data.get("worlds", {})
    
    def create_world(self, world_name, player_name="幸存者", difficulty="normal"):
        """创建新世界"""
        meta_data = self.load_meta_data()
        worlds = meta_data.get("worlds", {})
        
        # 生成唯一的世界ID
        world_id = f"world_{len(worlds) + 1}"
        
        # 创建世界目录
        world_dir = os.path.join(self.worlds_dir, world_id)
        if not os.path.exists(world_dir):
            os.makedirs(world_dir)
        
        # 初始化世界数据
        world_data = {
            "player": {
                "name": player_name,
                "health": 100,
                "hunger": 80,
                "thirst": 70,
                "energy": 90,
                "day": 1,
                "location": "安全屋",
                "skills": {
                    "scavenging": 1,
                    "crafting": 1,
                    "combat": 1
                }
            },
            "world_state": {
                "discovered_locations": ["安全屋"],
                "completed_quests": [],
                "active_quests": ["寻找食物", "寻找水源"],
                "npc_relations": {},
                "base_level": 1,
                "base_resources": {
                    "water_collector": 0,
                    "garden": 0,
                    "workshop": 0
                }
            },
            "game_settings": {
                "difficulty": difficulty,
                "autosave": True,
                "sound_volume": 80,
                "music_volume": 60
            },
            "system": {
                "version": "1.0",
                "created": datetime.now().isoformat(),
                "last_saved": datetime.now().isoformat(),
                "play_time": "00:00:00"
            }
        }
        
        # 保存世界数据
        world_file = os.path.join(world_dir, "save_data.json")
        with open(world_file, "w", encoding="utf-8") as f:
            json.dump(world_data, f, indent=2, ensure_ascii=False)
        
        # 创建初始库存
        inventory_manager = InventoryManager(world_id, self.item_manager)
        inventory = Inventory()
        
        # 添加初始物品
        initial_items = {
            "canned_food": 3,
            "bottled_water": 2,
            "bandage": 1,
            "scrap_metal": 5
        }
        
        for item_id, quantity in initial_items.items():
            item_data = self.item_manager.get_item(item_id)
            if item_data:
                inventory.add_item(item_id, item_data, quantity)
        
        # 保存库存
        inventory_manager.save_inventory(inventory)
        
        # 更新元数据
        worlds[world_id] = {
            "name": world_name,
            "created": datetime.now().isoformat(),
            "last_played": datetime.now().isoformat(),
            "days_survived": 1,
            "player_name": player_name,
            "difficulty": difficulty,
            "is_active": True,
            "inventory": {
                "capacity": inventory.capacity,
                "current_weight": inventory.get_total_weight(),
                "item_count": len(inventory.items)
            }
        }
        
        meta_data["worlds"] = worlds
        self.save_meta_data(meta_data)
        
        return world_id
    
    def load_world(self, world_id):
        """加载世界"""
        world_file = os.path.join(self.worlds_dir, world_id, "save_data.json")
        
        try:
            with open(world_file, "r", encoding="utf-8") as f:
                world_data = json.load(f)
            
            # 加载库存
            inventory_manager = InventoryManager(world_id, self.item_manager)
            inventory = inventory_manager.load_inventory()
            
            # 更新元数据中的最后游玩时间
            meta_data = self.load_meta_data()
            if world_id in meta_data["worlds"]:
                meta_data["worlds"][world_id]["last_played"] = datetime.now().isoformat()
                meta_data["worlds"][world_id]["days_survived"] = world_data["player"]["day"]
                meta_data["worlds"][world_id]["inventory"] = {
                    "capacity": inventory.capacity,
                    "current_weight": inventory.get_total_weight(),
                    "item_count": len(inventory.items)
                }
                self.save_meta_data(meta_data)
            
            self.current_world = world_id
            return world_data, inventory
        except FileNotFoundError:
            print(f"世界 {world_id} 不存在")
            return None, None
    
    def save_world(self, world_data, inventory):
        """保存世界"""
        if not self.current_world:
            print("没有当前激活的世界")
            return False
        
        world_file = os.path.join(self.worlds_dir, self.current_world, "save_data.json")
        
        # 更新最后保存时间
        world_data["system"]["last_saved"] = datetime.now().isoformat()
        
        try:
            with open(world_file, "w", encoding="utf-8") as f:
                json.dump(world_data, f, indent=2, ensure_ascii=False)
            
            # 保存库存
            inventory_manager = InventoryManager(self.current_world, self.item_manager)
            inventory_manager.save_inventory(inventory)
            
            # 更新元数据中的库存信息
            meta_data = self.load_meta_data()
            if self.current_world in meta_data["worlds"]:
                meta_data["worlds"][self.current_world]["inventory"] = {
                    "capacity": inventory.capacity,
                    "current_weight": inventory.get_total_weight(),
                    "item_count": len(inventory.items)
                }
                self.save_meta_data(meta_data)
            
            return True
        except Exception as e:
            print(f"保存世界时出错: {e}")
            return False
    
    def delete_world(self, world_id):
        """删除世界"""
        meta_data = self.load_meta_data()
        
        if world_id in meta_data["worlds"]:
            # 从元数据中移除
            del meta_data["worlds"][world_id]
            self.save_meta_data(meta_data)
            
            # 删除世界目录
            world_dir = os.path.join(self.worlds_dir, world_id)
            if os.path.exists(world_dir):
                import shutil
                shutil.rmtree(world_dir)
            
            return True
        return False
    
    def get_world_info(self, world_id):
        """获取世界信息"""
        meta_data = self.load_meta_data()
        return meta_data["worlds"].get(world_id, {})