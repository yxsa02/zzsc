# lib/memu/game_menu.py
from .common import board, need_redraw, _calculate_play_time
from .. import key
from .world import memu_confirm_exit

def memu_game_main(world_data, inventory):
    """游戏内主菜单显示 - 只负责显示和获取输入，不处理逻辑"""
    menu_items = [
        "探索区域", "原地休息", "查看/使用物品", "制作物品", "查看任务", "查看世界设置", "保存并返回主菜单"
    ]
    current_index = 0
    global need_redraw
    
    while True:
        try:
            # 清除并渲染菜单
            board.clear()
            if need_redraw:
                need_redraw = False

            # 显示玩家核心数据
            player = world_data["player"]
            world_state = world_data["world_state"]
            board.add_line(f" 生存第 {player['day']} 天 ", f"游戏时长: {_calculate_play_time(world_data)}")
            board.add_line(f"健康: {round(player['health'],1)}/100 | 饥饿: {round(player['hunger'],1)}/100", "")
            board.add_line(f"口渴: {round(player['thirst'],1)}/100 | 精力: {round(player['energy'],1)}/100", "")
            board.add_line(f"位置: {player['location']} | 已发现地点: {len(world_state['discovered_locations'])}", "")
            board.add_line(f"负重: {round(inventory.get_total_weight(),1)}/{inventory.capacity} | 物品数: {len(inventory.items)}", "")
            
            # 分割线
            board.add_line("=" * board.terminal_width, "")
            
            # 显示操作菜单
            for i, item in enumerate(menu_items):
                prefix = "▶ " if i == current_index else "  "
                board.add_line("", f"{prefix}{i+1}. {item}")
            
            # 操作提示
            board.add_line("使用 ↑↓ 选择，Enter 确认，ESC 快速返回主菜单", "")
            board.display()

            # 处理按键输入
            pressed_key = key.get()
            if pressed_key == "up":
                current_index = (current_index - 1) % len(menu_items)
            elif pressed_key == "down":
                current_index = (current_index + 1) % len(menu_items)
            elif pressed_key == "enter":
                # 返回操作标识符
                action_map = {
                    0: "explore",
                    1: "rest",
                    2: "inventory",
                    3: "craft",
                    4: "quests",
                    5: "settings",
                    6: "save_and_exit"
                }
                return action_map[current_index]
            elif pressed_key == "esc":
                # ESC 二次确认退出
                if memu_confirm_exit():
                    return "save_and_exit"

        except KeyboardInterrupt:
            return "save_and_exit"
        except Exception as e:
            print(f"游戏菜单错误: {e}")
            key.get()
            continue

def memu_show_explore_results(results, energy_remaining):
    """显示探索结果"""
    board.clear()
    board.add_line("探索结果", "")
    for result in results:
        board.add_line(result, "")
    board.add_line("", f"精力剩余: {round(energy_remaining,1)}/100")
    board.add_line("", "按任意键返回...")
    board.display()
    key.get()

def memu_show_rest_results(energy, hunger, thirst, penalty=""):
    """显示休息结果"""
    board.clear()
    board.add_line("休息结束！", "")
    board.add_line(f"精力: {round(energy,1)}/100", "")
    board.add_line(f"饥饿: {round(hunger,1)}/100 | 口渴: {round(thirst,1)}/100 {penalty}", "")
    board.add_line("", "按任意键返回...")
    board.display()
    key.get()

def memu_show_inventory(item_list):
    """显示库存并返回选中的物品索引"""
    current_item_idx = 0
    global need_redraw
    
    while True:
        try:
            # 渲染物品界面
            board.clear()
            if need_redraw:
                need_redraw = False

            # 左栏：物品列表
            board.add_line("=== 物品查看与使用 ===", f"当前选中: {item_list[current_item_idx].name}")
            board.add_line("\n【物品列表】（↑↓ 选择，Enter 使用，ESC 返回）", "")
            for idx, item in enumerate(item_list):
                prefix = "▶ " if idx == current_item_idx else "  "
                durability = f"（{item.durability}/{item.max_durability}）" if item.durability != item.max_durability else ""
                board.add_line(f"{prefix}{idx+1}. {item.name} x{item.quantity} {durability}", "")
            
            # 右栏：当前选中物品详情
            selected_item = item_list[current_item_idx]
            board.add_line("\n【物品详情】", "")
            board.add_line("", f"ID: {selected_item.id}")
            board.add_line("", f"类别: {selected_item.category.upper()}")
            board.add_line("", f"重量: {selected_item.weight}")
            board.add_line("", f"价值: {selected_item.value}")
            # 类别特定属性
            if selected_item.category == "food":
                board.add_line("", f"饥饿缓解: {selected_item.nutrition}")
            elif selected_item.category == "water":
                board.add_line("", f"口渴缓解: {selected_item.hydration}")
            elif selected_item.category == "medical":
                board.add_line("", f"健康恢复: {selected_item.health_effect}")
            elif selected_item.category in ["tools", "weapons"]:
                board.add_line("", f"伤害: {selected_item.damage}")
            board.add_line("", f"描述: {selected_item.description[:30]}...")

            board.display()

            # 处理按键输入
            pressed_key = key.get()
            if pressed_key == "up":
                current_item_idx = (current_item_idx - 1) % len(item_list)
            elif pressed_key == "down":
                current_item_idx = (current_item_idx + 1) % len(item_list)
            elif pressed_key == "enter":
                return current_item_idx  # 返回选中的物品索引
            elif pressed_key == "esc":
                return None  # 返回None表示取消

        except Exception as e:
            print(f"物品菜单错误: {e}")
            key.get()
            return None

