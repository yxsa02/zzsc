import time
import sys

class ConsoleOutputDemo:
    def __init__(self):
        self.messages = [
            "欢迎来到Python控制台输出示例",
            "这里展示了多种输出方式",
            "包括基本输出、动态效果和格式控制"
        ]
    
    def print_basic_output(self):
        """基本输出方法"""
        print("=" * 50)
        print("1. 基本输出方法")
        print("=" * 50)
        
        # 普通输出
        print("这是一个简单的打印输出")
        
        # 输出变量
        name = "Python开发者"
        age = 30
        print("姓名:", name, "年龄:", age)
        
        # 格式化输出
        print(f"格式化输出: {name}今年{age}岁")
        print("字符串格式化: {}今年{}岁".format(name, age))
        
        # 输出特殊字符
        print("特殊字符: \\ \' \" \n换行符\t制表符")
        
    def print_dynamic_output(self):
        """动态输出效果"""
        print("\n" + "=" * 50)
        print("2. 动态输出效果")
        print("=" * 50)
        
        # 进度条模拟
        print("进度条模拟:")
        for i in range(21):
            progress = i * 5
            bar = "[" + "=" * i + " " * (20 - i) + "]"
            print(f"\r{bar} {progress}%", end="", flush=True)
            time.sleep(0.1)
        print("\n完成!")
        
        # 逐字输出
        print("\n逐字输出效果:")
        text = "Python控制台输出可以创建动态效果"
        for char in text:
            print(char, end="", flush=True)
            time.sleep(0.05)
        print()
        
    def print_formatting(self):
        """输出格式控制"""
        print("\n" + "=" * 50)
        print("3. 输出格式控制")
        print("=" * 50)
        
        # 对齐输出
        data = [
            ("Alice", 95, "A"),
            ("Bob", 82, "B"),
            ("Charlie", 78, "C"),
            ("David", 92, "A")
        ]
        
        print("{:<10} {:<5} {:<5}".format("姓名", "分数", "等级"))
        print("-" * 25)
        for name, score, grade in data:
            print("{:<10} {:<5} {:<5}".format(name, score, grade))
        
     
        
    def run_demo(self):
        """运行所有演示"""
        for msg in self.messages:
            print(f">>> {msg}")
            time.sleep(0.5)
            
        time.sleep(1)
        self.print_basic_output()
        time.sleep(1)
        self.print_dynamic_output()
        time.sleep(1)
        self.print_formatting()
        
        # 结束消息
        print("\n" + "=" * 50)
        print("感谢查看Python控制台输出示例!")
        print("=" * 50)

# 创建实例并运行演示
if __name__ == "__main__":
    demo = ConsoleOutputDemo()
    demo.run_demo()