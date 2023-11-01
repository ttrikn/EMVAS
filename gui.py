import tkinter as tk
from tkinter.filedialog import askopenfilename
import cv2
from PIL import Image, ImageTk
from MSA.demo import offlinedemo, realtimedemo
from MSA.realtime import record_audio_video
from threading import Thread
from moviepy.video.io.VideoFileClip import VideoFileClip
import tkinter.font as tkFont
from queue import Queue
import queue
import pygame
import os


def selectPath():
    path_ = askopenfilename()
    path.set(path_)
    return path_
def startvideo():
    video_path = selectPath()
    path_name = os.path.basename(video_path)
    filename = path_name.split(".")[0]
    audio_path = f"D://djangoproject/MSA/guiaudio/{filename}.wav"

    video_clip = VideoFileClip(video_path)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(audio_path)
    audio_clip.close()

    if os.path.exists(audio_path):
        pygame.mixer.init()
        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play()
    else:
        print("在文件夹中没有找到同名的.wav文件。")
    if video_path[-3:] == "mp4":
        video = cv2.VideoCapture(video_path)
        fps = 150
        while video.isOpened():
            ret, frame = video.read()
            if ret == True:
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
                current_image = Image.fromarray(img).resize((540, 320))
                imgtk = ImageTk.PhotoImage(image=current_image)
                movieLabel1.imgtk = imgtk
                movieLabel1.config(image=imgtk)
                movieLabel1.update()

                cv2.waitKey(int(1000 / fps))
            else:
                break  # 如果视频结束，退出循环
        video.release()  # 循环结束后释放视频捕获对象


def generate(queue):
    video_path = path.get()
    if video_path:
        print(video_path)
    else:
        print("找不到文件")
    result = offlinedemo(video_path)
    queue.put(result)


def on_button_click1():
    result_queue = Queue()
    thread = Thread(target=lambda: generate(result_queue))
    thread.start()
    root.after(100, check_result, result_queue)


def on_button_click2():
    revideo_file, reaudio_file, remixvideo_file = record_audio_video()
    print(revideo_file)
    print(reaudio_file)
    print(remixvideo_file)

    if os.path.exists(reaudio_file):
        pygame.mixer.init()
        pygame.mixer.music.load(reaudio_file)
        pygame.mixer.music.play()
    else:
        print("在文件夹中没有找到同名的.wav文件。")
    if revideo_file[-3:] == "mp4":
        video = cv2.VideoCapture(revideo_file)
        fps = video.get(cv2.CAP_PROP_FPS)
        while video.isOpened():
            ret, frame = video.read()
            if ret == True:
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
                current_image = Image.fromarray(img).resize((540, 320))
                imgtk = ImageTk.PhotoImage(image=current_image)
                movieLabel2.imgtk = imgtk
                movieLabel2.config(image=imgtk)
                movieLabel2.update()

                cv2.waitKey(int(1000 / fps))
            else:
                break  # 如果视频结束，退出循环
        video.release()  # 循环结束后释放视频捕获对象

    realres = realtimedemo(reaudio_file, remixvideo_file)
    result_label2.config(text=f"情绪分析结果为：\n {realres}")


def check_result(result_queue):
    try:
        result = result_queue.get_nowait()
        result_label1.config(text=f"情绪分析结果依次为: \n {result}")
    except queue.Empty:
        root.after(100, check_result, result_queue)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("多模态情绪识别")
    root.geometry("800x1030")
    path = tk.StringVar()
    font_style = tkFont.Font(size=18)
    # 布局
    tk.Label(root, text="目标路径:").place(x=10, y=10, width=100, height=30)
    tk.Entry(root, textvariable=path).place(x=130, y=10, width=500, height=30)
    tk.Button(root, text="选择视频", command=startvideo).place(x=660, y=10, width=100, height=30)
    movieLabel1 = tk.Label(root, bg="white")
    movieLabel1.place(x=130, y=50, width=550, height=330)
    movieLabel2 = tk.Label(root, bg="white")
    movieLabel2.place(x=130, y=540, width=550, height=330)
    result_label1 = tk.Label(root, bg="white")
    result_label1.place(x=30, y=450, width=740, height=60)
    result_label2 = tk.Label(root, bg="white")
    result_label2.place(x=30, y=940, width=740, height=60)
    generate_button1 = tk.Button(root, text="开始检测", command=on_button_click1, font=font_style).place(x=340, y=400,
                                                                                                     width=120,
                                                                                                     height=30)
    generate_button2 = tk.Button(root, text="实时监测", command=on_button_click2, font=font_style).place(x=340, y=890,
                                                                                                     width=120,
                                                                                                     height=30)

root.mainloop()
cv2.destroyAllWindows()
