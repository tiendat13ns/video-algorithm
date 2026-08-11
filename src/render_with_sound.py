import os
import sys
import subprocess
import imageio_ffmpeg

def merge_audio_video(video_path: str):
    """Merge separate .wav audio track into .mp4 video track or boost existing audio."""
    if not os.path.isabs(video_path):
        video_path = os.path.abspath(video_path)
    
    wav_path = os.path.splitext(video_path)[0] + ".wav"
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    temp_mp4 = os.path.splitext(video_path)[0] + "_temp.mp4"

    if os.path.exists(wav_path) and os.path.exists(video_path):
        cmd = [
            ffmpeg_exe, "-y",
            "-i", video_path,
            "-i", wav_path,
            "-c:v", "copy",
            "-c:a", "aac",
            "-b:a", "192k",
            "-ar", "44100",
            temp_mp4
        ]
        res = subprocess.run(cmd, capture_output=True)
        if res.returncode == 0 and os.path.exists(temp_mp4):
            os.replace(temp_mp4, video_path)
            if os.path.exists(wav_path):
                os.remove(wav_path)
            print(f"[OK] Audio merged successfully into: {video_path}")
        else:
            print(f"[ERROR] Failed to merge audio: {res.stderr.decode('utf-8', errors='ignore')}")
    elif os.path.exists(video_path):
        # Normalize and boost existing embedded audio track
        cmd = [
            ffmpeg_exe, "-y",
            "-i", video_path,
            "-filter:a", "volume=2.5",
            "-c:v", "copy",
            "-c:a", "aac",
            "-b:a", "192k",
            "-ar", "44100",
            temp_mp4
        ]
        res = subprocess.run(cmd, capture_output=True)
        if res.returncode == 0 and os.path.exists(temp_mp4):
            os.replace(temp_mp4, video_path)
            print(f"[OK] Audio boosted and re-encoded in: {video_path}")
        else:
            print(f"[ERROR] Failed to process audio: {res.stderr.decode('utf-8', errors='ignore')}")

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "instagram/LinearRegression.mp4"
    merge_audio_video(target)
