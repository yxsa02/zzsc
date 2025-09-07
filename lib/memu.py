# memu.py
import os
import sys
import platform
import signal
from . import key
from .dp import AdaptiveDisplayBoard
from .world_manager import WorldManager

# 创建自适应显示板实例
board = AdaptiveDisplayBoard("ZZSC2", min_width=45)
world_manager = WorldManager()

# 全局变量来跟踪是否需要重绘
need_redraw = False

def handle_resize(signum, frame):
    """处理终端大小改变信号"""
    global need_redraw
    board.update_terminal_size()
    need_redraw = True

# 注册信号处理（仅限Unix/Linux/Mac）
if platform.system() != "Windows":
    signal.signal(signal.SIGWINCH, handle_resize)

def memu_start():
    menu_items = ["start", "load", "new", "setting", "exit"]
    mmb = ["hello", "lastplay:--", " ", " ", "chose your opt"]
    current_index = 0
    should_exit = False
    
    global need_redraw
    
    while not should_exit: 
        try:
            # 清除显示板内容
            board.clear()
            
            # 检查是否需要重绘（由于终端大小改变）
            if need_redraw:
                need_redraw = False
            
            # 获取最后游玩的世界信息
            worlds = world_manager.get_world_list()
            last_played = "--"
            for world_id, world_info in worlds.items():
                if world_info.get("is_active", False):
                    last_played = f"{world_info['name']} (Day {world_info['days_survived']})"
                    break
            
            mmb[1] = f"lastplay:{last_played}"
            
            # 添加菜单项
            for i, item in enumerate(menu_items):
                # 确保我们有对应的左侧文本
                left_text = mmb[i] if i < len(mmb) else ""
                prefix = ">" if i == current_index else " "
                board.add_line(left_text, f"{prefix}{item}")
            
            # 显示菜单
            board.display()
            print("使用方向键选择，回车确认，ESC退出")
            
            # 获取用户输入
            k = key.getch()
            current_index, should_exit, should_execute = key.dokey(k, current_index, menu_items)
            
            if should_execute:
                selected = menu_items[current_index]
                if selected.strip():  # 只返回非空菜单项
                    print("loading……")
                    return selected
            elif should_exit:
                return "exit"
                
        except KeyboardInterrupt:
            print("\n程序已退出")
            return "exit"
        except Exception as e:
            print(f"错误: {e}")
            continue

def memu_load_world():
    """加载世界菜单"""
    worlds = world_manager.get_world_list()
    world_ids = list(worlds.keys())
    world_names = [worlds[wid]["name"] for wid in world_ids]
    
    if not world_names:
        print("没有可加载的世界")
        input("按回车键继续...")
        return None
    
    menu_items = world_names + ["返回"]
    current_index = 0
    should_exit = False
    
    global need_redraw
    
    while not should_exit: 
        try:
            # 清除显示板内容
            board.clear()
            
            # 检查是否需要重绘（由于终端大小改变）
            if need_redraw:
                need_redraw = False
            
            # 添加菜单项
            board.add_line("选择世界", "")
            board.add_line("", "")
            
            for i, item in enumerate(menu_items):
                prefix = ">" if i == current_index else " "
                days_info = ""
                
                if i < len(world_names):
                    world_id = world_ids[i]
                    world_info = worlds[world_id]
                    days_info = f"Day {world_info['days_survived']}"
                
                board.add_line(f"{prefix}{item}", days_info)
            
            # 显示菜单
            board.display()
            print("使用方向键选择，回车确认，ESC返回")
            
            # 获取用户输入
            k = key.getch()
            current_index, should_exit, should_execute = key.dokey(k, current_index, menu_items)
            
            if should_execute:
                if current_index < len(world_names):
                    selected_world = world_ids[current_index]
                    print("loading……")
                    return selected_world
                else:
                    return None
            elif should_exit:
                return None
                
        except KeyboardInterrupt:
            print("\n程序已退出")
            return None
        except Exception as e:
            print(f"错误: {e}")
            continue

def memu_newworld(nwn, nwm):
    """新世界菜单 - 修改为创建新世界"""
    menu_items = ["OK", "remake", "edit", "import", "back"]
    mmb = ["New World", f"WorldName:{nwn}", " ", " ", "chose your opt"]
    current_index = 0
    should_exit = False
    
    global need_redraw
    
    while not should_exit: 
        try:
            # 清除显示板内容
            board.clear()
            
            # 检查是否需要重绘（由于终端大小改变）
            if need_redraw:
                need_redraw = False
            
            # 添加菜单项
            for i, item in enumerate(menu_items):
                # 确保我们有对应的左侧文本
                left_text = mmb[i] if i < len(mmb) else ""
                prefix = ">" if i == current_index else " "
                board.add_line(left_text, f"{prefix}{item}")
            
            # 显示菜单
            board.display()
            print("使用方向键选择，回车确认，ESC退出")
            
            # 获取用户输入
            k = key.getch()
            current_index, should_exit, should_execute = key.dokey(k, current_index, menu_items)
            
            if should_execute:
                selected = menu_items[current_index]
                if selected.strip():  # 只返回非空菜单项
                    print("loading……")
                    
                    if selected == "OK":
                        # 创建新世界
                        world_id = world_manager.create_world(nwn)
                        return world_id
                    else:
                        return selected
            elif should_exit:
                return "back"
                
        except KeyboardInterrupt:
            print("\n程序已退出")
            return "back"
        except Exception as e:
            print(f"错误: {e}")
            continue