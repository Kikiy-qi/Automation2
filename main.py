import os
import yt_dlp
from moviepy.editor import VideoFileClip
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def get_latest_video_urls(channel_url, max_results=15):
    ydl_opts = {
        'extract_flat': True,
        'playlist_items': f'1-{max_results}',
        'quiet': True,
        'cookiefile': 'cookies.txt'
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
        'format': 'best',
        'outtmpl': output_filename,
        'quiet': True,
        'no_warnings': True,
        'cookiefile': 'cookies.txt'
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

def upload_to_youtube(video_path, part_number):
    credentials = Credentials.from_authorized_user_file('token.json', ['https://www.googleapis.com/auth/youtube.upload'])
    youtube = build('youtube', 'v3', credentials=credentials)
    
    body = {
        'snippet': {
            'title': f'Ewing HD Paling Menyeramkan - Part {part_number} #shorts',
            'description': f'Cuplikan video Ewing HD bagian {part_number}. #ewinghd #horror #shorts',
            'tags': ['ewing hd', 'horror', 'shorts'],
            'categoryId': '24'
        },
        'status': {
            'privacyStatus': 'public',
            'selfDeclaredMadeForKids': False
        }
    }
    
    media = MediaFileUpload(video_path, chunksize=-1, resumable=True, mimetype='video/mp4')
    request = youtube.videos().insert(part='snippet,status', body=body, media_body=media)
    response = request.execute()
    print(f"Video part {part_number} berhasil diunggah! ID: {response['id']}")

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
            print("Berhasil mengunduh video.")
            break
        except Exception as e:
            print(f"Gagal mengunduh: {e}")
            continue
            
    if downloaded:
        print("Memulai proses pemotongan menjadi 5 bagian...")
        parts = split_video_into_parts(source_file, 5)
        for index, part in enumerate(parts):
            print(f"Mengunggah {part} ke YouTube...")
            try:
                upload_to_youtube(part, index + 1)
            except Exception as e:
                print(f"Gagal upload ke YouTube: {e}")
    else:
        print("Tidak ada video yang bisa diunduh.")

if __name__ == "__main__":
    main()
