"""
Công cụ hỗ trợ tách Audio TOEIC Listening bằng FFmpeg
Sử dụng:
    python split_audio.py --part 1
    python split_audio.py --part 2
    python split_audio.py --part 3
    python split_audio.py --all
"""

import os
import subprocess
import argparse
import re

AUDIO_DIR = "audio"
OUTPUT_DIR = "audio_segments"

def split_by_silence(input_file, output_prefix, min_silence_duration=1.8, silence_thresh="-30dB"):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"[*] Đang phân tích khoảng lặng trong {input_file}...")
    
    cmd = [
        "ffmpeg", "-i", input_file,
        "-af", f"silencedetect=noise={silence_thresh}:d={min_silence_duration}",
        "-f", "null", "-"
    ]
    
    proc = subprocess.run(cmd, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="ignore")
    lines = proc.stderr.split("\n")
    
    silence_starts = []
    silence_ends = []
    for line in lines:
        s_start = re.search(r"silence_start:\s*([0-9.]+)", line)
        if s_start:
            silence_starts.append(float(s_start.group(1)))
        s_end = re.search(r"silence_end:\s*([0-9.]+)", line)
        if s_end:
            silence_ends.append(float(s_end.group(1)))

    print(f"[*] Tìm thấy {len(silence_ends)} điểm ngắt âm.")
    
    # Cut segments
    start_time = 0.0
    seg_idx = 1
    for end_time in silence_ends:
        duration = end_time - start_time
        if duration > 3.0: # Chỉ lưu các đoạn âm thanh dài hơn 3 giây
            out_file = os.path.join(OUTPUT_DIR, f"{output_prefix}_q{seg_idx:02d}.mp3")
            cut_cmd = [
                "ffmpeg", "-y", "-ss", str(start_time), "-to", str(end_time),
                "-i", input_file, "-c", "copy", out_file
            ]
            subprocess.run(cut_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"    -> Đã tạo: {out_file} ({duration:.1f}s)")
            seg_idx += 1
        start_time = end_time

def main():
    parser = argparse.ArgumentParser(description="Tách file audio TOEIC Listening")
    parser.add_argument("--part", choices=["1", "2", "3"], help="Phần muốn tách (1, 2 hoặc 3)")
    parser.add_argument("--all", action="store_true", help="Tách tất cả các phần")
    args = parser.parse_args()

    files = {
        "1": (os.path.join(AUDIO_DIR, "PART 1 - TEST 1.mp3"), "part1"),
        "2": (os.path.join(AUDIO_DIR, "PART 2 - TEST 1.mp3"), "part2"),
        "3": (os.path.join(AUDIO_DIR, "PART 3 - TEST 1.mp3"), "part3"),
    }

    if args.all or (not args.part and not args.all):
        for p, (fpath, prefix) in files.items():
            if os.path.exists(fpath):
                split_by_silence(fpath, prefix)
    elif args.part:
        fpath, prefix = files[args.part]
        if os.path.exists(fpath):
            split_by_silence(fpath, prefix)
        else:
            print(f"Không tìm thấy file: {fpath}")

if __name__ == "__main__":
    main()
