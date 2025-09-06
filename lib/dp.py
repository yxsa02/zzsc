import os
import sys
import platform
from wcwidth import wcswidth

def get_terminal_size():
    """获取终端大小（跨平台）"""
    try:
        # 尝试使用标准方法
        columns, rows = os.get_terminal_size()
    except (AttributeError, OSError):
        try:
            # Windows 系统
            if platform.system() == "Windows":
                from ctypes import windll, create_string_buffer
                h = windll.kernel32.GetStdHandle(-12)
                csbi = create_string_buffer(22)
                res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)
                if res:
                    import struct
                    (_, _, _, _, _, left, top, right, bottom, _, _) = struct.unpack("hhhhHhhhhhh", csbi.raw)
                    columns = right - left + 1
                    rows = bottom - top + 1
                else:
                    columns, rows = 80, 24  # 默认值
            else:
                # Unix/Linux/Mac
                rows, columns = os.popen('stty size 2>/dev/null').read().split()
                columns, rows = int(columns), int(rows)
        except:
            # 如果所有方法都失败，使用默认值
            columns, rows = 80, 24
    
    return columns, rows

class AdaptiveDisplayBoard:
    def __init__(self, title="window", min_width=45, max_width=None):
        self.lines = []  # 存储 (left_text, right_text) 元组
        self.title = title
        self.min_width = min_width
        self.max_width = max_width
        self.left_ratio = 0.7  # 左侧区域占总宽度的比例
        self.right_ratio = 0.3  # 右侧区域占总宽度的比例
        
    def _get_display_width(self, text):
        """计算字符串的显示宽度"""
        width = 0
        for char in text:
            # 中文字符通常占用2个英文字符宽度
            if '\u4e00' <= char <= '\u9fff':
                width += 2
            else:
                width += 1
        return width
    
    def _truncate_text(self, text, max_width, ellipsis="…"):
        """截断文本并添加省略号"""
        if self._get_display_width(text) <= max_width:
            return text
            
        # 计算省略号的宽度
        ellipsis_width = self._get_display_width(ellipsis)
        max_content_width = max_width - ellipsis_width
        
        result = ""
        current_width = 0
        
        for char in text:
            char_width = 2 if '\u4e00' <= char <= '\u9fff' else 1
            if current_width + char_width > max_content_width:
                break
            result += char
            current_width += char_width
        
        return result + ellipsis
    
    def display(self):
        """显示内容，自适应终端大小"""
        # 获取终端大小
        columns, rows = get_terminal_size()
        
        # 确定显示板宽度
        if self.max_width:
            width = min(columns, self.max_width)
        else:
            width = columns
        
        width = max(width, self.min_width)  # 确保不小于最小宽度
        
        # 计算左右区域宽度
        left_width = int((width - 3) * self.left_ratio)  # -3 是为了边框和分隔符
        right_width = int((width - 3) * self.right_ratio)
        
        # 清屏
        os.system("cls" if platform.system() == "Windows" else "clear")
        
        # 显示标题
        title_width = self._get_display_width(self.title)
        title_padding = (width - title_width - 2) // 2
        left_pad = " " * title_padding
        right_pad = " " * (width - title_width - 2 - title_padding)
        print("=" * width)
        print(f"={left_pad}{self.title}{right_pad}=")
        print("=" * width)
        
        # 显示内容行
        for left_text, right_text in self.lines:
            # 处理文本溢出
            left_display = self._truncate_text(left_text, left_width)
            right_display = self._truncate_text(right_text, right_width)
            
            # 计算填充
            left_display_width = self._get_display_width(left_display)
            right_display_width = self._get_display_width(right_display)
            
            left_padding = left_width - left_display_width
            right_padding = right_width - right_display_width
            
            # 创建格式化字符串
            line = f"={left_display}{' ' * left_padding}={right_display}{' ' * right_padding}="
            print(line)
        
        # 显示底部边框
        print("=" * width)
    
    def add_line(self, left_text="", right_text=""):
        """添加一行内容"""
        self.lines.append((left_text, right_text))
    
    def clear(self):
        """清空内容"""
        self.lines = []
    
    def set_title(self, title):
        """设置标题"""
        self.title = title