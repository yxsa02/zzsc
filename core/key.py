# key.py
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
        
def get():
    """
    等待用户按下按键并返回按键名称
    返回常见的按键名称，如 'up', 'down', 'enter', 'esc', 'a', '1' 等
    """
    key = getch()
    
    # 处理特殊按键
    if key == '\x1b':  # ESC字符
        # 检查是否是转义序列的一部分
        next_char = getch()
        if next_char == '[':
            # 处理方向键和功能键
            direction = getch()
            if direction == 'A':
                return 'up'
            elif direction == 'B':
                return 'down'
            elif direction == 'C':
                return 'right'
            elif direction == 'D':
                return 'left'
            elif direction == 'H':
                return 'home'
            elif direction == 'F':
                return 'end'
            elif direction == '1' or direction == '2' or direction == '3' or direction == '4' or direction == '5':
                # 处理功能键 F1-F5
                next_next_char = getch()
                if next_next_char == '~':
                    if direction == '1':
                        return 'f1'
                    elif direction == '2':
                        return 'f2'
                    elif direction == '3':
                        return 'f3'
                    elif direction == '4':
                        return 'f4'
                    elif direction == '5':
                        return 'f5'
        # 如果不是转义序列，返回 ESC
        return 'esc'
    
    # 处理其他特殊按键
    elif key == '\r' or key == '\n':
        return 'enter'
    elif key == '\t':
        return 'tab'
    elif key == '\x7f':  # 退格键
        return 'backspace'
    elif key == ' ':
        return 'space'
    
    # 处理控制键 (Ctrl+字母)
    elif key in ['\x01', '\x02', '\x03', '\x04', '\x05', '\x06', '\x07', 
                 '\x08', '\x09', '\x0a', '\x0b', '\x0c', '\x0d', '\x0e', 
                 '\x0f', '\x10', '\x11', '\x12', '\x13', '\x14', '\x15', 
                 '\x16', '\x17', '\x18', '\x19', '\x1a', '\x1b', '\x1c', 
                 '\x1d', '\x1e', '\x1f']:
        # 将控制字符转换为可读格式 (Ctrl+A -> Ctrl+Z)
        ctrl_char = chr(ord(key) + 64)
        return f'ctrl+{ctrl_char.lower()}'
    
    # 处理普通按键
    else:
        # 如果是可打印字符，直接返回
        if key.isprintable():
            return key.lower() if key.isalpha() else key
        # 对于不可打印字符，返回其十六进制表示
        return f'0x{ord(key):02x}'