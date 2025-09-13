# lib/memu/world_menu.py
from .common import board, world_manager, need_redraw
from .. import key

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

def memu_confirm_exit():
    """退出确认菜单：防止误操作退出游戏"""
    menu_items = ["确认退出", "取消"]
    current_index = 0
    global need_redraw
    
    while True:
        try:
            board.clear()
            if need_redraw:
                need_redraw = False
            
            # 渲染确认界面
            board.add_line("提示", "确定要退出游戏吗？")
            board.add_line("", "")
            for i, item in enumerate(menu_items):
                prefix = ">" if i == current_index else " "
                board.add_line(f"{prefix}{item}", "")
            board.display()
            print("使用方向键选择，回车确认，ESC取消")
            
            # 处理按键
            pressed_key = key.get()
            if pressed_key == "up" or pressed_key == "down":
                current_index = (current_index + 1) % len(menu_items)
            elif pressed_key == "enter":
                return menu_items[current_index] == "确认退出"  # 返回布尔值：True=退出，False=取消
            elif pressed_key == "esc":
                return False  # ESC默认取消
        except Exception as e:
            print(f"退出确认菜单错误: {e}")
            time.sleep(1)
            return False

def memu_edit_difficulty(current_diff="normal"):
    """难度编辑菜单：修改新世界/现有世界的难度"""
    difficulty_options = [("简单", "easy"), ("普通", "normal"), ("困难", "hard")]
    current_index = 1  # 默认选中"普通"
    # 匹配当前难度的索引
    for i, (_, diff_code) in enumerate(difficulty_options):
        if diff_code == current_diff:
            current_index = i
            break
    
    global need_redraw
    while True:
        try:
            board.clear()
            if need_redraw:
                need_redraw = False
            
            # 渲染难度选择界面
            board.add_line("编辑游戏难度", f"当前难度: {difficulty_options[current_index][0]}")
            board.add_line("", "")
            for i, (diff_name, _) in enumerate(difficulty_options):
                prefix = ">" if i == current_index else " "
                board.add_line(f"{prefix}{i+1}. {diff_name}", "")
            board.add_line("", "")
            board.add_line("1-3选择难度，回车确认，ESC返回", "")
            board.display()
            
            # 处理按键
            pressed_key = key.get()
            if pressed_key == "up":
                current_index = (current_index - 1) % len(difficulty_options)
            elif pressed_key == "down":
                current_index = (current_index + 1) % len(difficulty_options)
            elif pressed_key in ["1", "2", "3"]:
                current_index = int(pressed_key) - 1
            elif pressed_key == "enter":
                return difficulty_options[current_index][1]  # 返回难度编码（easy/normal/hard）
            elif pressed_key == "esc":
                return current_diff  # 返回原难度，不修改
        except Exception as e:
            print(f"难度编辑菜单错误: {e}")
            time.sleep(1)
            return current_diff

def memu_world_settings(world_id):
    """世界设置菜单：修改已有世界的难度、自动保存等配置"""
    # 获取当前世界信息
    world_info = world_manager.get_world_info(world_id)
    if not world_info:
        board.clear()
        board.add_line("错误", "世界不存在")
        board.add_line("", "按回车返回")
        board.display()
        key.get()
        return
    
    # 加载当前世界数据
    world_data, _ = world_manager.load_world(world_id)
    if not world_data:
        board.clear()
        board.add_line("错误", "无法加载世界数据")
        board.add_line("", "按回车返回")
        board.display()
        key.get()
        return
    
    # 当前设置
    current_diff = world_data["game_settings"]["difficulty"]
    current_autosave = world_data["game_settings"]["autosave"]
    menu_items = ["修改难度", "切换自动保存", "返回"]
    current_index = 0
    global need_redraw
    
    while True:
        try:
            board.clear()
            if need_redraw:
                need_redraw = False
            
            # 渲染设置界面
            board.add_line(f"世界设置: {world_info['name']}", "")
            board.add_line(f"当前难度: {current_diff}", f"自动保存: {'开启' if current_autosave else '关闭'}")
            board.add_line("", "")
            for i, item in enumerate(menu_items):
                prefix = ">" if i == current_index else " "
                board.add_line(f"{prefix}{item}", "")
            board.display()
            print("使用方向键选择，回车确认，ESC返回")
            
            # 处理按键
            pressed_key = key.get()
            if pressed_key == "up":
                current_index = (current_index - 1) % len(menu_items)
            elif pressed_key == "down":
                current_index = (current_index + 1) % len(menu_items)
            elif pressed_key == "enter":
                selected = menu_items[current_index]
                if selected == "修改难度":
                    # 调用难度编辑菜单更新难度
                    new_diff = memu_edit_difficulty(current_diff)
                    if new_diff != current_diff:
                        world_data["game_settings"]["difficulty"] = new_diff
                        world_manager.save_world(world_data, _)  # 保存修改
                        current_diff = new_diff
                elif selected == "切换自动保存":
                    # 切换自动保存状态
                    current_autosave = not current_autosave
                    world_data["game_settings"]["autosave"] = current_autosave
                    world_manager.save_world(world_data, _)  # 保存修改
                elif selected == "返回":
                    return
            elif pressed_key == "esc":
                return
        except Exception as e:
            print(f"世界设置菜单错误: {e}")
            time.sleep(1)
            return

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