from moviepy.editor import *
import os
import filetype

import shutil
from scipy.io import wavfile
import os
import numpy as np
import argparse
from tqdm import tqdm
import json

from datetime import datetime, timedelta



import argparse

# 修改这里啊
root = "E:\\zjw\\PPASR-master\\newvideo\\"
rootVoice = "E:\\zjw\\PPASR-master\\audio\\"
voiceType = "wav"
videoType = "video/mp4"


# 获取文件名称
def getName(video_name):
    return os.path.basename(video_name).split('.')[0]


# 修改文件后缀例如： C:/dir/a/b.png 需要转为 C:/dir/a/b.jpg  调用函数：trAffter('C:/dir/a/b.png', 'jpg')
def trAffter(path, type):
    a = path.split('/')
    b = a[-1].split('.')
    b[-1] = voiceType
    a[-1] = '.'.join(b)
    return '/'.join(a)


# 提取音频
def extractMp3(video_path):
    print("提取文件：", video_path)
    audio = VideoFileClip(video_path).audio
    # 音频保存的路径
    voice_path = video_path.replace(root, rootVoice)
    destination_folder = r'E:\zjw\PPASR-master\audio'

    print("\t音频保存至：", trAffter(voice_path, voiceType))
    print(trAffter(voice_path, voiceType))
    audio.write_audiofile(trAffter(voice_path, voiceType))
    shutil.copy2(trAffter(voice_path, voiceType),destination_folder)
    # audio.write_audiofile(r'E:\zjw\PPASR-master\audio')


# 遍历目录下的所有文件
def getVideoList(path):
    # 是否为文件
    if not os.path.isdir(path):
        ft = filetype.guess(path)
        if ft is not None and ft.mime == videoType:
            extractMp3(path)
        else:
            print(f"跳过文件{path}")
        return
    # 递归遍历
    for dir in os.listdir(path):
        # 音频保存的路径目录不存在新建
        voice_path = path.replace(root, rootVoice)
        if not os.path.exists(voice_path):
            os.makedirs(voice_path)
        getVideoList(os.path.join(path, dir))


# 开始
# getVideoList(root)






# Utility functions

def GetTime(video_seconds):
    if (video_seconds < 0):
        return 00

    else:
        sec = timedelta(seconds=float(video_seconds))
        d = datetime(1, 1, 1) + sec

        instant = str(d.hour).zfill(2) + ':' + str(d.minute).zfill(2) + ':' + str(d.second).zfill(2) + str('.001')

        return instant


def GetTotalTime(video_seconds):
    sec = timedelta(seconds=float(video_seconds))
    d = datetime(1, 1, 1) + sec
    delta = str(d.hour) + ':' + str(d.minute) + ":" + str(d.second)

    return delta


def windows(signal, window_size, step_size):
    if type(window_size) is not int:
        raise AttributeError("Window size must be an integer.")
    if type(step_size) is not int:
        raise AttributeError("Step size must be an integer.")
    for i_start in range(0, len(signal), step_size):
        i_end = i_start + window_size
        if i_end >= len(signal):
            break
        yield signal[i_start:i_end]


def energy(samples):
    return np.sum(np.power(samples, 2.)) / float(len(samples))


def rising_edges(binary_signal):
    previous_value = 0
    index = 0
    for x in binary_signal:
        if x and not previous_value:
            yield index
        previous_value = x
        index += 1




def main(root):
    root1 = "E:\\zjw\\PPASR-master\\newaudio"
    rootVoice1 = "E:\\zjw\\PPASR-master\\audio"

    for filename in os.listdir(root1):
        file_path = os.path.join(root1, filename)
        # 判断路径是否为文件
        if os.path.isfile(file_path):
            # 删除文件
            os.remove(file_path)
    for filename in os.listdir(rootVoice1):
        file_path = os.path.join(rootVoice1, filename)
        # 判断路径是否为文件
        if os.path.isfile(file_path):
            # 删除文件
            os.remove(file_path)



    getVideoList(root)
    '''
    Last Acceptable Values
    
    min_silence_length = 0.3
    silence_threshold = 1e-3
    step_duration = 0.03/10
    
    '''
    # Change the arguments and the input file here
    folder_path = 'E:\\zjw\\PPASR-master\\audio'
    wav_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.wav')]
    for input_file in wav_files:
        print(f"Processing file: {input_file}")

    #input_file = 'E:\\firefoxdownload\\SpeechEmotionRecognition-master\\zwork\\audio\\20230214-143734.wav'
    output_dir = 'E:\\zjw\\PPASR-master\\newaudio'
    min_silence_length = 0.6  # The minimum length of silence at which a split may occur [seconds]. Defaults to 3 seconds.
    silence_threshold = 1e-4  # The energy level (between 0.0 and 1.0) below which the signal is regarded as silent.
    step_duration = 0.03 / 10  # The amount of time to step forward in the input file after calculating energy. Smaller value = slower, but more accurate silence detection. Larger value = faster, but might miss some split opportunities. Defaults to (min-silence-length / 10.).

    input_filename = input_file
    window_duration = min_silence_length
    if step_duration is None:
        step_duration = window_duration / 10.
    else:
        step_duration = step_duration

    output_filename_prefix = os.path.splitext(os.path.basename(input_filename))[0]
    dry_run = False

    print("Splitting {} where energy is below {}% for longer than {}s.".format(
        input_filename,
        silence_threshold * 100.,
        window_duration
    )
    )

    # Read and split the file

    sample_rate, samples = input_data = wavfile.read(filename=input_filename, mmap=True)

    max_amplitude = np.iinfo(samples.dtype).max
    print(max_amplitude)

    max_energy = energy([max_amplitude])
    print(max_energy)

    window_size = int(window_duration * sample_rate)
    step_size = int(step_duration * sample_rate)

    signal_windows = windows(
        signal=samples,
        window_size=window_size,
        step_size=step_size
    )

    window_energy = (energy(w) / max_energy for w in tqdm(
        signal_windows,
        total=int(len(samples) / float(step_size))
    ))

    window_silence = (e > silence_threshold for e in window_energy)

    cut_times = (r * step_duration for r in rising_edges(window_silence))

    # This is the step that takes long, since we force the generators to run.
    print("Finding silences...")
    cut_samples = [int(t * sample_rate) for t in cut_times]
    cut_samples.append(-1)

    cut_ranges = [(i, cut_samples[i], cut_samples[i + 1]) for i in range(len(cut_samples) - 1)]

    video_sub = {str(i): [str(GetTime(((cut_samples[i]) / sample_rate))),
                          str(GetTime(((cut_samples[i + 1]) / sample_rate)))]
                 for i in range(len(cut_samples) - 1)}

    for i, start, stop in tqdm(cut_ranges):
        output_file_path = "{}_{:03d}.wav".format(
            os.path.join(output_dir, output_filename_prefix),
            i
        )
        if not dry_run:
            print("Writing file {}".format(output_file_path))
            wavfile.write(
                filename=output_file_path,
                rate=sample_rate,
                data=samples[start:stop]
            )
        else:
            print("Not writing file {}".format(output_file_path))

    with open(output_dir + '\\' + output_filename_prefix + '.json', 'w') as output:
        json.dump(video_sub, output)


if __name__=="__main__":
     main()