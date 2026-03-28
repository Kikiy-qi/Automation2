import os
import yt_dlp
from moviepy.editor import VideoFileClip

def download_video(url):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
        'outtmpl': 'source_video.mp4',
        'merge_output_format': 'mp4'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return 'source_video.mp4'

def edit_to_shorts(input_path, output_path, start_time, end_time):
    clip = VideoFileClip(input_path).subclip(start_time, end_time)
    
    w, h = clip.size
    target_ratio = 9 / 16
    target_w = h * target_ratio
    
    x_center = w / 2
    
    clip_resized = clip.crop(
        x1=x_center - target_w/2,
        y1=0,
        x2=x_center + target_w/2,
        y2=h
    )
    
    clip_resized.write_videofile(
        output_path, 
        codec='libx264', 
        audio_codec='aac', 
        temp_audiofile='temp-audio.m4a', 
        remove_temp=True
    )
    
    clip.close()
    clip_resized.close()

def upload_to_youtube(file_path):
    print("Fungsi upload YouTube akan dijalankan di sini")
    pass

def main():
    video_url = "https://www.youtube.com/watch?v=CONTOH_ID_VIDEO"
    
    print("Mengunduh video sumber...")
    download_video(video_url)
    
    print("Memotong dan mengubah ke rasio vertikal 9:16...")
    edit_to_shorts('source_video.mp4', 'final_shorts.mp4', 30, 80)
    
    print("Video final_shorts.mp4 siap diunggah!")
    upload_to_youtube('final_shorts.mp4')

if __name__ == "__main__":
    main()
