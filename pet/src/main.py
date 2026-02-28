# 桌宠项目 - 仙侠少女（简化版3动作）
# idle常驻, click点击触发, happy无操作2秒后循环
# 双击打开对话窗口

from PyQt6.QtWidgets import QApplication, QWidget, QSystemTrayIcon, QMenu, QLabel
from PyQt6.QtCore import Qt, QTimer, QPoint
from PyQt6.QtGui import QPixmap, QIcon, QAction, QPainter, QColor, QFont
import sys
import os

# 导入行为AI和对话窗口
from behavior import BehaviorAI, PetState
from chat_dialog import ChatDialog


class DesktopPet(QWidget):
    def __init__(self):
        super().__init__()
        
        # 基础尺寸 (2:3比例)
        self.base_width = 200
        self.base_height = 300
        self.scale = 1.0
        
        # 状态
        self.state = 'idle'
        self.frame_index = 0
        self.frames = {}
        self.dragging = False
        self.drag_position = None
        
        # 行为AI
        self.behavior = BehaviorAI()
        self.behavior.state_changed.connect(self.on_state_changed)
        
        # 对话窗口
        self.chat_dialog = None
        
        # 动画定时器
        self.anim_timer = QTimer()
        self.anim_timer.timeout.connect(self.update_frame)
        self.anim_timer.start(150)
        
        self.init_ui()
        self.load_frames()
        self.behavior.start()  # 启动AI
        
    def init_ui(self):
        """初始化窗口"""
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # 显示区域
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.update_size()
        
        # 系统托盘
        self.setup_tray()
        
        # 初始位置（屏幕右下角）
        screen = QApplication.primaryScreen().geometry()
        self.move(screen.width() - self.width() - 50, 
                  screen.height() - self.height() - 100)
        
    def setup_tray(self):
        """系统托盘菜单"""
        self.tray = QSystemTrayIcon(self)
        self.tray.setToolTip("仙侠桌宠")
        
        menu = QMenu()
        
        # 缩放选项
        scale_menu = menu.addMenu("大小")
        for s in [0.5, 0.75, 1.0, 1.25, 1.5, 2.0]:
            action = QAction(f"{int(s*100)}%", self)
            action.triggered.connect(lambda checked, sc=s: self.set_scale(sc))
            scale_menu.addAction(action)
        
        menu.addSeparator()
        
        # 状态切换
        idle_action = QAction("待机", self)
        idle_action.triggered.connect(lambda: self.behavior.set_state(PetState.IDLE))
        menu.addAction(idle_action)
        
        happy_action = QAction("开心", self)
        happy_action.triggered.connect(lambda: self.behavior.set_state(PetState.HAPPY))
        menu.addAction(happy_action)
        
        menu.addSeparator()
        
        # 对话功能
        chat_action = QAction("对话", self)
        chat_action.triggered.connect(self.open_chat)
        menu.addAction(chat_action)
        
        menu.addSeparator()
        
        quit_action = QAction("退出", self)
        quit_action.triggered.connect(QApplication.quit)
        menu.addAction(quit_action)
        
        self.tray.setContextMenu(menu)
        self.tray.show()
        
    def load_frames(self):
        """加载动画帧 - 只加载3个动作"""
        states = ['idle', 'click', 'happy']
        base_path = os.path.join(os.path.dirname(__file__), '..', 'assets')
        
        print(f"加载资源路径: {base_path}")
        
        for state in states:
            self.frames[state] = []
            state_path = os.path.join(base_path, state)
            
            print(f"检查 {state} 路径: {state_path}")
            
            if os.path.exists(state_path):
                files = sorted([f for f in os.listdir(state_path) 
                              if f.endswith(('.png', '.webp', '.gif'))])
                print(f"  找到 {len(files)} 个文件")
                for f in files:
                    try:
                        pixmap = QPixmap(os.path.join(state_path, f))
                        if not pixmap.isNull():
                            self.frames[state].append(pixmap)
                            print(f"  加载成功: {f}")
                        else:
                            print(f"  加载失败: {f}")
                    except Exception as e:
                        print(f"  错误 {f}: {e}")
            else:
                print(f"  路径不存在: {state_path}")
            
            # 如果没有资源，使用占位
            if not self.frames[state]:
                print(f"  使用占位图")
                self.frames[state] = [self.create_placeholder(state)]
    
    def create_placeholder(self, text):
        """创建占位图"""
        pixmap = QPixmap(self.base_width, self.base_height)
        pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(pixmap)
        painter.setPen(QColor(100, 150, 200))
        painter.setFont(QFont("Microsoft YaHei", 12))
        painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, 
                        f"[{text}]\n待添加资源")
        painter.end()
        
        return pixmap
        
    def update_size(self):
        """更新窗口大小"""
        w = int(self.base_width * self.scale)
        h = int(self.base_height * self.scale)
        self.setFixedSize(w, h)
        self.label.setFixedSize(w, h)
        
    def set_scale(self, scale):
        """设置缩放比例"""
        self.scale = scale
        self.update_size()
        self.update_frame()
        
    def on_state_changed(self, state: PetState):
        """AI状态变化回调"""
        self.set_state(state.name.lower())
        
    def set_state(self, state: str):
        """切换状态"""
        if state in self.frames and state != self.state:
            self.state = state
            self.frame_index = 0
            self.update_frame()
            
    def update_frame(self):
        """更新动画帧"""
        frames = self.frames.get(self.state, [])
        if not frames:
            return
            
        # 获取当前帧
        pixmap = frames[self.frame_index % len(frames)]
        
        # click动作播放一次后自动回idle
        if self.state == 'click':
            self.frame_index += 1
            if self.frame_index >= len(frames):
                self.frame_index = 0
                self.behavior._return_to_idle()
                return
        else:
            # idle和happy循环播放
            self.frame_index = (self.frame_index + 1) % len(frames)
        
        # 缩放显示
        scaled = pixmap.scaled(
            self.label.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.label.setPixmap(scaled)
        
    # ========== 鼠标交互 ==========
    
    def mousePressEvent(self, event):
        """鼠标按下"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            self.behavior.on_click()
            event.accept()
            
    def mouseMoveEvent(self, event):
        """鼠标拖动"""
        if self.dragging:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()
            
    def mouseReleaseEvent(self, event):
        """鼠标释放"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False
            self.behavior.on_drag_end()
            event.accept()
            
    def mouseDoubleClickEvent(self, event):
        """双击打开对话窗口"""
        self.open_chat()
        event.accept()
        
    def open_chat(self):
        """打开对话窗口"""
        if self.chat_dialog is None or not self.chat_dialog.isVisible():
            self.chat_dialog = ChatDialog(self)
            # 显示在桌宠旁边
            pet_pos = self.pos()
            self.chat_dialog.move(pet_pos.x() - 420, pet_pos.y())
            self.chat_dialog.show()
        else:
            self.chat_dialog.raise_()
            self.chat_dialog.activateWindow()
        
    def contextMenuEvent(self, event):
        """右键菜单"""
        self.tray.contextMenu().popup(event.globalPos())


def main():
    import traceback
    try:
        app = QApplication(sys.argv)
        app.setQuitOnLastWindowClosed(False)
        
        pet = DesktopPet()
        pet.show()
        
        sys.exit(app.exec())
    except Exception as e:
        print(f"错误: {e}")
        traceback.print_exc()
        input("按回车键退出...")


if __name__ == '__main__':
    main()
