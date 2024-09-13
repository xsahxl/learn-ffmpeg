import subprocess

def convert_video(input_file, output_file):
    command = [
        'ffmpeg',
        '-i', input_file,
        output_file
    ]
    
    try:
        # 执行 ffmpeg 命令
        subprocess.run(command, check=True)
        print(f"视频转换成功：{input_file} -> {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"视频转换失败：{e}")
    except Exception as e:
        print(f"发生错误：{e}")

# 调用函数
input_file = 'input1.mp4'
output_file = 'output.webm'
convert_video(input_file, output_file)