# 桌宠动画管理系统
# 处理帧序列、过渡、混合动画

from PyQt6.QtCore import QObject, pyqtSignal, QTimer
from PyQt6.QtGui import QPixmap
from typing import List, Dict, Optional
import os


class AnimationFrame:
    """单帧数据"""
    def __init__(self, pixmap: QPixmap, duration: int = 150):
        self.pixmap = pixmap
        self.duration = duration  # 毫秒
        

class AnimationState:
    """动画状态（一个动作的完整帧序列）"""
    def __init__(self, name: str, frames: List[AnimationFrame], loop: bool = True):
        self.name = name
        self.frames = frames
        self.loop = loop
        self.total_duration = sum(f.duration for f in frames)
        

class AnimationManager(QObject):
    """动画管理器"""
    frame_changed = pyqtSignal(QPixmap)  # 帧更新信号
    state_finished = pyqtSignal(str)     # 状态播放完成信号
    
    def __init__(self):
        super().__init__()
        
        self.states: Dict[str, AnimationState] = {}
        self.current_state: Optional[AnimationState] = None
        self.current_frame_index = 0
        
        self.timer = QTimer()
        self.timer.timeout.connect(self._next_frame)
        
    def add_state(self, state: AnimationState):
        """添加动画状态"""
        self.states[state.name] = state
        
    def load_from_directory(self, state_name: str, directory: str, 
                           frame_duration: int = 150):
        """从目录加载帧序列"""
        frames = []
        
        if not os.path.exists(directory):
            return
            
        files = sorted([f for f in os.listdir(directory)
                       if f.endswith(('.png', '.webp', '.jpg', '.jpeg', '.gif'))])
        
        for filename in files:
            path = os.path.join(directory, filename)
            pixmap = QPixmap(path)
            if not pixmap.isNull():
                frames.append(AnimationFrame(pixmap, frame_duration))
                
        if frames:
            state = AnimationState(state_name, frames)
            self.add_state(state)
            
    def play(self, state_name: str, force_restart: bool = False):
        """播放指定状态"""
        if state_name not in self.states:
            return
            
        new_state = self.states[state_name]
        
        # 如果已经在播放且不是强制重启，继续
        if self.current_state == new_state and not force_restart:
            return
            
        self.current_state = new_state
        self.current_frame_index = 0
        
        if new_state.frames:
            self._emit_current_frame()
            self._start_timer()
            
    def _start_timer(self):
        """启动定时器"""
        if not self.current_state or not self.current_state.frames:
            return
            
        frame = self.current_state.frames[self.current_frame_index]
        self.timer.start(frame.duration)
        
    def _next_frame(self):
        """下一帧"""
        if not self.current_state:
            return
            
        self.current_frame_index += 1
        
        # 检查是否播放完成
        if self.current_frame_index >= len(self.current_state.frames):
            if self.current_state.loop:
                self.current_frame_index = 0
            else:
                self.state_finished.emit(self.current_state.name)
                return
                
        self._emit_current_frame()
        self._start_timer()
        
    def _emit_current_frame(self):
        """发送当前帧"""
        if self.current_state and self.current_frame_index < len(self.current_state.frames):
            frame = self.current_state.frames[self.current_frame_index]
            self.frame_changed.emit(frame.pixmap)
            
    def stop(self):
        """停止播放"""
        self.timer.stop()
        self.current_state = None
        self.current_frame_index = 0
        
    def get_current_pixmap(self) -> Optional[QPixmap]:
        """获取当前帧图像"""
        if (self.current_state and 
            self.current_frame_index < len(self.current_state.frames)):
            return self.current_state.frames[self.current_frame_index].pixmap
        return None
