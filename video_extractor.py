#!/usr/bin/env python3
import cv2
import os
import argparse

def video_extractor(file_name, output_directory, start_time, end_time, duration):
    # ========================
    # 設定
    # ========================
    file_path = os.path.normpath(os.path.join(os.getcwd(), file_name))

    video_basename = os.path.splitext(os.path.basename(file_path))[0]
    output_directory = os.path.join(output_directory, video_basename)

    # ========================
    # 初期化
    # ========================
    cap = cv2.VideoCapture(file_path)
    if not cap.isOpened():
        print(f"Failed to open video: {file_path}")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        print("Failed to get FPS from video.")
        cap.release()
        return

    os.makedirs(output_directory, exist_ok=True)

    # 開始時刻のフレームまでシーク
    frame_index = int(start_time * fps)
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
    frame_index = int(cap.get(cv2.CAP_PROP_POS_FRAMES))

    next_save_time = start_time
    saved_count = 0

    # ========================
    # 動画読み込み
    # ========================
    while True:
        t = frame_index / fps
        if t > end_time:
            break

        # 保存しないフレームはデコード結果を取り出さずに読み飛ばす
        if t < next_save_time:
            if not cap.grab():
                break
            frame_index += 1
            continue

        ret, frame = cap.read()
        if not ret:
            break
        frame_index += 1

        timestamp = int(t)
        filename = os.path.join(
            output_directory,
            f"image_{saved_count:04d}_{timestamp}.png"
        )
        cv2.imwrite(filename, frame)

        print(f"Saved: {filename}")

        saved_count += 1
        next_save_time += duration

    cap.release()
    print("Done.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file_name", help="video file (mp4, etc.)")
    parser.add_argument("-o", "--output_directory", default="extracted_images/", help="base output directory (a subdirectory named after the video file is created under it)")
    parser.add_argument("-s", "--start_time", default="0", help="start time")
    parser.add_argument("-e", "--end_time", default="1000", help="end time")
    parser.add_argument("-d", "--duration", default="1", help="capture duration")
    args = parser.parse_args()
    file_name = args.file_name
    output_directory = args.output_directory
    s = float(args.start_time)
    e = float(args.end_time)
    d = float(args.duration)
    video_extractor(file_name, output_directory, s, e, d)
