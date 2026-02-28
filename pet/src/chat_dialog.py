# Simple Chat Dialog for Desktop Pet

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTextEdit
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
import random


class ChatDialog(QWidget):
    """Simple chat dialog"""
    
    # Fixed replies
    REPLIES = {
        "hello": ["Hello!", "Hi~", "Nice to see you!"],
        "there": ["I'm here~", "Always here for you"],
        "name": ["I'm XiaoXue~", "Call me XiaoXue"],
        "joke": ["Why do programmers confuse Christmas and Halloween? Because 31 OCT = 25 DEC"],
        "default": ["Hmm~", "I'm listening~", "Go on~", "Interesting~", "I see~"]
    }
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Chat with XiaoXue")
        self.setMinimumSize(350, 450)
        
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("XianXia Pet - XiaoXue")
        title.setFont(QFont("Microsoft YaHei", 14))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Chat display
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet("background: #f5f5f5; border-radius: 10px; padding: 10px;")
        layout.addWidget(self.chat_display)
        
        # Welcome message
        self.add_message("XiaoXue", "Hello! I'm XiaoXue, your desktop pet~")
        
        # Quick buttons
        btn_layout = QHBoxLayout()
        for text in ["hello", "there", "joke"]:
            btn = QPushButton(text)
            btn.clicked.connect(lambda checked, t=text: self.send_message(t))
            btn_layout.addWidget(btn)
        layout.addLayout(btn_layout)
        
        # Input area
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type message...")
        self.input_field.returnPressed.connect(lambda: self.send_message(self.input_field.text()))
        
        send_btn = QPushButton("Send")
        send_btn.clicked.connect(lambda: self.send_message(self.input_field.text()))
        
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(send_btn)
        layout.addLayout(input_layout)
        
    def add_message(self, sender, text):
        """Add message"""
        color = "#4CAF50" if sender == "Me" else "#2196F3"
        self.chat_display.append(f'{sender}: {text}')
        
    def send_message(self, text):
        """Send message"""
        text = text.strip().lower()
        if not text:
            return
            
        # Show user message
        self.add_message("Me", text)
        self.input_field.clear()
        
        # Get reply
        reply = self.REPLIES.get(text, self.REPLIES["default"])
        if isinstance(reply, list):
            reply = random.choice(reply)
        
        # Delayed reply
        QTimer.singleShot(500, lambda: self.add_message("XiaoXue", reply))