def memu_show_item_use_result(message, health, hunger, thirst):
    """显示物品使用结果"""
    board.clear()
    board.add_line("物品使用结果", message)
    board.add_line("", f"当前健康: {round(health,1)}/100")
    board.add_line("", f"饥饿: {round(hunger,1)}/100")
    board.add_line("", f"口渴: {round(thirst,1)}/100")
    board.add_line("", "按任意键返回...")
    board.display()
    key.get()

def memu_show_crafting(craftable_items, item_manager, inventory):
    """显示制作菜单并返回选中的配方索引"""
    current_index = 0
    global need_redraw
    
    while True:
        try:
            # 渲染制作菜单
            board.clear()
            if need_redraw:
                need_redraw = False

            board.add_line("=== 物品制作 ===", "")
            # 显示可制作物品详情
            for idx, (recipe_id, recipe) in enumerate(craftable_items):
                board.add_line(f"\n{idx+1}. {recipe['name']}", f"配方ID: {recipe_id}")
                # 所需材料
                board.add_line("  所需材料：", "")
                for req_id, req_qty in recipe["requirements"].items():
                    req_data = item_manager.get_item(req_id)
                    current_qty = inventory.items[req_id].quantity if req_id in inventory.items else 0
                    board.add_line(f"    - {req_data['name']}: {current_qty}/{req_qty}", "")
                # 制作结果
                board.add_line("  制作结果：", "")
                for res_id, res_qty in recipe["results"].items():
                    res_data = item_manager.get_item(res_id)
                    board.add_line(f"    - {res_data['name']} x{res_qty}", "")
            
            # 操作提示
            board.add_line("\n操作提示", "")
            board.add_line("", "1. 输入编号制作物品")
            board.add_line("", "2. 按 ESC 返回上一级")
            board.display()
            print("请输入制作物品的编号（1-" + str(len(craftable_items)) + "）：", end="")

            # 处理输入
            input_str = ""
            while True:
                pressed_key = key.get()
                if pressed_key == "enter":
                    print()
                    if input_str.strip().isdigit():
                        idx = int(input_str.strip()) - 1
                        if 0 <= idx < len(craftable_items):
                            return idx  # 返回选中的配方索引
                        else:
                            print("无效编号，按任意键重新输入...", end="")
                            key.get()
                    else:
                        print("请输入有效数字，按任意键重新输入...", end="")
                        key.get()
                    break
                elif pressed_key == "esc":
                    print()
                    return None  # 返回None表示取消
                elif pressed_key.isdigit():
                    input_str += pressed_key
                    print(pressed_key, end="")

        except Exception as e:
            print(f"制作菜单错误: {e}")
            key.get()
            return None

def memu_show_craft_result(message):
    """显示制作结果"""
    board.clear()
    board.add_line("制作结果", message)
    board.add_line("", "按任意键返回...")
    board.display()
    key.get()

def memu_show_quests(active_quests, completed_quests):
    """显示任务列表"""
    board.clear()
    board.add_line("=== 任务列表 ===", f"总计: {len(active_quests)+len(completed_quests)}")
    # 活跃任务
    board.add_line("\n【活跃任务】", f"数量: {len(active_quests)}")
    for idx, quest in enumerate(active_quests, 1):
        board.add_line(f"  {idx}. {quest}", "状态: 进行中")
    if not active_quests:
        board.add_line("  暂无活跃任务", "")
    # 已完成任务
    board.add_line("\n【已完成任务】", f"数量: {len(completed_quests)}")
    for idx, quest in enumerate(completed_quests, 1):
        board.add_line(f"  {idx}. {quest}", "状态: 已完成")
    if not completed_quests:
        board.add_line("  暂无已完成任务", "")
    
    board.add_line("\n按任意键返回...", "")
    board.display()
    key.get()

def memu_show_new_day(day):
    """显示新的一天开始"""
    board.clear()
    board.add_line("新的一天开始了!", f"第 {day} 天")
    board.add_line("", "按任意键继续...")
    board.display()
    key.get()

def memu_show_game_over(days_survived):
    """显示游戏结束画面"""
    board.clear()
    board.add_line("游戏结束", "你的健康值降为零...")
    board.add_line("", "你没能在这个末日世界中生存下来")
    board.add_line("", "")
    board.add_line("生存天数:", f"{days_survived}")
    board.add_line("", "")
    board.add_line("按任意键返回主菜单...", "")
    board.display()
    key.get()

def memu_show_message(title, message):
    """显示通用消息"""
    board.clear()
    board.add_line(title, message)
    board.add_line("", "按任意键返回...")
    board.display()
    key.get()