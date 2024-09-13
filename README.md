# FFmpeg

ffmpeg 是一个非常强大的跨平台的命令行工具，用于转换多媒体数据，包括视频和音频文件的转码、剪辑、合并等多种功能。

FFmpeg 中的 "FF" 是 "Fast Forward" 的缩写，而 "mpeg" 则是 "Motion Picture Experts Group" 的缩写形式，指的是运动图像专家组。

根据不同的资源，FFmpeg 的发音可能有所不同，但是一个较为普遍接受的发音方式是将其读作 "eff eff em peg"。这里的 "eff" 是字母 "F" 的发音，"em" 是字母 "M" 的发音，而 "peg" 则直接读作 "peg"。

因此，当你需要读出 FFmpeg 时，可以按照 "eff eff em peg" 来发音。

# 安装 (mac)

```bash
brew install ffmpeg
```

# 1. 转换视频格式

```bash
ffmpeg -i input1.mp4 output.webm
```

# 2. 截取视频片段

```bash
ffmpeg -i input1.mp4 -ss 00:01:30 -t 00:00:10 -c copy output.mp4 -y
```

这里 -ss 指定开始时间，-t 指定持续时间，-c copy 表示不重新编码。

# 3. 合并视频文件

```bash
ffmpeg -i "concat:input.mp4|demo.mp4" -c copy output.mp4 -y
ffmpeg -i "concat:input.mp4|demo.mp4" -c copy output.mp4 -y
ffmpeg -i "input1.mp4" -i "input2.mp4" -filter_complex "[0:v:0][0:a:0][1:v:0][1:a:0]concat=n=2:v=1:a=1[v][a]" -map "[v]" -map "[a]" output.mp4 -y
```

[Parsed_concat_0 @ 0x7fd82ef2d080] Input link in0:v0 parameters (size 640x360, SAR 1:1) do not match the corresponding output link in0:v0 parameters (1280x720, SAR 1:1)

视频合成之前需要确保分辨率是一样的

```bash
ffmpeg -i input.mp4
```

Stream #0:0[0x1](eng): Video: h264 (Baseline) (avc1 / 0x31637661), yuv420p(tv, progressive), 1280x720 [SAR 1:1 DAR 16:9], 59 kb/s, 30 fps, 30 tbr, 30k tbn (default)

```bash
ffmpeg -i input2.mp4 -vf scale=1280:720 -c:a copy output2_resized.mp4
ffmpeg -i watermark.jpeg -vf scale=100:100 watermark.png -y
```

在 FFmpeg 中，“-vf” 是 “-video_filter” 的缩写，用于指定视频过滤器。
视频过滤器可以对视频进行各种处理操作，比如调整大小（scale）、裁剪（crop）、添加水印（overlay）、调整颜色（hue、saturation、brightness、contrast 等）、旋转（rotate）等。
例如：
“-vf scale=1280:720” 表示将视频的分辨率调整为 1280x720。
“-vf overlay=x=10:y=10” 表示在视频上叠加另一个视频或图像，位置为坐标 (10,10)。

```bash
ffmpeg -i input1.mp4 -i output2_resized.mp4 -filter_complex "[0:v:0][0:a:0][1:v:0][1:a:0]concat=n=2:v=1:a=1[v][a]" -map "[v]" -map "[a]" output.mp4 -y
```

# 4. 添加水印

```bash
ffmpeg -i input1.mp4 -i watermark.png -filter_complex overlay=10:10 output.mp4 -y
ffmpeg -i video.mp4 -i image.jpg -filter_complex "[0:v][1:v]overlay=0:0" output.mp4
```

这里 -i watermark.png 是水印图片，overlay=10:10 表示水印的位置

```bash
ffmpeg -i input1.mp4 -i watermark.png -filter_complex "overlay=x=(main_w-overlay_w)/2:y=(main_h-overlay_h)/2" output.mp4 -y
```

参数解释：
-i input.mp4：指定输入的视频文件。
-i watermark.png：指定水印图像文件。
-filter_complex "overlay=x=(main_w-overlay_w)/2:y=(main_h-overlay_h)/2"：这是一个复杂滤镜参数。其中 “overlay” 表示叠加操作，“x=(main_w-overlay_w)/2” 表示水印在水平方向上居中，即水印的横坐标 x 等于视频宽度（main_w）减去水印宽度（overlay_w）后再除以 2；“y=(main_h-overlay_h)/2” 表示水印在垂直方向上居中，即水印的纵坐标 y 等于视频高度（main_h）减去水印高度（overlay_h）后再除以 2。
output.mp4：指定输出的视频文件名称。

```bash
ffmpeg -i input1.mp4 -vf "drawtext=text='Sample Text':fontcolor=red:fontsize=24:x=w-tw:y=h-th:enable='between(t,10,30)'" output.mp4 -y
```

# 5. 调整视频分辨率

