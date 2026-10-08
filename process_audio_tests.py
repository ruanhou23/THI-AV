import os
import sys
import subprocess
import re
import json

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

def get_silences(mp3_path, noise="-28dB", min_dur=3.0):
    cmd = [
        "ffmpeg", "-i", mp3_path,
        "-af", f"silencedetect=noise={noise}:d={min_dur}",
        "-f", "null", "-"
    ]
    p = subprocess.run(cmd, stderr=subprocess.PIPE, text=True, errors="ignore")
    starts = [float(x) for x in re.findall(r"silence_start:\s*([0-9.]+)", p.stderr)]
    ends = [float(x) for x in re.findall(r"silence_end:\s*([0-9.]+)", p.stderr)]
    return list(zip(starts, ends))

def get_duration(mp3_path):
    cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", mp3_path]
    return float(subprocess.check_output(cmd).decode().strip())

def cut_audio(input_mp3, start_t, end_t, output_mp3):
    os.makedirs(os.path.dirname(output_mp3), exist_ok=True)
    # Using ffmpeg copy
    cmd = [
        "ffmpeg", "-y",
        "-ss", f"{start_t:.2f}",
        "-to", f"{end_t:.2f}",
        "-i", input_mp3,
        "-c", "copy",
        output_mp3
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def process_test(test_dir, test_num):
    print(f"\n=======================================================")
    print(f"[*] Bắt đầu xử lý: {test_dir} (Test {test_num})")
    print(f"=======================================================")
    
    out_base = os.path.join(test_dir, "audio_split")
    os.makedirs(out_base, exist_ok=True)
    manifest = {"test": test_num, "parts": {}}

    # --- PART 1 ---
    mp3_p1 = os.path.join(test_dir, f"PART 1 - TEST {test_num}.mp3")
    if os.path.exists(mp3_p1):
        print(f"[*] Đang tách Part 1: {mp3_p1}")
        silences = get_silences(mp3_p1, noise="-28dB", min_dur=2.0)
        # Expected 7 pauses:
        # Pause 0: after Q1
        # Pause 1: after Q2
        # Pause 2: after "Go on to next page"
        # Pause 3: after Q3
        # Pause 4: after Q4
        # Pause 5: after Q5
        # Pause 6: after Q6
        p1_segments = []
        if len(silences) >= 7:
            # Q1
            p1_segments.append((1, 0.0, silences[0][0] + 0.5))
            # Q2
            p1_segments.append((2, silences[0][1] - 0.2, silences[1][0] + 0.5))
            # Q3 (skipping "Go on to next page" between silences[1] and silences[2])
            p1_segments.append((3, silences[2][1] - 0.2, silences[3][0] + 0.5))
            # Q4
            p1_segments.append((4, silences[3][1] - 0.2, silences[4][0] + 0.5))
            # Q5
            p1_segments.append((5, silences[4][1] - 0.2, silences[5][0] + 0.5))
            # Q6
            p1_segments.append((6, silences[5][1] - 0.2, silences[6][0] + 0.5))
        else:
            print(f"[!] Cảnh báo: Tìm thấy {len(silences)} khoảng lặng cho Part 1")

        p1_out_dir = os.path.join(out_base, "Part 1")
        manifest["parts"]["Part 1"] = []
        for q_num, st, et in p1_segments:
            out_file = os.path.join(p1_out_dir, f"Part1_Q{q_num:02d}.mp3")
            cut_audio(mp3_p1, st, et, out_file)
            dur = et - st
            print(f"    -> Đã tạo: {os.path.basename(out_file)} ({st:.1f}s - {et:.1f}s, dài {dur:.1f}s)")
            manifest["parts"]["Part 1"].append({
                "question": q_num,
                "file": out_file,
                "start": st,
                "end": et,
                "duration": dur
            })

    # --- PART 2 ---
    mp3_p2 = os.path.join(test_dir, f"PART 2 - TEST {test_num}.mp3")
    if os.path.exists(mp3_p2):
        print(f"[*] Đang tách Part 2: {mp3_p2}")
        silences = get_silences(mp3_p2, noise="-28dB", min_dur=3.0)
        tot_dur = get_duration(mp3_p2)
        p2_segments = []
        # Expected 24 pauses for 25 questions (Q7 - Q31)
        if len(silences) >= 24:
            # Q7
            p2_segments.append((7, 0.0, silences[0][0] + 0.5))
            for i in range(1, 24):
                q_num = 7 + i
                st = silences[i-1][1] - 0.2
                et = silences[i][0] + 0.5
                p2_segments.append((q_num, st, et))
            # Q31
            p2_segments.append((31, silences[23][1] - 0.2, tot_dur))
        else:
            print(f"[!] Cảnh báo: Tìm thấy {len(silences)} khoảng lặng cho Part 2")

        p2_out_dir = os.path.join(out_base, "Part 2")
        manifest["parts"]["Part 2"] = []
        for q_num, st, et in p2_segments:
            out_file = os.path.join(p2_out_dir, f"Part2_Q{q_num:02d}.mp3")
            cut_audio(mp3_p2, st, et, out_file)
            dur = et - st
            print(f"    -> Đã tạo: {os.path.basename(out_file)} ({st:.1f}s - {et:.1f}s, dài {dur:.1f}s)")
            manifest["parts"]["Part 2"].append({
                "question": q_num,
                "file": out_file,
                "start": st,
                "end": et,
                "duration": dur
            })

    # --- PART 3 ---
    mp3_p3 = os.path.join(test_dir, f"PART 3 - TEST {test_num}.mp3")
    if os.path.exists(mp3_p3):
        print(f"[*] Đang tách Part 3: {mp3_p3}")
        silences = get_silences(mp3_p3, noise="-28dB", min_dur=5.0)
        tot_dur = get_duration(mp3_p3)
        # Expected 40 pauses (every 3 pauses define 1 conversation)
        p3_segments = []
        conv_ranges = [
            (32, 34), (35, 37), (38, 40), (41, 43), (44, 46),
            (47, 49), (50, 52), (53, 55), (56, 58), (59, 61),
            (62, 64), (65, 67), (68, 70)
        ]
        if len(silences) >= 39:
            for idx, (q_s, q_e) in enumerate(conv_ranges):
                if idx == 0:
                    st = 0.0
                else:
                    prev_p_idx = idx * 3 - 1
                    st = silences[prev_p_idx][1] - 0.2
                
                curr_p_idx = (idx + 1) * 3 - 1
                if curr_p_idx < len(silences):
                    et = silences[curr_p_idx][1]
                else:
                    et = tot_dur
                
                p3_segments.append((f"Q{q_s}_{q_e}", st, et))
        else:
            print(f"[!] Cảnh báo: Tìm thấy {len(silences)} khoảng lặng cho Part 3")

        p3_out_dir = os.path.join(out_base, "Part 3")
        manifest["parts"]["Part 3"] = []
        for q_label, st, et in p3_segments:
            out_file = os.path.join(p3_out_dir, f"Part3_{q_label}.mp3")
            cut_audio(mp3_p3, st, et, out_file)
            dur = et - st
            print(f"    -> Đã tạo: {os.path.basename(out_file)} ({st:.1f}s - {et:.1f}s, dài {dur:.1f}s)")
            manifest["parts"]["Part 3"].append({
                "questions": q_label,
                "file": out_file,
                "start": st,
                "end": et,
                "duration": dur
            })

    manifest_path = os.path.join(out_base, "audio_split_manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print(f"[+] Hoàn thành lưu manifest: {manifest_path}")

def main():
    tests = [
        ("Listening practice test 1", 1),
        ("Listening practice test 2", 2),
        ("Listening practice test 3", 3),
        ("Listening practice test 4", 4),
    ]
    for test_dir, num in tests:
        if os.path.exists(test_dir):
            process_test(test_dir, num)

if __name__ == "__main__":
    main()
