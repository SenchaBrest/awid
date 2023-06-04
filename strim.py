import cv2
import time
from datetime import datetime
from moviepy.editor import VideoFileClip, concatenate_videoclips
from itertools import chain
from db import Database

def save_video_stream(url, current_time, duration=60):
    cap = cv2.VideoCapture(url)

    if not cap.isOpened():
        print("Ошибка при открытии видео трансляции")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    output_file = f"videos/{url.split('/')[-1]}_{current_time}.mp4"

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

    start_time = time.time()
    while time.time() - start_time < duration:
        ret, frame = cap.read()
        if ret:
            out.write(frame)
        else:
            break
    cap.release()
    out.release()


def union(video_paths, output_path):
    clips = []
    for video_path in video_paths:
        clip = VideoFileClip(video_path)
        clips.append(clip)
    
    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")


def check(arr1, arr2):
    set1 = set(list(chain.from_iterable(arr1)))
    set2 = set(list(chain.from_iterable(arr2)))
    return bool(set1.intersection(set2))


def remove(video_paths):
    pass


def main(url):
    db = Database()
    aqp = []
    for _ in range(3 * 6):
        aqp.append(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
        save_video_stream(url, aqp[-1])
    
    flags = [False, False]
    while True:
        flags[1] = check(db.get_records_ids(url, aqp[-1], aqp[-2]), db.get_records_ids(url, aqp[- 3 * 6 + 1], aqp[- 3 * 6]))
        if flags[0] is False and flags[1] is False: 
            remove() # TODO: remove
        elif flags[0] is False and flags[1] is True: 
            pass
        elif flags[0] is True and flags[1] is True: 
            pass
        else:
            union() # TODO: union
            remove() # TODO: remove
        flags[0] = flags[1]


if __name__ == "__main__":
    main(url = "https://s1.moidom-stream.ru/s/public/0000001301.m3u8")

