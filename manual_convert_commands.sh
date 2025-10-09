#!/bin/bash
# 手动转换视频为GIF的命令

echo "🎬 手动视频转GIF命令"
echo "请将你的视频文件名替换为实际文件名"
echo ""

echo "1. 基本转换 (假设视频文件为 recording.mov):"
echo "ffmpeg -i recording.mov -filter_complex '[0:v]setpts=0.5*PTS,scale=800:-1:flags=lanczos,fps=15[v]' -map '[v]' -y demo.gif"
echo ""

echo "2. 如果文件太大，使用压缩版本:"
echo "ffmpeg -i recording.mov -filter_complex '[0:v]setpts=0.3*PTS,scale=600:-1:flags=lanczos,fps=12[v]' -map '[v]' -y demo.gif"
echo ""

echo "3. 超压缩版本 (适合大文件):"
echo "ffmpeg -i recording.mov -filter_complex '[0:v]setpts=0.2*PTS,scale=400:-1:flags=lanczos,fps=10[v]' -map '[v]' -y demo.gif"
echo ""

echo "参数说明:"
echo "- setpts=0.5*PTS: 2倍速"
echo "- setpts=0.3*PTS: 3.3倍速"
echo "- setpts=0.2*PTS: 5倍速"
echo "- scale=800:-1: 宽度800像素，高度自动"
echo "- fps=15: 每秒15帧"
echo ""

echo "使用方法:"
echo "1. 将你的视频文件放到当前目录"
echo "2. 将上面命令中的 'recording.mov' 替换为你的文件名"
echo "3. 在终端运行命令"