import argparse
import cv2
import os
import imageio
import subprocess

from utils import get_datetime_str


def convert_gif_to_mp4(gif_file, output_file=None):
    # 打开GIF文件
    cap = cv2.VideoCapture(gif_file)
    
    # 获取GIF的帧速率和帧大小
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # 定义MP4编码器
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    
    # 创建VideoWriter对象
    out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # 将每一帧写入MP4文件
        out.write(frame)
    
    # 释放VideoCapture和VideoWriter
    cap.release()
    out.release()


def convert_mp4_to_gif(mp4_file, output_file=None):
    reader = imageio.get_reader(mp4_file)
    fps = reader.get_meta_data()['fps']
    print(f"{mp4_file} : fps = {fps}")
    # 创建 GIF 写入器
    writer = imageio.get_writer(output_file, mode='I', fps=10)
    
    # 循环处理视频中的每一帧
    i = 0
    for frame in reader:
        i = i+1
        if i % 2 == 0:
            writer.append_data(frame)
    
    # 关闭写入器
    writer.close()
    print("done")


def reduce_frame_rate(input_file, output_file, target_frame_rate):
    # 使用FFmpeg降低视频的帧率
    command = [
        'ffmpeg',
        '-i', input_file,
        '-r', str(target_frame_rate),
        '-strict', 'experimental',
        output_file
    ]

    try:
        subprocess.run(command, check=True)
        print(f"Video frame rate reduced to {target_frame_rate} FPS and saved to {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

def speed_up_video(input_file, output_file, speed_factor):
    # 构建FFmpeg命令
    command = [
        'ffmpeg',
        '-i', input_file,          # 输入文件
        '-filter:v', f'setpts={1/speed_factor}*PTS',  # 视频速度倍数
        '-filter:a', f'atempo={speed_factor}',        # 音频速度倍数
        output_file                # 输出文件
    ]

    try:
        subprocess.run(command, check=True)
        print(f"Video sped up and saved to {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")


def main():
    print("*"*50)
    print("*\n*   WELCOME TO Init-Bot Tools!\n*   Enjoy it!\n*")
    print("*"*50)
    while True:
        print("Choose a function:")
        print("1 or gif2mp4: GIF to MP4")
        print("2 or mp42gif: MP4 to GIF")
        print("3 or low_fps: MP4 Low-fps")
        print("4 or speed_up: MP4 Speed Up")
        print("q: quit")

        choice = input("Enter your choice (1/2/3/4): ")

        try:
            if choice == "1" or choice == "gif2mp4":
                input_file = input("Enter the path of the input GIF file: ")
                output_file = input("Enter the path of the output MP4 file (or press Enter to use default): ").strip()
                if output_file:
                    output_file = input_file.replace('.gif', '_' + get_datetime_str() + '_.mp4')
                convert_gif_to_mp4(input_file, output_file)
            elif choice == "2" or choice == "mp42gif":
                input_file = input("Enter the path of the input MP4 file: ")
                output_file = input("Enter the path of the output GIF file (or press Enter to use default): ").strip()
                if not output_file:
                    output_file = input_file.replace('.mp4', '_' + get_datetime_str() + '_.gif')
                convert_mp4_to_gif(input_file, output_file)
            elif choice == "3" or choice == "low_fps":
                input_file = input("Enter the path of the input MP4 file: ")
                output_file = input("Enter the path of the output GIF file (or press Enter to use default): ").strip()
                target_frame_rate = input("Enter target frame rate: ").strip()
                if not output_file:
                    output_file = input_file.replace('.mp4', '_' + get_datetime_str() + '_low_fps.mp4')
                target_fps = int(target_frame_rate)
                reduce_frame_rate(input_file, output_file, target_fps)
            elif choice == "4" or choice == "speed_up":
                input_file = input("Enter the path of the input MP4 file: ")
                output_file = input("Enter the path of the output GIF file (or press Enter to use default): ").strip()
                speed_factor = input("Enter speed_factor rate: ").strip()
                if not output_file:
                    output_file = input_file.replace('.mp4', '_' + get_datetime_str() + '_speed_up.mp4')
                speed_factor_rate = float(speed_factor)
                speed_up_video(input_file, output_file, speed_factor_rate)
            elif choice == 'q':
                print("*"*50)
                print("*\n*   Thank you for your valuable suggestions!\n*   Bye!\n*")
                print("*"*50)
                break
            else:
                print("Invalid choice. Please choose 1, 2, 3, 4 or q")
        except Exception as e:
            print("Error: ", e)

if __name__ == "__main__":
    main()
