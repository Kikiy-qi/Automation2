import os
import yt_dlp
from moviepy.editor import VideoFileClip

def get_latest_video_url(channel_url):
    ydl_opts = {
        'extract_flat': True,
        'max_downloads': 1,
        'playlist_items': '1',
        'quiet': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(channel_url, download=False)
        if 'entries' in info and len(info['entries']) > 0:
            return info['entries'][0]['url']
    return None

def download_video(url, output_filename):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
        'outtmpl': output_filename,
        'merge_output_format': 'mp4'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return output_filename

def split_video_into_parts(input_path, num_parts=5):
    clip = VideoFileClip(input_path)
    total_duration = clip.duration
    part_duration = total_duration / num_parts
    
    output_files = []
    
    for i in range(num_parts):
        start_time = i * part_duration
        end_time = (i + 1) * part_duration
        
        part_clip = clip.subclip(start_time, end_time)
        output_filename = f"part_{i+1}.mp4"
        
        part_clip.write_videofile(
            output_filename,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile=f'temp-audio-{i}.m4a',
            remove_temp=True
        )
        output_files.append(output_filename)
        part_clip.close()
            
    clip.close()
    return output_files

def main():
    channel_url = "https://www.youtube.com/@EwingHDTV/videos"
    
    video_url = get_latest_video_url(channel_url)
    
    if video_url:
        source_file = "source_video.mp4"
        download_video(video_url, source_file)
        
        parts = split_video_into_parts(source_file, 5)
        
        for part in parts:
            print(f"File siap dipublikasikan: {part}")
    else:
        print("Tidak dapat menemukan video.")

if __name__ == "__main__":
    main()
