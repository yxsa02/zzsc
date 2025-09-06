# memu.py
import os
import sys
from . import key
from .dp import AdaptiveDisplayBoard

# 创建自适应显示板实例
board = AdaptiveDisplayBoard("ZZSC", min_width=45)

def memu_start():
    menu_items = ["start", "人 ", "new", "setting", "exit"]
    mmb = ["hello", "lastplay:--", " ", " ", "chose your opt"]
    current_index = 0
    should_exit = False
    
    while not should_exit: 
        try:
            board.clear()
            
            # 添加菜单项
            for i, (ll, item) in enumerate(zip(mmb, menu_items)):
                prefix = ">" if i == current_index else " "
                board.add_line(ll, f"{prefix}{item}")
            
            board.display()
            print("使用方向键选择，回车确认，ESC退出")
            
            k = key.getch()
            current_index, should_exit, should_execute = key.dokey(k, current_index, menu_items)
            
            if should_execute:
                selected = menu_items[current_index]
                print("loading……")
                return selected
                
        except KeyboardInterrupt:
            print("\n程序已退出")
            break
        except Exception as e:
            print(f"错误: {e}")
            continue
            
def memu_newworld(nwn, nwm):
    menu_items = ["OK", "remake", "edit", "import", "back"]
    current_index = 0
    should_exit = False
    
    while not should_exit: 
        try:
            board.clear()
            mmb = ["New World", f"WorldName:{nwn}", " ", " ", "chose your opt"]
            
            # 添加菜单项
            for i, (ll, item) in enumerate(zip(mmb, menu_items)):
                prefix = ">" if i == current_index else " "
                board.add_line(ll, f"{prefix}{item}")
            
            board.display()
            print("使用方向键选择，回车确认，ESC退出")
            
            k = key.getch()
            current_index, should_exit, should_execute = key.dokey(k, current_index, menu_items)
            
            if should_execute:
                selected = menu_items[current_index]
                print("loading……")
                return selected
                
        except KeyboardInterrupt:
            print("\n程序已退出")
            break
        except Exception as e:
            print(f"错误: {e}")
            continue