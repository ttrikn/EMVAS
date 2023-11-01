import pickle
# 打开 .pkl 文件并加载数据到变量
#with open("E:\\MMSA-FET-master\\src\\MSA_FET\\feature\\feature2.pkl", 'rb') as f:
    #data = pickle.load(f)
# 打印数据
#print(data)
import moviepy
import pydub

from moviepy.editor import VideoFileClip
import pydub
import os
from pydub.silence import split_on_silence
#最好在前面有个去噪模块

def extract_audio_from_video(video_path, audio_path):
    # 从视频中提取音频
    video_clip = VideoFileClip(video_path)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(audio_path)
    audio_clip.close()

def detect_speech_segments(audio_path, min_silence_duration=600, silence_threshold=-40):
    audio = pydub.AudioSegment.from_file(audio_path)
    speech_segments = pydub.silence.split_on_silence(
        audio, min_silence_len=min_silence_duration, silence_thresh=silence_threshold
    )
    # 记录每个语音段的开始时间和结束时间（单位为毫秒）
    speech_segments_info = []
    prev_end = 0
    for segment in speech_segments:
        start_time = prev_end
        end_time = prev_end + len(segment)
        speech_segments_info.append((start_time, end_time))
        prev_end = end_time
    print(speech_segments_info)
    return speech_segments_info

if __name__ == "__main__":
    video_path = "E://MMSAdatasets//20221207-164912.mp4"
    audio_path = "E://MMSAdatasets//test.wav"

    # Step 1: 提取音频
    extract_audio_from_video(video_path, audio_path)

    # Step 2: 语音分段
    speech_segments = detect_speech_segments(audio_path)

    # Step 3: 切割视频
    video_clip = VideoFileClip(video_path)
    output_folder = "E://MMSAdatasets//slicevideo"

    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    for i, (start_time, end_time) in enumerate(speech_segments):
        start_time_sec = start_time / 1000.0
        end_time_sec = end_time / 1000.0
        print(start_time_sec, end_time_sec)
        #video_chunk = video_clip.subclip(start_time_sec, end_time_sec)
        #output_video_path = os.path.join(output_folder, f"output_chunk_{i}.mp4")
        #video_chunk.write_videofile(output_video_path, codec="libx264")

    video_clip.reader.close()
    video_clip.audio.reader.close_proc()