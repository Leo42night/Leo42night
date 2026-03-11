import sys
import yt_dlp
import re

def get_info(url):
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'js_runtime': 'node', # Pastikan Node.js terinstal
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        return ydl.extract_info(url, download=False)

def download_all(url, res, sub_lang, video_title):
    # Output ke folder Videos dengan postfix resolusi
    output_path = f"C:/Users/ADVAN/Videos/%(title)s [{res}p].%(ext)s"
    
    ydl_opts = {
        # Format JS Runtimes yang benar untuk Python
        'js_runtimes': {'node': {}},  
        
        # Penyamaran agar YouTube memberikan link DASH (1080p)
        'impersonate': 'chrome-110', 
        
        # LOGIKA FORMAT: Paksa ambil Video + Audio terpisah (DASH)
        # Format 137 adalah 1080p mp4, 399 adalah 1080p av01
        'format': f"bestvideo[height<={res}]+bestaudio/best[height<={res}]",
        
        'merge_output_format': 'mp4',
        'outtmpl': output_path,
        'writesubtitles': True,             # Cari subtitle manual
        'writeautomaticsub': True,          # Cari subtitle otomatis (WAJIB TRUE)
        'subtitleslangs': [sub_lang] if sub_lang else [],
        'subtitlesformat': 'srt',
        'postprocessors': [
            {'key': 'FFmpegVideoConvertor', 'preferedformat': 'mp4'},
            {'key': 'FFmpegSubtitlesConvertor', 'format': 'srt'},
        ],
        'noplaylist': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        print(f"⚠️ Mencoba tanpa impersonasi karena: {e}")
        del ydl_opts['impersonate']
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

def main():
    if len(sys.argv) < 3:
        print("Penggunaan: yt-down <url> <480/720/1080>")
        return

    url = sys.argv[1]
    max_res = sys.argv[2]

    if max_res not in ["480", "720", "1080"]:
        print("❌ Resolusi tidak didukung. Pilih: 480, 720, atau 1080.")
        return

    print(f"🔍 Menganalisis video: {url}")
    try:
        info = get_info(url)
    except Exception as e:
        print(f"❌ Gagal mengambil info: {e}")
        return

    video_title = info.get('title', 'video')
    
    # Ambil daftar subtitle (Manual & Otomatis)
    subs = info.get('subtitles', {})
    auto_subs = info.get('automatic_captions', {})
    
    all_subs = []
    
    # Filter: Hanya masukkan jika kodenya mengandung 'en' atau 'id'
    # Kita gunakan startswith agar en-US atau id-ID tetap terbawa
    target_langs = ['en', 'id']
    
    # Cek Subtitle Manual
    for lang in subs:
        if any(lang.startswith(t) for t in target_langs):
            all_subs.append({'id': lang, 'name': f"{lang} (Manual)"})
            
    # Cek Subtitle Otomatis
    for lang in auto_subs:
        if any(lang.startswith(t) for t in target_langs):
            all_subs.append({'id': lang, 'name': f"{lang} (Auto)"})

    selected_lang = None
    if all_subs:
        print("\n--- DAFTAR SUBTITLE (EN/ID) ---")
        for i, s in enumerate(all_subs, 1):
            print(f"[{i}] {s['name']}")
        print("[0] Tanpa Subtitle")

        choice = input("\nPilih nomor subtitle: ")
        if choice.isdigit() and 0 < int(choice) <= len(all_subs):
            selected_lang = all_subs[int(choice) - 1]['id']
            print(f"✅ Memilih subtitle: {selected_lang}")
        else:
            print("⏩ Melanjutkan tanpa subtitle.")

    print(f"\n🚀 Mengunduh kualitas {max_res}p (Best Quality)...")
    download_all(url, max_res, selected_lang, video_title)
    print("\n✅ Selesai! Cek folder C:/Users/ADVAN/Videos/")

if __name__ == "__main__":
    main()
