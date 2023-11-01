from silence import extract_audio_from_video,cut_audio,cut_video

import subprocess

# 输入视频文件路径
input_video_path = "E://MMSAdatasets/20221207-164912.mp4"
# 输出音频文件路径
output_audio_path = "E://MMSAdatasets/test.wav"

# 使用FFmpeg将视频转换为音频
ffmpeg_cmd = [
    'ffmpeg',         # 命令名
    '-i', input_video_path,  # 输入视频文件路径
    '-vn',             # 禁止视频流
    '-acodec', 'pcm_s16le',  # 指定音频编码器为PCM 16位有符号立体声
    '-ar', '44100',    # 采样率为44100 Hz
    '-ac', '2',        # 2个音频通道（立体声）
    '-y',              # 覆盖输出文件
    output_audio_path  # 输出音频文件路径
]

subprocess.run(ffmpeg_cmd)

print("视频已成功转换为音频。")

video_path = "E://MMSAdatasets/20221207-164912.mp4"
audio_path = "E://MMSAdatasets/test.wav"
#extract_audio_from_video(video_path, audio_path)

output_dir = "E://MMSAdatasets/sliceaudio"
output_path = "E://MMSAdatasets/slicevideo/"

speech_segments_info = cut_audio(audio_path, output_dir)
cut_video(video_path, output_path, speech_segments_info)

