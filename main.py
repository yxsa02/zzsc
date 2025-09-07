# main.py
from lib import memu
from lib.world_manager import WorldManager
from lib.game_loop import GameLoop

world_manager = WorldManager()
game_loop = GameLoop(world_manager)

while True:
    bootopt = memu.memu_start()
    
    if bootopt == "exit":
        break
        
    elif bootopt == "start":
        # 加载现有世界
        world_id = memu.memu_load_world()
        if world_id:
            world_data, inventory = world_manager.load_world(world_id)
            if world_data:
                print(f"进入世界: {world_manager.get_world_info(world_id)['name']}")
                game_loop.start(world_data, inventory)
                
    elif bootopt == "new":
        nwn = "New World"
        while True:         
            nwopt = memu.memu_newworld(nwn, "")
                    
            if nwopt == "back":
                break
                
            elif nwopt == "edit":
                nwn = input("输入世界名: ")
                
            elif isinstance(nwopt, str) and nwopt.startswith("world_"):
                # 新世界创建成功，进入游戏
                world_data, inventory = world_manager.load_world(nwopt)
                if world_data:
                    print(f"进入新世界: {nwn}")
                    game_loop.start(world_data, inventory)
                    break