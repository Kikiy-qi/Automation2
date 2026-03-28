import os
import yt_dlp
from moviepy.editor import VideoFileClip

def get_latest_video_urls(channel_url, max_results=5):
    ydl_opts = {
        'extract_flat': True,
        'playlist_items': f'1-{max_results}',
        'quiet': True
    }
    urls = []
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(channel_url, download=False)
        if 'entries' in info:
            for entry in info['entries']:
                if entry.get('url'):
                    urls.append(entry['url'])
    return urls

def download_video(url, output_filename):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
        'outtmpl': output_filename,
        'merge_output_format': 'mp4',
        'quiet': True,
        'no_warnings': True
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
            remove_temp=True,
            logger=None
        )
        output_files.append(output_filename)
        part_clip.close()
            
    clip.close()
    return output_files

def main():
    channel_url = "https://www.youtube.com/@EwingHDTV/videos"
    video_urls = get_latest_video_urls(channel_url)
    
    source_file = "source_video.mp4"
    downloaded = False
    
    for url in video_urls:
        try:
            print(f"Mencoba mengunduh: {url}")
            download_video(url, source_file)
            downloaded = True
            print("Berhasil mengunduh video publik.")
            break
        except Exception:
            print("Gagal mengunduh (mungkin video khusus member). Lanjut ke video berikutnya...")
            continue
            
    if downloaded:
        print("Memulai proses pemotongan menjadi 5 bagian...")
        parts = split_video_into_parts(source_file, 5)
        for part in parts:
            print(f"File siap: {part}")
    else:
        print("Tidak ada video publik yang bisa diunduh.")

if __name__ == "__main__":
    main()
