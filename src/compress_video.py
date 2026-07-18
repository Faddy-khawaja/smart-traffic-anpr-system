import subprocess
import imageio_ffmpeg

ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()

input_path = "demo/traffic-anpr-detection-demo.mp4"
output_path = "demo/traffic-anpr-demo-compressed.mp4"

command = [
    ffmpeg_path,
    "-i", input_path,
    "-vcodec", "libx264",
    "-crf", "30",
    "-preset", "fast",
    output_path,
]

subprocess.run(command, check=True)
print("Compression done:", output_path)