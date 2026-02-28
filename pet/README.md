# 仙侠桌宠 - 简化版（3动作 + 对话）

二次元古风仙侠少女桌宠，青绿汉服，双剑背负。

## 功能特性

### 动画动作
| 动作 | 触发方式 | 播放方式 |
|------|----------|----------|
| idle 待机 | 默认常驻 | 循环播放 |
| click 被点击 | 点击/拖动时 | 播放一次后回idle |
| happy 开心 | 2秒无操作自动 | 循环播放 |

### 对话功能
- **双击桌宠** - 打开对话窗口
- **右键菜单 → 对话** - 打开对话窗口
- 连接本地 OpenClaw 网关
- 气泡聊天界面

## 文件结构

```
pet/
├── assets/
│   ├── idle/          # 待机帧 (12帧)
│   ├── click/         # 点击帧 (6帧)
│   └── happy/         # 开心帧 (10帧)
├── src/
│   ├── main.py        # 主程序
│   ├── behavior.py    # 行为AI
│   ├── animation.py   # 动画管理
│   └── chat_dialog.py # 对话窗口
├── tools/
│   └── video_to_frames.py  # 视频转帧工具
└── config.py          # 配置
```

## 安装运行

```bash
cd pet/src
pip install PyQt6
python main.py
```

## 对话功能配置

对话窗口默认连接 `http://127.0.0.1:18792`

如需修改网关地址，编辑 `chat_dialog.py`：
```python
self.gateway_url = "http://你的网关地址:端口"
```

## 交互方式

| 操作 | 效果 |
|------|------|
| 左键点击 | 触发click动作 |
| 左键拖动 | 移动位置 |
| 双击 | 打开对话窗口 |
| 右键 | 菜单（大小、状态、对话、退出）|

## 视频转帧

```bash
python tools/video_to_frames.py video.mp4 -o assets/idle -m 12 -s 400x600
```
