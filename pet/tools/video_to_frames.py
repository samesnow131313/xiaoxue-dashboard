#!/usr/bin/env python3
"""
视频转序列帧工具
用于将AI生成的动画视频转换为桌宠用的帧序列
"""

import cv2
import os
import argparse
from pathlib import Path


def video_to_frames(
    video_path: str,
    output_dir: str,
    fps: float = None,
    max_frames: int = None,
    size: tuple = None,
    format: str = 'png'
):
    """
    将视频转换为帧序列
    
    Args:
        video_path: 视频文件路径
        output_dir: 输出目录
        fps: 提取帧率（None则提取所有帧）
        max_frames: 最大帧数限制
        size: 输出尺寸 (width, height)，None则保持原尺寸
        format: 输出格式 png/jpg/webp
    """
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 打开视频
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"无法打开视频: {video_path}")
    
    # 获取视频信息
    video_fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    print(f"视频信息:")
    print(f"  分辨率: {int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))}x{int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))}")
    print(f"  帧率: {video_fps:.2f} fps")
    print(f"  总帧数: {total_frames}")
    print(f"  时长: {total_frames/video_fps:.2f} 秒")
    
    # 计算提取间隔
    if fps is None:
        frame_interval = 1  # 提取所有帧
        target_frames = total_frames
    else:
        frame_interval = int(video_fps / fps)
        target_frames = int(total_frames / frame_interval)
    
    if max_frames and target_frames > max_frames:
        frame_interval = int(total_frames / max_frames)
        target_frames = max_frames
    
    print(f"\n提取设置:")
    print(f"  目标帧率: {fps or video_fps:.2f} fps")
    print(f"  提取间隔: 每 {frame_interval} 帧")
    print(f"  预计输出: {target_frames} 帧")
    print(f"  输出尺寸: {size or '保持原尺寸'}")
    print(f"  输出格式: {format}")
    print()
    
    # 提取帧
    frame_count = 0
    saved_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # 按间隔提取
        if frame_count % frame_interval == 0:
            # 调整尺寸
            if size:
                frame = cv2.resize(frame, size, interpolation=cv2.INTER_LANCZOS4)
            
            # 生成文件名 (frame_01.png, frame_02.png, ...)
            filename = f"frame_{saved_count+1:02d}.{format}"
            filepath = os.path.join(output_dir, filename)
            
            # 保存
            if format == 'jpg':
                cv2.imwrite(filepath, frame, [cv2.IMWRITE_JPEG_QUALITY, 95])
            elif format == 'webp':
                cv2.imwrite(filepath, frame, [cv2.IMWRITE_WEBP_QUALITY, 95])
            else:  # png
                cv2.imwrite(filepath, frame)
            
            saved_count += 1
            print(f"  保存: {filename}", end='\r')
            
            if max_frames and saved_count >= max_frames:
                break
        
        frame_count += 1
    
    cap.release()
    print(f"\n\n完成! 共保存 {saved_count} 帧到: {output_dir}")
    
    return saved_count


def batch_convert(config_file: str):
    """批量转换（从配置文件）"""
    import json
    
    with open(config_file, 'r', encoding='utf-8') as f:
        configs = json.load(f)
    
    for config in configs:
        print(f"\n{'='*50}")
        print(f"处理: {config['name']}")
        print('='*50)
        video_to_frames(**config['params'])


def main():
    parser = argparse.ArgumentParser(description='视频转序列帧工具')
    parser.add_argument('video', help='视频文件路径')
    parser.add_argument('-o', '--output', default='frames', help='输出目录')
    parser.add_argument('-f', '--fps', type=float, help='目标帧率')
    parser.add_argument('-m', '--max-frames', type=int, help='最大帧数')
    parser.add_argument('-s', '--size', help='输出尺寸 (如: 400x600)')
    parser.add_argument('--format', default='png', choices=['png', 'jpg', 'webp'])
    parser.add_argument('--batch', help='批量配置文件(JSON)')
    
    args = parser.parse_args()
    
    if args.batch:
        batch_convert(args.batch)
    else:
        size = None
        if args.size:
            w, h = map(int, args.size.split('x'))
            size = (w, h)
        
        video_to_frames(
            video_path=args.video,
            output_dir=args.output,
            fps=args.fps,
            max_frames=args.max_frames,
            size=size,
            format=args.format
        )


if __name__ == '__main__':
    main()
