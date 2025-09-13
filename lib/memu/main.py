# lib/memu/main_menu.py
from .common import board, world_manager, need_redraw
from .. import key

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
                    # 将中文选项映射回英文标识符
                    option_map = {
                        "继续游戏": "start",
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