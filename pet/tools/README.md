# 视频转序列帧工具使用说明

## 安装依赖

```bash
pip install opencv-python
```

## 基础用法

### 1. 提取所有帧
```bash
python video_to_frames.py input.mp4 -o output_folder
```

### 2. 指定帧率（如每秒8帧）
```bash
python video_to_frames.py input.mp4 -o output_folder -f 8
```

### 3. 限制最大帧数（如只取12帧）
```bash
python video_to_frames.py input.mp4 -o output_folder -m 12
```

### 4. 调整输出尺寸（2:3比例）
```bash
python video_to_frames.py input.mp4 -o output_folder -s 400x600
```

### 5. 指定格式
```bash
python video_to_frames.py input.mp4 -o output_folder --format webp
```

## 桌宠专用示例

### Idle 待机（12帧）
```bash
python video_to_frames.py idle_video.mp4 \
    -o ../assets/idle \
    -m 12 \
    -s 400x600 \
    --format png
```

### Walk 行走（8帧）
```bash
python video_to_frames.py walk_video.mp4 \
    -o ../assets/walk \
    -m 8 \
    -s 400x600 \
    --format png
```

### 批量处理

创建 `batch_config.json`:
```json
[
  {
    "name": "idle",
    "params": {
      "video_path": "videos/idle.mp4",
      "output_dir": "../assets/idle",
      "max_frames": 12,
      "size": [400, 600],
      "format": "png"
    }
  },
  {
    "name": "walk", 
    "params": {
      "video_path": "videos/walk.mp4",
      "output_dir": "../assets/walk",
      "max_frames": 8,
      "size": [400, 600],
      "format": "png"
    }
  }
]
```

运行:
```bash
python video_to_frames.py --batch batch_config.json
```

## 输出文件命名

自动命名为 `frame_01.png`, `frame_02.png`, ... 方便桌宠程序读取。
