import os
import cv2
from pathlib import Path


def extract_frames(
    raw_videos_dir="dataset/raw_videos",
    output_dir="dataset/extracted_frames",
    every_nth_frame=60,
    target_width=1280,
    target_height=720
):
    raw_path = Path(raw_videos_dir)
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    video_files = list(raw_path.glob("*.mp4")) + list(raw_path.glob("*.MP4"))
    if not video_files:
        print(f"No videos found in {raw_videos_dir}")
        return

    total_frames_extracted = 0

    for video_file in video_files:
        print(f"Processing: {video_file.name}")
        cap = cv2.VideoCapture(str(video_file))
        if not cap.isOpened():
            print(f"  Warning: Could not open {video_file.name}")
            continue

        frame_count = 0
        extracted_count = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if frame_count % every_nth_frame == 0:
                resized = cv2.resize(frame, (target_width, target_height))
                output_filename = f"{video_file.stem}_frame_{frame_count:06d}.jpg"
                output_path = out_path / output_filename

                if not output_path.exists():
                    cv2.imwrite(str(output_path), resized)
                    extracted_count += 1
                    total_frames_extracted += 1

            frame_count += 1

        cap.release()
        print(f"  Extracted {extracted_count} frames from {video_file.name}")

    print(f"\nDone! Total frames extracted: {total_frames_extracted}")
    print(f"Frames saved to: {output_dir}")


if __name__ == "__main__":
    extract_frames()
