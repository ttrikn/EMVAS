import pyaudio
import cv2
import subprocess
import wave
import time
import os
from moviepy.editor import VideoFileClip, AudioFileClip
from platform import release


VIDEO_SAVE_FOLDER = 'realtiming/video'
AUDIO_SAVE_FOLDER = 'realtiming/audio'
MIX_SAVE_FOLDER = 'realtiming/mix'
# Set up PyAudio
p = pyaudio.PyAudio()

# Set up OpenCV
cap = cv2.VideoCapture(0)

# 音频采样率
sample_rate = 16000
# fps
frame_rate = 15.625


def record_audio_video():
    # 打开pyaudio流录制音频
    audio_stream = p.open(format=pyaudio.paInt16,
                          channels=1,
                          rate=sample_rate,
                          frames_per_buffer=1024,
                          input=True,
                          input_device_index=5)

    # 设置视频的FourCC代码和帧大小
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    frame_size = (640, 480)

    # 创建一个VideoWriter对象来保存视频
    video_writer = cv2.VideoWriter(os.path.join(VIDEO_SAVE_FOLDER, 'video.mp4'), fourcc, frame_rate, frame_size)

    audio_data = []
    start_time = time.time()
    # 开始循环录制
    while True:
        # 显示摄像头
        ret, frame = cap.read()
        if ret:
            # 将视频帧保存到视频文件
            video_writer.write(frame)
            cv2.imshow('Camera', frame)

            # 从麦克风读取音频数据并将其附加到audio_data变量
            audio = audio_stream.read(1024)
            audio_data.append(audio)
            # 如果用户按下'q'键，则打破循环
            if time.time() - start_time >= 7:
                video_writer.release()
                audio_stream.stop_stream()
                audio_stream.close()
                break
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cap.release()
                # 释放摄像头资源
                video_writer.release()
                # 关闭录像窗口
                cv2.destroyAllWindows()

                # 释放音频资源
                audio_stream.stop_stream()
                audio_stream.close()
                p.terminate()
                break

        else:
            break

    # 保存音频文件为wav
    audio_filename = os.path.join(AUDIO_SAVE_FOLDER, "audio.wav")
    wf = wave.open(audio_filename, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(16000)
    wf.writeframes(b''.join(audio_data))
    wf.close()

    realvideo = os.path.abspath(os.path.join(VIDEO_SAVE_FOLDER, "video.mp4"))
    realaudio = os.path.abspath(os.path.join(AUDIO_SAVE_FOLDER, "audio.wav"))
    realmix = os.path.abspath(os.path.join(MIX_SAVE_FOLDER, "mix_video.mp4"))

    # 合并音频和视频文件
    video_clip = VideoFileClip(realvideo)
    audio_clip = AudioFileClip(realaudio)
    final_clip = video_clip.set_audio(audio_clip)
    final_clip.write_videofile(realmix)

    return realvideo, realaudio, realmix


if __name__ == "__main__":
    a, b, c = record_audio_video()
    print(a, b, c)
