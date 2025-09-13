# lib/memu/common.py
import os
import sys
import platform
import signal
import time
from datetime import datetime
from .. import key
from ..dp import AdaptiveDisplayBoard
from ..world import WorldManager

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

def _calculate_play_time(world_data):
    """计算游戏时长（从世界创建到当前，格式 HH:MM:SS）"""
    created_time = datetime.fromisoformat(world_data["system"]["created"])
    elapsed = datetime.now() - created_time
    total_seconds = elapsed.total_seconds()
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"