from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import os
import subprocess
import django_rq
from moviepy import VideoFileClip
from django.core.files import File
import io
from PIL import Image
from .models import Video
import time


def process_video(video_id):
    for attempt in range(5):
        try:
            video = Video.objects.get(id=video_id)
            break
        except Video.DoesNotExist:
            time.sleep(1)
    else:
        return

    video_path = video.video_file.path
    base_path, ext = os.path.splitext(video_path)

    resolutions = {
        "120p": (160, 120),
        "360p": (640, 360),
        "720p": (1280, 720),
        "1080p": (1920, 1080),
    }

    for res, size in resolutions.items():
        output_path = f"{base_path}_{res}.mp4"
        if res == "120p":
            command = [
                "ffmpeg", "-i", video_path, "-vf", "scale=160:-1",
                "-c:v", "libx264", "-preset", "fast", "-crf", "23",
                "-c:a", "aac", "-b:a", "128k", output_path
            ]
        else:
            command = [
                "ffmpeg", "-i", video_path, "-vf", f"scale={size[0]}:{size[1]}",
                "-c:v", "libx264", "-preset", "fast", "-crf", "23",
                "-c:a", "aac", "-b:a", "128k", output_path
            ]
        result = subprocess.run(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            continue

        with open(output_path, "rb") as f:
            if res == "120p":
                video.video_120p.save(
                    f"{video.title}_120p.mp4", File(f), save=False)
            elif res == "360p":
                video.video_360p.save(
                    f"{video.title}_360p.mp4", File(f), save=False)
            elif res == "720p":
                video.video_720p.save(
                    f"{video.title}_720p.mp4", File(f), save=False)
            elif res == "1080p":
                video.video_1080p.save(
                    f"{video.title}_1080p.mp4", File(f), save=False)

    generate_thumbnail(video)
    video.save()


def generate_thumbnail(video):
    video_clip = VideoFileClip(video.video_file.path)
    if video_clip.duration < 2:
        return
    frame = video_clip.get_frame(5)
    pil_image = Image.fromarray(frame).convert("RGB")
    pil_image.thumbnail((200, 150), Image.Resampling.LANCZOS)
    thumb_io = io.BytesIO()
    pil_image.save(thumb_io, 'PNG')
    thumb_dir = os.path.join(settings.MEDIA_ROOT, 'thumbnails')
    if not os.path.exists(thumb_dir):
        os.makedirs(thumb_dir)
    thumb_file_name = os.path.join(thumb_dir, f"{video.title}_thumb.png")
    with open(thumb_file_name, 'wb') as f:
        f.write(thumb_io.getvalue())
    video.thumbnail = os.path.join(
        'thumbnails', f"{video.title}_thumb.png")
    video.save()
    video_clip.close()
