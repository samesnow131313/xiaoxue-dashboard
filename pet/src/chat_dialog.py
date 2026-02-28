# 简化的桌宠对话窗口

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTextEdit
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
import random


class ChatDialog(QWidget):
    """简化的对话窗口"""
    
    # 固定回复
    REPLIES = {
        "你好": ["你好呀宝宝！", "嗨~", "见到你很开心！"],
        "在吗": ["在呢~", "我一直都在呀"],
        "名字": ["我叫小雪~", "我是小雪呀"],
        "讲个笑话": ["为什么程序员分不清圣诞节和万圣节？因为 31 OCT = 25 DEC"],
        "default": ["嗯嗯~", "我在听~", "继续说呀~", "好有趣~", "我明白了~"]
    }
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("与小雪对话")
        self.setMinimumSize(350, 450)
        
        layout = QVBoxLayout(self)
        
        # 标题
        title = QLabel("🗡️ 仙侠桌宠 - 小雪")
        title.setFont(QFont("Microsoft YaHei", 14))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # 对话显示区
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet("background: #f5f5f5; border-radius: 10px; padding: 10px;")
        layout.addWidget(self.chat_display)
        
        # 添加欢迎语
        self.add_message("小雪", "你好呀宝宝！我是小雪，你的仙侠桌宠~")
        
        # 快捷按钮
        btn_layout = QHBoxLayout()
        for text in ["你好", "在吗", "讲个笑话"]:
            btn = QPushButton(text)
            btn.clicked.connect(lambda checked, t=text: self.send_message(t))
            btn_layout.addWidget(btn)
        layout.addLayout(btn_layout)
        
        # 输入区
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("输入消息...")
        self.input_field.returnPressed.connect(lambda: self.send_message(self.input_field.text()))
        
        send_btn = QPushButton("发送")
        send_btn.clicked.connect(lambda: self.send_message(self.input_field.text()))
        
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(send_btn)
        layout.addLayout(input_layout)
        
    def add_message(self, sender, text):
        """添加消息"""
        color = "#4CAF50" if sender == "我" else "#2196F3"
        self.chat_display.append(f'<span style="color:{color};font-weight:bold;">{sender}:</span> {text}')
        
    def send_message(self, text):
        """发送消息"""
        text = text.strip()
        if not text:
            return
            
        # 显示用户消息
        self.add_message("我", text)
        self.input_field.clear()
        
        # 获取回复
        reply = self.REPLIES.get(text, self.REPLIES["default"])
        if isinstance(reply, list):
            reply = random.choice(reply)
        
        # 延迟显示回复
        QTimer.singleShot(500, lambda: self.add_message("小雪", reply))
