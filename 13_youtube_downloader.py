# ============================================================
# PROJECT 13: YouTube Video Downloader
# Requires: pip install yt-dlp
# yt-dlp is the actively maintained fork of youtube-dl
# ============================================================

import sys
import os
import subprocess

def check_dependencies():
    """Check if yt-dlp is installed."""
    try:
        import yt_dlp
        return True
    except ImportError:
        return False

def install_ytdlp():
    print("  📦 Installing yt-dlp...")
    result = subprocess.run([sys.executable, "-m", "pip", "install", "yt-dlp"],
                             capture_output=True, text=True)
    if result.returncode == 0:
        print("  ✅ yt-dlp installed successfully!")
        return True
    else:
        print(f"  ❌ Installation failed: {result.stderr}")
        return False

def get_video_info(url):
    """Get video information without downloading."""
    import yt_dlp
    ydl_opts = {'quiet': True, 'no_warnings': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return info

def display_formats(info):
    """Display available formats."""
    formats = info.get('formats', [])
    print(f"\n  📹 Title: {info.get('title', 'Unknown')}")
    print(f"  ⏱️  Duration: {info.get('duration', 0)//60}m {info.get('duration', 0)%60}s")
    print(f"  👤 Uploader: {info.get('uploader', 'Unknown')}")
    print(f"  👁️  Views: {info.get('view_count', 0):,}")
    print(f"\n  📋 Available formats:")
    print(f"  {'─'*60}")
    print(f"  {'ID':>6}  {'Ext':5} {'Res':10} {'Size':10} {'Note'}")
    print(f"  {'─'*60}")

    video_formats = [f for f in formats if f.get('vcodec') != 'none'
                      and f.get('height')]

    for fmt in sorted(video_formats, key=lambda x: x.get('height', 0), reverse=True)[:10]:
        fmt_id   = fmt.get('format_id', 'N/A')
        ext      = fmt.get('ext', 'N/A')
        height   = fmt.get('height', 0)
        filesize = fmt.get('filesize') or fmt.get('filesize_approx', 0)
        size_mb  = f"{filesize/1024/1024:.1f}MB" if filesize else "~"
        note     = fmt.get('format_note', '')
        print(f"  {fmt_id:>6}  {ext:5} {str(height)+'p':10} {size_mb:10} {note}")

def download_video(url, output_dir, quality="best", audio_only=False, fmt_id=None):
    """Download video with yt-dlp."""
    import yt_dlp

    os.makedirs(output_dir, exist_ok=True)
    output_template = os.path.join(output_dir, "%(title)s.%(ext)s")

    if audio_only:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_template,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
    elif fmt_id:
        ydl_opts = {
            'format': fmt_id,
            'outtmpl': output_template,
        }
    else:
        format_map = {
            "best": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            "1080p": "bestvideo[height<=1080][ext=mp4]+bestaudio/best[height<=1080]",
            "720p":  "bestvideo[height<=720][ext=mp4]+bestaudio/best[height<=720]",
            "480p":  "bestvideo[height<=480][ext=mp4]+bestaudio/best[height<=480]",
            "360p":  "bestvideo[height<=360][ext=mp4]+bestaudio/best[height<=360]",
        }
        ydl_opts = {
            'format': format_map.get(quality, "best"),
            'outtmpl': output_template,
            'merge_output_format': 'mp4',
        }

    # Progress hook
    def progress_hook(d):
        if d['status'] == 'downloading':
            downloaded = d.get('downloaded_bytes', 0)
            total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
            if total:
                percent = (downloaded / total) * 100
                bar_len = 30
                filled = int(bar_len * percent / 100)
                bar = '█' * filled + '░' * (bar_len - filled)
                speed = d.get('speed', 0)
                speed_str = f"{speed/1024/1024:.1f} MB/s" if speed else "..."
                print(f"\r  [{bar}] {percent:.1f}% {speed_str}", end='', flush=True)
        elif d['status'] == 'finished':
            print(f"\n  ✅ Download complete!")

    ydl_opts['progress_hooks'] = [progress_hook]

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"  📁 Saved to: {output_dir}")
        return True
    except Exception as e:
        print(f"\n  ❌ Download failed: {e}")
        return False

def download_playlist(url, output_dir):
    """Download entire playlist."""
    import yt_dlp
    os.makedirs(output_dir, exist_ok=True)
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': os.path.join(output_dir, "%(playlist_index)s - %(title)s.%(ext)s"),
        'merge_output_format': 'mp4',
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"\n  ✅ Playlist downloaded to: {output_dir}")
    except Exception as e:
        print(f"\n  ❌ Playlist download failed: {e}")

def main():
    print("=" * 55)
    print("      📹 YOUTUBE VIDEO DOWNLOADER")
    print("=" * 55)
    print("  Powered by yt-dlp\n")

    # Check/install dependencies
    if not check_dependencies():
        print("  ⚠️  yt-dlp is not installed.")
        if input("  Install it now? (y/n): ").lower() == 'y':
            if not install_ytdlp():
                print("  Please run: pip install yt-dlp")
                return
        else:
            print("  Please install: pip install yt-dlp")
            return

    # Default download folder
    default_dir = os.path.join(os.path.expanduser("~"), "Downloads", "YouTube")
    print(f"  Default download folder: {default_dir}")

    while True:
        print("\nOptions:")
        print("  1. 📥 Download single video")
        print("  2. 🎵 Download audio only (MP3)")
        print("  3. 📋 Browse formats and select")
        print("  4. 📚 Download playlist")
        print("  5. ℹ️  Get video info")
        print("  6. 🚪 Quit")

        choice = input("\nChoose: ").strip()

        if choice in ['1', '2', '3', '4', '5']:
            url = input("  Enter YouTube URL: ").strip()
            if not url:
                print("  No URL entered!")
                continue

            out_dir = input(f"  Save to folder (Enter for default): ").strip() or default_dir

        if choice == '1':
            print("  Quality: 1) Best  2) 1080p  3) 720p  4) 480p  5) 360p")
            q_map = {"1":"best","2":"1080p","3":"720p","4":"480p","5":"360p"}
            q = q_map.get(input("  Choose (1-5): ").strip(), "best")
            print(f"\n  ⬇️  Downloading {q}...")
            download_video(url, out_dir, quality=q)

        elif choice == '2':
            print("\n  ⬇️  Downloading audio (MP3)...")
            print("  Note: Requires FFmpeg for MP3 conversion.")
            download_video(url, out_dir, audio_only=True)

        elif choice == '3':
            try:
                print("\n  🔍 Fetching video info...")
                info = get_video_info(url)
                display_formats(info)
                fmt_id = input("\n  Enter format ID (or Enter for best): ").strip()
                download_video(url, out_dir, fmt_id=fmt_id if fmt_id else None)
            except Exception as e:
                print(f"  ❌ Error: {e}")

        elif choice == '4':
            download_playlist(url, out_dir)

        elif choice == '5':
            try:
                print("\n  🔍 Fetching info...")
                info = get_video_info(url)
                display_formats(info)
                print(f"\n  📝 Description preview:")
                desc = (info.get('description') or "")[:300]
                print(f"  {desc}...")
            except Exception as e:
                print(f"  ❌ Error: {e}")

        elif choice == '6':
            print("\n  👋 Goodbye!")
            break
        else:
            print("  Invalid choice!")

if __name__ == "__main__":
    main()
