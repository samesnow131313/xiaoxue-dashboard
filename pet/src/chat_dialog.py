# 桌宠对话窗口 - 固定回复模式
# 预设多组回复，根据关键词匹配

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QScrollArea, QFrame
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
import random


# ==================== 固定回复库 ====================
class ResponseLibrary:
    """桌宠回复库"""
    
    # 关键词 -> 回复列表
    KEYWORD_RESPONSES = {
        # 问候
        "你好": ["你好呀宝宝！", "嗨~", "你好呀，今天心情怎么样？", "见到你很开心！"],
        "嗨": ["嗨~", "你好呀！", "嗨嗨~"],
        "在吗": ["在呢在呢~", "我一直都在呀", "在的，宝宝找我什么事？"],
        
        # 名字相关
        "名字": ["我叫小雪，是你的专属桌宠~", "我是小雪呀，不记得了吗？"],
        "你是谁": ["我是小雪，你的仙侠桌宠~", "我是陪伴你的小雪呀~"],
        
        # 心情相关
        "开心": ["宝宝开心我也开心！", "太好啦，要保持好心情哦~", "开心就好，要一直开心下去！"],
        "难过": ["不要难过啦，有我在呢", "抱抱宝宝，会好起来的", "想开点，我陪你~"],
        "累": ["累了就休息一下吧", "辛苦啦，要不要我陪你说说话？", "累了就歇歇，别硬撑~"],
        "无聊": ["那我陪你聊天呀~", "无聊的话，双击我可以互动哦~", "要不做点有趣的事？"],
        
        # 功能相关
        "桌宠": ["就是我呀，可爱吧~", "桌宠就是我，我会一直陪着你的", "喜欢我的话多和我互动呀~"],
        "功能": ["我可以陪你聊天，还可以双击打开对话窗口哦~", "我会待机、点击反应、还有开心动作~"],
        "动画": ["我的动作都是AI生成的哦，有idle、click、happy三种~", "喜欢我的动作吗？都是精心设计的~"],
        
        # 时间相关
        "早上": ["早上好呀宝宝！", "早安，今天也要元气满满哦~", "早呀，新的一天开始啦~"],
        "晚上": ["晚上好~", "晚安宝宝，早点休息哦~", "夜深了，别熬夜太晚~"],
        "晚安": ["晚安宝宝，好梦~", "晚安，明天见~", "睡个好觉哦~"],
        
        # 互动
        "谢谢": ["不用谢呀~", "能帮到你我很开心~", "这是我应该做的~"],
        "喜欢": ["我也喜欢宝宝~", "被喜欢好开心~", "喜欢就多来看看我呀~"],
        "可爱": ["嘻嘻，谢谢夸奖~", "被你夸好开心~", "我也觉得自己很可爱~"],
        
        # 默认回复（无匹配时随机选择）
        "default": [
            "嗯嗯，我在听~",
            "真的吗？",
            "然后呢？",
            "好有趣呀~",
            "我明白了~",
            "这样啊~",
            "宝宝说得对~",
            "我也是这么想的~",
            "嗯哼~",
            "继续说呀，我在听~",
            "哇~",
            "原来如此~",
            "学到了学到了~",
            "哈哈~",
            "好呀好呀~",
            "没问题~",
            "交给我吧~",
            "我会一直陪着你的~",
            "有我在呢~",
            "别担心~",
        ]
    }
    
    # 特殊指令
    SPECIAL_COMMANDS = {
        "讲个笑话": ["为什么程序员总是分不清圣诞节和万圣节？因为 31 OCT = 25 DEC", 
                   "你知道为什么程序员喜欢黑暗吗？因为光明会让他们有bug", 
                   "一个程序员走进酒吧，举起双手说：'我要一杯啤酒。'酒保问：'一杯还是两杯？'程序员说：'一杯。'酒保给了他两杯。"],
        "随机": ["随机选择：是的！", "随机选择：再等等看~", "随机选择：听你的~", "随机选择：我觉得可以~"],
        "帮助": ["我可以陪你聊天，双击我可以互动，右键可以调整大小和状态~"],
    }
    
    @classmethod
    def get_response(cls, message: str) -> str:
        """根据消息获取回复"""
        message = message.lower().strip()
        
        # 检查特殊指令
        for cmd, responses in cls.SPECIAL_COMMANDS.items():
            if cmd in message:
                return random.choice(responses)
        
        # 检查关键词
        for keyword, responses in cls.KEYWORD_RESPONSES.items():
            if keyword != "default" and keyword in message:
                return random.choice(responses)
        
        # 默认回复
        return random.choice(cls.KEYWORD_RESPONSES["default"])


