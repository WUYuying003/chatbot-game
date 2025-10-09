#!/usr/bin/env python3
"""
Video to GIF Converter with Speed Adjustment
将录制的游戏视频转换为10秒内的GIF
"""

import os
import sys
import subprocess

def check_ffmpeg():
    """检查ffmpeg是否安装"""
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def install_ffmpeg_instructions():
    """显示ffmpeg安装说明"""
    print("🔧 需要安装FFmpeg来处理视频转换")
    print("\n📥 安装方法:")
    print("macOS: brew install ffmpeg")
    print("Windows: 下载 https://ffmpeg.org/download.html")
    print("Ubuntu: sudo apt install ffmpeg")

def convert_video_to_gif(input_file, output_file="demo.gif", target_duration=10):
    """
    将视频转换为GIF并调整速度
    
    参数:
    - input_file: 输入视频文件路径
    - output_file: 输出GIF文件名
    - target_duration: 目标时长（秒）
    """
    
    if not os.path.exists(input_file):
        print(f"❌ 找不到文件: {input_file}")
        return False
    
    if not check_ffmpeg():
        install_ffmpeg_instructions()
        return False
    
    try:
        # 获取视频时长
        result = subprocess.run([
            'ffprobe', '-v', 'quiet', '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1', input_file
        ], capture_output=True, text=True, check=True)
        
        original_duration = float(result.stdout.strip())
        speed_factor = original_duration / target_duration
        
        print(f"📹 原始视频时长: {original_duration:.2f}秒")
        print(f"🎯 目标时长: {target_duration}秒")
        print(f"⚡ 加速倍数: {speed_factor:.2f}x")
        
        # 转换命令
        cmd = [
            'ffmpeg', '-i', input_file,
            '-filter_complex', 
            f'[0:v]setpts={1/speed_factor}*PTS,scale=800:-1:flags=lanczos,fps=15[v]',
            '-map', '[v]',
            '-y',  # 覆盖输出文件
            output_file
        ]
        
        print("🔄 开始转换...")
        subprocess.run(cmd, check=True)
        
        # 检查文件大小
        file_size = os.path.getsize(output_file) / 1024 / 1024  # MB
        print(f"✅ 转换完成!")
        print(f"📁 输出文件: {output_file}")
        print(f"📊 文件大小: {file_size:.2f} MB")
        
        if file_size > 10:
            print("⚠️  文件较大，建议进一步压缩")
            optimize_gif(output_file)
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 转换失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        return False

def optimize_gif(gif_file):
    """优化GIF文件大小"""
    optimized_file = gif_file.replace('.gif', '_optimized.gif')
    
    try:
        cmd = [
            'ffmpeg', '-i', gif_file,
            '-filter_complex',
            '[0:v]scale=600:-1:flags=lanczos,fps=12[v]',
            '-map', '[v]',
            '-y',
            optimized_file
        ]
        
        print("🔄 优化GIF文件大小...")
        subprocess.run(cmd, check=True)
        
        original_size = os.path.getsize(gif_file) / 1024 / 1024
        optimized_size = os.path.getsize(optimized_file) / 1024 / 1024
        
        print(f"📊 原始大小: {original_size:.2f} MB")
        print(f"📊 优化大小: {optimized_size:.2f} MB")
        print(f"💾 节省: {((original_size - optimized_size) / original_size * 100):.1f}%")
        
    except subprocess.CalledProcessError as e:
        print(f"⚠️  优化失败: {e}")

def main():
    """主函数"""
    print("🎬 视频转GIF工具")
    print("=" * 40)
    
    # 查找视频文件
    video_extensions = ['.mp4', '.mov', '.avi', '.mkv', '.webm']
    video_files = []
    
    for file in os.listdir('.'):
        if any(file.lower().endswith(ext) for ext in video_extensions):
            video_files.append(file)
    
    if not video_files:
        print("❌ 当前目录没有找到视频文件")
        print("请将录制的视频文件放在当前目录下")
        print(f"支持格式: {', '.join(video_extensions)}")
        return
    
    if len(video_files) == 1:
        input_file = video_files[0]
        print(f"📹 找到视频文件: {input_file}")
    else:
        print("📹 找到多个视频文件:")
        for i, file in enumerate(video_files, 1):
            print(f"  {i}. {file}")
        
        try:
            choice = int(input("请选择要转换的文件 (输入数字): ")) - 1
            input_file = video_files[choice]
        except (ValueError, IndexError):
            print("❌ 无效选择")
            return
    
    # 转换为GIF
    output_file = "demo.gif"
    success = convert_video_to_gif(input_file, output_file, target_duration=10)
    
    if success:
        print("\n🎉 转换成功!")
        print(f"📁 GIF文件已保存为: {output_file}")
        print("📋 现在可以将此文件放入作业目录:")
        print("   voice_controlled_bird_assignment/demo.gif")

if __name__ == "__main__":
    main()