# memu.py
import os
import sys
import platform
import signal
from . import key
from .dp import AdaptiveDisplayBoard
from .world_manager import WorldManager

# 创建自适应显示板实例
board = AdaptiveDisplayBoard("ZZSC", min_width=45)
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
    menu_items = ["继续游戏", "新的世界", "设置", "退出游戏"]
    mmb = ["欢迎来到ZZSC", "最后游玩: --", " ", "请选择操作"]
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
                    last_played = f"{world_info['name']} (第{world_info['days_survived']}天)"
                    break
            
            mmb[1] = f"最后游玩: {last_played}"
            
            # 添加菜单项
            for i, item in enumerate(menu_items):
                # 确保我们有对应的左侧文本
                left_text = mmb[i] if i < len(mmb) else ""
                prefix = ">" if i == current_index else " "
                board.add_line(left_text, f"{prefix}{item}")
            
            # 显示菜单
            board.display()
            print("使用方向键选择，回车确认，ESC退出")
            
            # 使用新的 get() 函数获取用户输入
            pressed_key = key.get()
            
            # 处理按键
            if pressed_key == "up":
                current_index = (current_index - 1) % len(menu_items)
            elif pressed_key == "down":
                current_index = (current_index + 1) % len(menu_items)
            elif pressed_key == "enter":
                selected = menu_items[current_index]
                if selected.strip():  # 只返回非空菜单项
                    print("加载中……")
                    # 将中文选项映射回英文标识符
                    option_map = {
                        "开始游戏": "start",
                        "加载存档": "load",
                        "新的世界": "new",
                        "设置": "setting",
                        "退出游戏": "exit"
                    }
                    return option_map.get(selected, selected)
            elif pressed_key == "esc":
                return "exit"
            elif pressed_key == "q":
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
                    days_info = f"第{world_info['days_survived']}天"
                
                board.add_line(f"{prefix}{item}", days_info)
            
            # 显示菜单
            board.display()
            print("使用方向键选择，回车确认，ESC返回")
            
            # 使用新的 get() 函数获取用户输入
            pressed_key = key.get()
            
            # 处理按键
            if pressed_key == "up":
                current_index = (current_index - 1) % len(menu_items)
            elif pressed_key == "down":
                current_index = (current_index + 1) % len(menu_items)
            elif pressed_key == "enter":
                if current_index < len(world_names):
                    selected_world = world_ids[current_index]
                    print("加载中……")
                    return selected_world
                else:
                    return None
            elif pressed_key == "esc":
                return None
                
        except KeyboardInterrupt:
            print("\n程序已退出")
            return None
        except Exception as e:
            print(f"错误: {e}")
            continue

def memu_newworld(nwn, nwm):
    """新世界菜单"""
    menu_items = ["确认创建", "重新命名", "编辑设置", "导入世界", "返回"]
    mmb = ["创建新世界", f"世界名称: {nwn}", " ", " ", "请选择操作"]
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
            
            # 使用新的 get() 函数获取用户输入
            pressed_key = key.get()
            
            # 处理按键
            if pressed_key == "up":
                current_index = (current_index - 1) % len(menu_items)
            elif pressed_key == "down":
                current_index = (current_index + 1) % len(menu_items)
            elif pressed_key == "enter":
                selected = menu_items[current_index]
                if selected.strip():  # 只返回非空菜单项
                    print("处理中……")
                    
                    # 将中文选项映射回英文标识符
                    option_map = {
                        "确认创建": "OK",
                        "重新命名": "remake",
                        "编辑设置": "edit",
                        "导入世界": "import",
                        "返回": "back"
                    }
                    
                    selected_en = option_map.get(selected, selected)
                    
                    if selected_en == "OK":
                        # 创建新世界
                        world_id = world_manager.create_world(nwn)
                        return world_id
                    else:
                        return selected_en
            elif pressed_key == "esc":
                return "back"
                
        except KeyboardInterrupt:
            print("\n程序已退出")
            return "back"
        except Exception as e:
            print(f"错误: {e}")
            continue

def memu_edit_world_name(current_name):
    """编辑世界名称菜单"""
    board.clear()
    board.set_title("编辑世界名称")
    board.add_line("当前名称:", current_name)
    board.add_line("", "")
    board.add_line("请输入新的世界名称", "")
    board.add_line("按回车确认，ESC取消", "")
    board.display()
    
    new_name = input("> ")
    
    if new_name.strip():
        return new_name
    else:
        return current_name