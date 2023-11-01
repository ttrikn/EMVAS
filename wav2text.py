# 视频切割 转文本 生成路径
import glob
import pydub
from pydub import AudioSegment
from MSA.silence import  cut_video,cut_audio,extract_audio_from_video
from app01.PPASRmaster.zimu import predict_audio
import os
def video2text(videopath):
    path_name = os.path.basename(videopath)
    filename = path_name.split(".")[0]
    print(filename)
    # 视频路径
    video_path = videopath
    if not os.path.exists(f"D://djangoproject/MSA/sliceaudio/{filename}"):
        os.mkdir(f"D://djangoproject/MSA/sliceaudio/{filename}")
    audio_path = f"D://djangoproject/MSA/sliceaudio/{filename}.wav"
    extract_audio_from_video(video_path, audio_path)

    output_dir = f"D://djangoproject//MSA/sliceaudio/{filename}"

    if not os.path.exists(f"D://djangoproject//MSA/slicevideo/{filename}"):
        os.mkdir(f"D://djangoproject//MSA/slicevideo/{filename}")
    output_path = f"D://djangoproject//MSA/slicevideo/{filename}/{filename}"
    speech_segments_info = cut_audio(audio_path, output_dir)
    cut_video(video_path, output_path, speech_segments_info)

    wav_files = glob.glob(os.path.join(output_dir, "*.wav"))

    for audio in wav_files:
        #full_audio_name = os.path.join(output_dir,audio)
        audiotime = AudioSegment.from_file(audio)
        duration_ms = len(audiotime)
        if duration_ms >= 1000:
            print(audio)
            text = predict_audio(audio)
        else:
            print("语音时间过短")
            text = "语音时间过短"
        # 假设你得到的结果是一个字符串
        #headname = audio.split(".")[0]
        # 新建一个txt文件并保存结果
        if not os.path.exists(f"D://djangoproject//MSA/slicetext/{filename}"):
            os.mkdir(f"D://djangoproject//MSA/slicetext/{filename}")
        textname = f"D://djangoproject//MSA/slicetext/{filename}/"
        headname = os.path.basename(audio)
        headname = headname.split(".")[0]
        textfullname = textname + headname + ".txt"  # 新建的txt文件名
        with open(textfullname, "w", encoding="utf-8") as file:
            file.write(str(text))
        print("结果已保存到", textfullname)
    return filename
    # videoname = "E://MSA/slicevideo/"+filename
    # if os.path.exists(videoname): None
    # else : os.mkdir(videoname)
    # print(videoname)

    # # 语音路径
    # audioname = "E://MSA/sliceaudio/"+filename
    # print(audioname)
    # if os.path.exists(audioname): None
    # else : os.mkdir(audioname)
    # 文本路径
    # textname = "E://MSA/slicetext/" + filename
    # if os.path.exists(textname):
    #     None
    # else:
    #     os.mkdir(textname)
    #

    # 转语音
    # for video in videoname:
    #     full_video_name = os.path.join(videoname,video)
    #     extract_audio_from_video(full_video_name,audioname)
    # 转文本
    # for audio in audioname:
    #     full_audio_name = os.path.join(audioname,audio)
    #     text = predict_audio(full_audio_name)
    #     # 假设你得到的结果是一个字符串
    #     headname = audio.split(".")[0]
    #     # 新建一个txt文件并保存结果
    #     filename = textname + headname + ".txt"  # 新建的txt文件名
    #     with open(filename, "w", encoding="utf-8") as file:
    #         file.write(str(text))
    #     print("结果已保存到", filename)
    # return


if __name__=="__main__":
	video2text("E://MSA/20230214-192557.mp4")



