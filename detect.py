from moviepy.editor import VideoFileClip
import glob
import os
def is_video_complete(file_path):
    try:
        # Attempt to load the video file
        video = VideoFileClip(file_path)
        duration = video.duration
        video.reader.close()
        return True, duration
    except Exception as e:
        # An exception occurred, indicating the video is not complete or has issues
        return False, str(e)

if __name__ == "__main__":
    videofile1 = "D://djangoproject/MSA/slicevideo/20221207-164912"
    v_files = glob.glob(os.path.join(videofile1, "*.mp4"))
    for video in v_files:
        is_complete, duration = is_video_complete(video)
        if is_complete:
            print(f"The video {video} is complete and can be played. Duration: {duration} seconds.")
        else:
            print(f"The video {video} is not complete or has issues. Skipping this video. Error: {duration}")


