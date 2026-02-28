# 配置文件 - 简化版（3动作）

# 窗口设置
WINDOW = {
    'base_width': 200,      # 基础宽度
    'base_height': 300,     # 基础高度 (2:3比例)
    'min_scale': 0.5,       # 最小缩放
    'max_scale': 3.0,       # 最大缩放
    'default_scale': 1.0,   # 默认缩放
}

# 动画设置
ANIMATION = {
    'idle_frame_duration': 200,     # 待机组慢一些（飘逸感）
    'click_frame_duration': 100,    # 点击组快一些
    'happy_frame_duration': 150,    # 开心组正常
}

# 行为AI设置
BEHAVIOR = {
    'idle_to_happy_delay': 2000,  # 2秒无操作切换到happy（毫秒）
    'click_recovery_time': 800,   # 点击后恢复idle时间（毫秒）
}

# 资源路径 - 只保留3个动作
ASSETS = {
    'base_path': 'assets',
    'states': ['idle', 'click', 'happy']
}

# 动作帧数
FRAME_COUNTS = {
    'idle': 12,     # 循环播放
    'click': 6,     # 单次播放后回idle
    'happy': 10,    # 循环播放
}

# 动作说明
STATE_DESCRIPTION = {
    'idle': '待机 - 常驻默认状态，呼吸裙摆飘动',
    'click': '被点击 - 点击或拖动时触发，播放一次',
    'happy': '开心 - 2秒无操作自动播放，循环',
}
