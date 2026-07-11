import os, sys
import platform,signal
from wcwidth import wcswidth

class displayer:
    def __init__(self):
        os.system("cls" if platform.system() == "Windows" else "clear")
        self.x = 1
        self.y = 1
        self.getTsize()
    def print(self,t):
        sys.stdout.write(t)
        sys.stdout.flush()
    def moveC(self, x, y, text=""):
        """移动光标并可选写入文本"""
        self.x = x
        self.y = y
        sys.stdout.write(f"\033[{x};{y}H{text}")
        sys.stdout.flush()
    def getTsize(self):
        """获取终端大小（跨平台）"""
        try:
            # 尝试使用标准方法
            self.w, self.h = os.get_terminal_size()
            return self.w, self.h
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
                        self.w = right - left + 1
                        self.h = bottom - top + 1
                        return self.w, self.h
                else:
                    # Unix/Linux/Mac
                    self.h, self.w = os.popen('stty size 2>/dev/null').read().split()
                    return int(self.w), int(self.h)
            except:
                pass
    def makeScreen(self):
        a = "="+" "*(self.w-2)+"="
        self.print("="*self.w)
        self.print(a)
        self.print("="*self.w)
        for i in range(self.h-5):
            self.print(a)
        self.print("="*self.w)
    def printCenter(self,text):
        c = int((self.w-2-len(text))/2)
        self.print(" "*c+text+" "*(self.w-2-c-len(text)))
if __name__ == "__main__":
    d = displayer()
    #for i in range(25):
        #d.moveC(i,i)
    d.makeScreen()
    d.moveC(2,2)
    d.print("hello|的")
    b = "1234567890abcdefghijklmnopqrstuvwxyz"
    d.moveC(4,2)
    d.printCenter(b)
    d.moveC(5,2) 
    d.printCenter(b[:10])   
    d.moveC(d.h-1,1)
