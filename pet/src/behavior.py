# 桌宠行为AI - 简化版（3动作）
# idle常驻, click点击触发, happy无操作2秒后循环播放

from PyQt6.QtCore import QObject, pyqtSignal, QTimer
from enum import Enum, auto


class PetState(Enum):
    """状态枚举"""
    IDLE = auto()      # 待机 - 常驻默认
    CLICK = auto()     # 被点击 - 点击/拖动触发
    HAPPY = auto()     # 开心 - 2秒无操作自动循环


class BehaviorAI(QObject):
    """行为AI - 简化版"""
    state_changed = pyqtSignal(PetState)  # 状态变化信号
    
    def __init__(self):
        super().__init__()
        
        self.current_state = PetState.IDLE
        
        # 空闲检测定时器（2秒无操作 -> happy）
        self.idle_timer = QTimer()
        self.idle_timer.timeout.connect(self._on_idle_timeout)
        self.idle_timer.setInterval(2000)  # 2秒
        
        # 点击恢复定时器
        self.click_timer = QTimer()
        self.click_timer.setSingleShot(True)
        self.click_timer.timeout.connect(self._return_to_idle)
        
        # 状态标志
        self.is_interacting = False  # 是否正在交互中
        
    def _on_idle_timeout(self):
        """空闲超时 - 切换到happy循环"""
        if not self.is_interacting and self.current_state != PetState.HAPPY:
            self.set_state(PetState.HAPPY)
            # happy循环播放，不自动切回idle
            
    def _return_to_idle(self):
        """返回待机状态"""
        self.is_interacting = False
        self.set_state(PetState.IDLE)
        self.idle_timer.start()  # 重新开始空闲计时
        
    def set_state(self, state: PetState):
        """设置状态"""
        if state == self.current_state:
            return
            
        self.current_state = state
        self.state_changed.emit(state)
        
    def on_click(self):
        """被点击"""
        self.is_interacting = True
        self.idle_timer.stop()
        self.set_state(PetState.CLICK)
        # 800ms后恢复idle
        self.click_timer.start(800)
        
    def on_drag_start(self):
        """开始拖动"""
        self.is_interacting = True
        self.idle_timer.stop()
        self.set_state(PetState.CLICK)
        
    def on_drag_end(self):
        """结束拖动"""
        self.click_timer.start(500)  # 500ms后恢复
        
    def on_interaction_end(self):
        """交互结束，重新开始空闲计时"""
        self.is_interacting = False
        self.set_state(PetState.IDLE)
        self.idle_timer.start()
        
    def get_state_name(self) -> str:
        """获取当前状态名称"""
        return self.current_state.name.lower()
        
    def start(self):
        """启动AI"""
        self.set_state(PetState.IDLE)
        self.idle_timer.start()
        
    def stop(self):
        """停止AI"""
        self.idle_timer.stop()
        self.click_timer.stop()