class ChatMessage(QFrame):
    """单条消息气泡"""
    def __init__(self, text, is_user=True, parent=None):
        super().__init__(parent)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        
        self.label = QLabel(text)
        self.label.setWordWrap(True)
        self.label.setFont(QFont("Microsoft YaHei", 11))
        self.label.setStyleSheet(f"""
            QLabel {{
                background-color: {'#DCF8C6' if is_user else '#E3F2FD'};
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


class ChatDialog(QWidget):
    """桌宠对话窗口 - 固定回复版"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.init_ui()
        self.add_system_message("🗡️ 你好呀宝宝！我是小雪，你的仙侠桌宠~\n\n可以和我聊聊天，或者问我一些问题哦~")
        
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
        title = QLabel("🗡️ 仙侠桌宠 - 小雪")
        title.setFont(QFont("Microsoft YaHei", 14, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #1976D2; padding: 5px;")
        layout.addWidget(title)
        
        # 消息区域
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
        
        # 快捷按钮
        quick_layout = QHBoxLayout()
        quick_replies = ["你好", "讲个笑话", "在干嘛", "谢谢"]
        for reply in quick_replies:
            btn = QPushButton(reply)
            btn.setStyleSheet("""
                QPushButton {
                    background: #E3F2FD;
                    border: none;
                    border-radius: 15px;
                    padding: 5px 12px;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background: #BBDEFB;
                }
            """)
            btn.clicked.connect(lambda checked, r=reply: self.quick_send(r))
            quick_layout.addWidget(btn)
        layout.addLayout(quick_layout)
        
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
                background: #1976D2;
                color: white;
                border: none;
                border-radius: 20px;
                padding: 8px 20px;
            }
            QPushButton:hover {
                background: #1565C0;
            }
        """)
        self.send_btn.clicked.connect(self.send_message)
        
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.send_btn)
        layout.addLayout(input_layout)
        
        self.setStyleSheet("""
            QWidget {
                background: #FAFAFA;
            }
        """)
        
    def add_message(self, text, is_user=True):
        """添加消息"""
        item = self.message_layout.itemAt(self.message_layout.count() - 1)
        if item and item.spacerItem():
            self.message_layout.removeItem(item)
        
        msg = ChatMessage(text, is_user)
        self.message_layout.addWidget(msg)
        
        self.message_layout.addStretch()
        QTimer.singleShot(100, self.scroll_to_bottom)
        
    def add_system_message(self, text):
        """添加系统消息"""
        self.add_message(text, is_user=False)
        
    def scroll_to_bottom(self):
        """滚动到底部"""
        scrollbar = self.scroll_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
        
    def quick_send(self, text):
        """快捷发送"""
        self.input_field.setText(text)
        self.send_message()
        
    def send_message(self):
        """发送消息"""
        text = self.input_field.text().strip()
        if not text:
            return
            
        # 显示用户消息
        self.add_message(text, is_user=True)
        self.input_field.clear()
        
        # 获取固定回复
        response = ResponseLibrary.get_response(text)
        
        # 模拟打字延迟
        QTimer.singleShot(random.randint(500, 1500), lambda: self.add_system_message(response))
        
    def closeEvent(self, event):
        """关闭"""
        event.accept()
