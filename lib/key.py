import sys

try:
    # Windows
    import msvcrt
    def getch():
        return msvcrt.getch().decode('utf-8')
except ImportError:
    # Unix/Linux/Mac
    import tty
    import termios
    def getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
        
def dokey(key, current_index, menu_items):
    if key == '\x1b':  # ESC字符
        next_char = getch()
        if next_char == '[':
            direction = getch()
            if direction == 'A':  # 上箭头
                current_index = (current_index - 1) % len(menu_items)
                return current_index, False, False
            elif direction == 'B':  # 下箭头
                current_index = (current_index + 1) % len(menu_items)
                return current_index, False, False
        else:
            return current_index, True, False  # 退出
    elif key == '\r' or key == '\n':  # 回车键
        return current_index, False, True  # 不退出，但需要执行
    elif key.lower() == 'q':
        return current_index, True, False  # 退出
    else:
        return current_index, False, False  # 其他按键不做处理