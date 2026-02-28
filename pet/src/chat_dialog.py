# 桌宠对话窗口 - 连接本地 OpenClaw

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit,
    QPushButton, QLabel, QScrollArea, QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QColor, QPalette
import json
import uuid


class ChatMessage(QFrame):
    """单条消息气泡"""
    def __init__(self, text, is_user=True, parent=None):
        super().__init__(parent)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        
        # 消息标签
        self.label = QLabel(text)
        self.label.setWordWrap(True)
        self.label.setFont(QFont("Microsoft YaHei", 11))
        self.label.setStyleSheet(f"""
            QLabel {{
                background-color: {'#DCF8C6' if is_user else '#FFFFFF'};
                border-radius: 12px;
                padding: 10px 15px;
                color: #333;
            }}
        """)
        self.label.setMaximumWidth(350)
        
        if is_user:
            layout.addStretch()
            layout.addWidget(self.label)
        else:
            layout.addWidget(self.label)
            layout.addStretch()
            
        self.setStyleSheet("background: transparent;")


class ChatWorker(QThread):
    """后台通信线程"""
    response_ready = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, gateway_url, message, session_key=None):
        super().__init__()
        self.gateway_url = gateway_url
        self.message = message
        self.session_key = session_key or str(uuid.uuid4())
        
    def run(self):
        """发送消息到 OpenClaw"""
        try:
            import urllib.request
            import urllib.error
            
            data = json.dumps({
                "text": self.message,
                "sessionKey": self.session_key
            }).encode('utf-8')
            
            req = urllib.request.Request(
                f"{self.gateway_url}/api/chat",
                data=data,
                headers={
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                method='POST'
            )
            
            with urllib.request.urlopen(req, timeout=60) as response:
                result = json.loads(response.read().decode('utf-8'))
                self.response_ready.emit(result.get('text', '无回复'))
                
        except Exception as e:
            self.error_occurred.emit(str(e))


class ChatDialog(QWidget):
    """桌宠对话窗口"""
    
    def __init__(self, parent=None, gateway_url="http://127.0.0.1:18792"):
        super().__init__(parent)
        
        self.gateway_url = gateway_url
        self.session_key = str(uuid.uuid4())
        self.worker = None
        
        self.init_ui()
        self.add_system_message("你好呀！我是你的桌宠，有什么想聊的吗？")
        
    def init_ui(self):
        """初始化界面"""
        self.setWindowTitle("与桌宠对话")
        self.setMinimumSize(400, 500)
        self.setMaximumSize(450, 600)
        
        # 主布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # 标题栏
        title = QLabel("🗡️ 仙侠桌宠")
        title.setFont(QFont("Microsoft YaHei", 14, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #2E7D32; padding: 5px;")
        layout.addWidget(title)
        
        # 消息区域（滚动）
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                border: 1px solid #ddd;
                border-radius: 8px;
                background: #F5F5F5;
            }
        """)
        
        self.message_container = QWidget()
        self.message_layout = QVBoxLayout(self.message_container)
        self.message_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.message_layout.setSpacing(5)
        self.message_layout.addStretch()
        
        self.scroll_area.setWidget(self.message_container)
        layout.addWidget(self.scroll_area)
        
        # 输入区域
        input_layout = QHBoxLayout()
        
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("输入消息...")
        self.input_field.setFont(QFont("Microsoft YaHei", 11))
        self.input_field.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ddd;
                border-radius: 20px;
                padding: 8px 15px;
                background: white;
            }
        """)
        self.input_field.returnPressed.connect(self.send_message)
        
        self.send_btn = QPushButton("发送")
        self.send_btn.setFont(QFont("Microsoft YaHei", 10))
        self.send_btn.setStyleSheet("""
            QPushButton {
                background: #4CAF50;
                color: white;
                border: none;
                border-radius: 20px;
                padding: 8px 20px;
            }
            QPushButton:hover {
                background: #45a049;
            }
            QPushButton:disabled {
                background: #ccc;
            }
        """)
        self.send_btn.clicked.connect(self.send_message)
        
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.send_btn)
        layout.addLayout(input_layout)
        
        # 状态标签
        self.status_label = QLabel("就绪")
        self.status_label.setFont(QFont("Microsoft YaHei", 9))
        self.status_label.setStyleSheet("color: #666;")
        layout.addWidget(self.status_label)
        
        self.setStyleSheet("""
            QWidget {
                background: #FAFAFA;
            }
        """)
        
    def add_message(self, text, is_user=True):
        """添加消息到界面"""
        # 移除底部的 stretch
        item = self.message_layout.itemAt(self.message_layout.count() - 1)
        if item and item.spacerItem():
            self.message_layout.removeItem(item)
        
        # 添加消息
        msg = ChatMessage(text, is_user)
        self.message_layout.addWidget(msg)
        
        # 重新添加 stretch
        self.message_layout.addStretch()
        
        # 滚动到底部
        QTimer.singleShot(100, self.scroll_to_bottom)
        
    def add_system_message(self, text):
        """添加系统消息"""
        self.add_message(text, is_user=False)
        
    def scroll_to_bottom(self):
        """滚动到底部"""
        scrollbar = self.scroll_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
        
    def send_message(self):
        """发送消息"""
        text = self.input_field.text().strip()
        if not text:
            return
            
        # 显示用户消息
        self.add_message(text, is_user=True)
        self.input_field.clear()
        
        # 禁用发送按钮
        self.send_btn.setEnabled(False)
        self.status_label.setText("发送中...")
        
        # 后台发送
        self.worker = ChatWorker(self.gateway_url, text, self.session_key)
        self.worker.response_ready.connect(self.on_response)
        self.worker.error_occurred.connect(self.on_error)
        self.worker.finished.connect(self.on_finished)
        self.worker.start()
        
    def on_response(self, text):
        """收到回复"""
        self.add_system_message(text)
        
    def on_error(self, error):
        """发生错误"""
        self.add_system_message(f"[连接失败: {error}]")
        
    def on_finished(self):
        """完成"""
        self.send_btn.setEnabled(True)
        self.status_label.setText("就绪")
        self.worker = None
        
    def closeEvent(self, event):
        """关闭时清理"""
        if self.worker and self.worker.isRunning():
            self.worker.terminate()
            self.worker.wait()
        event.accept()