```bash
ffmpeg -i input.mp4 -vf scale=640:480 output.mp4
```

scale=640:480 表示调整为 640x480 分辨率。

# 6. 转换音频格式

```bash
ffmpeg -i input1.mp4 -vn -acodec copy output_audio.mp3
ffmpeg -i input1.mp4 -vn -acodec libmp3lame output_audio.mp3 -y
ffmpeg -i input1.mp4 -vn -acodec libmp3lame -ab 192k -ar 44100 output_audio.mp3 -y
```

参数解释：
-i input_video.mp4：指定输入的视频文件。
-vn：表示不处理视频，即只提取音频。
-acodec copy：指定音频编码方式为复制，这样可以快速地将视频中的音频提取出来而不进行重新编码，速度较快且能保持音频的原有质量。如果需要指定特定的音频编码格式，可以将 “copy” 替换为相应的编码格式名称，如 “-acodec libmp3lame” 表示使用 MP3 编码格式进行重新编码。
output_audio.mp3：指定输出的音频文件名称及格式，这里输出为 MP3 格式，你可以根据需要修改为其他音频格式，如 “.wav”“.flac” 等。
-acodec libmp3lame：FFmpeg 会使用 libmp3lame 编码器对音频进行重新编码
可以使用 -ab 参数来调整音频的比特率。例如，设置音频比特率为 192k
使用 -ar 参数来调整音频的采样率。例如，设置采样率为 44100Hz

在音频领域中，比特率和采样率是两个重要的概念。

## 一、比特率（Bitrate）

定义：
比特率又称码率，指的是单位时间内传输或处理的比特数量，通常用每秒比特数（bps）来表示。
例如，128kbps 的比特率意味着每秒传输 128,000 比特的数据。
对音频质量的影响：
较高的比特率通常意味着更好的音频质量。高比特率能够保留更多的音频细节，使声音更加清晰、丰富和逼真。
低比特率的音频文件可能会丢失一些细节，导致声音听起来比较模糊、单薄或有杂音。
然而，过高的比特率也会增加文件的大小，占用更多的存储空间和传输带宽。
常见的比特率范围：
对于 MP3 等常见音频格式，比特率可以从几十 kbps 到 320kbps 甚至更高。一般来说，128kbps 是比较常见的中等质量比特率，320kbps 则被认为是高质量比特率。

## 二、采样率（Sample Rate）

定义：
采样率是指在单位时间内对模拟音频信号进行采样的次数，通常用赫兹（Hz）表示。
例如，44100Hz 的采样率表示每秒对音频信号采样 44100 次。
对音频质量的影响：
较高的采样率能够捕捉到更广泛的音频频率范围，从而提供更准确和逼真的音频再现。
低采样率可能会导致高频部分的音频信息丢失，使声音听起来比较沉闷或缺乏清晰度。
但是，高采样率也会增加文件的大小和处理要求。
常见的采样率：
常见的音频采样率有 44100Hz（CD 音质）、48000Hz（常用于数字音频和视频）等。一些专业音频应用可能会使用更高的采样率，如 96000Hz 或 192000Hz。

# 8. 去除音频

```bash
ffmpeg -i input1.mp4 -vcodec copy -an output_video_no_audio.mp4
```

# 9. 添加音频到视频

```bash
ffmpeg -i output_video_no_audio.mp4 -i output_audio.mp3 -c:v copy -c:a aac -strict experimental output.mp4 -y
```

# 10. 视频截图

```bash
ffmpeg -i input1.mp4 images/output%d.jpg
ffmpeg -i input1.mp4 -vf fps=1/5 -qscale:v 2 -y images/output%d.jpg
```

-i input.mp4：指定输入文件为 input.mp4。

-vf fps=1/5：
-vf 表示使用视频滤镜（video filter）。
fps=1/5 设置帧率为每秒 1/5 帧。这意味着从视频中每 5 秒提取一帧图像。

-qscale:v 2：
-qscale:v 设置视频的质量级别。
2 是一个质量值，数值越小，质量越高。这里设置为 2，表示较高的图像质量。

-y output%d.jpg：
-y 强制覆盖输出文件，无需确认提示。
output%d.jpg 指定输出文件名格式。%d 是一个占位符，表示按顺序编号的文件名。例如，output0001.jpg, output0002.jpg, 等等。
总结一下，这条命令的作用是从 input.mp4 视频文件中每 5 秒提取一帧图像，并以高质量的 JPEG 格式保存到 output%d.jpg 文件中。

```bash
ffmpeg -i input.mp4 -vframes 1 -ss [时间点] -qscale:v 2 -y output.jpg
ffmpeg -i input.mp4 -vframes 1 -ss 0 -qscale:v 2 -y output.jpg
```

# 11. 图片生成视频

```bash
ffmpeg -framerate 24 -i images/output%d.jpg -c:v libx264 -r 24 -pix_fmt yuv420p video_output.mp4 -y
```
