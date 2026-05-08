import os
import time
from flask import Flask, render_template_string, request, send_file, jsonify
import yt_dlp

app = Flask(__name__)

# Personal Configuration
MY_FACEBOOK = "https://www.facebook.com/kalochele.0070"
MY_TIKTOK = "https://www.tiktok.com/@omor.60?_r=1&_t=ZS-95QqkGPZTVJ"
MY_INSTAGRAM = "https://www.instagram.com/faruk.0070?igsh=MW1rbWwzZmNjMGJhMA=="
MY_YOUTUBE = "https://youtube.com/@faruk0070?si=Fbw7kt24in8leHMT"
PHOTO_PATH = "faruk.jpg" 

HTML_CODE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OMOR DL v5.1</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root { --bg: #000; --box: #1a1a1a; --text: #fff; --accent: #00ffff; --status: #ff0000; }
        body { background-color: var(--bg); color: var(--text); font-family: 'Segoe UI', sans-serif; text-align: center; margin: 0; padding: 20px; transition: 0.3s; }
        body.light-mode { --bg: #f4f4f4; --box: #ffffff; --text: #333; --accent: #007bff; --status: #28a745; }

        .profile-pic { width: 110px; height: 110px; border-radius: 50%; border: 3px solid var(--accent); box-shadow: 0 0 15px var(--accent); object-fit: cover; margin-top: 10px; background: #333; }
        h1 { color: var(--accent); text-transform: uppercase; font-size: 1.6em; margin: 15px 0; text-shadow: 0 0 10px var(--accent); }
        
        .main-box { background: var(--box); padding: 20px; border-radius: 20px; max-width: 400px; margin: auto; border: 1px solid #333; position: relative; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
        
        .input-group { position: relative; margin-bottom: 15px; display: flex; align-items: center; }
        input[type="text"] { width: 100%; padding: 15px; border-radius: 10px; border: 1px solid var(--accent); background: transparent; color: var(--text); outline: none; box-sizing: border-box; }
        .paste-btn { position: absolute; right: 10px; color: var(--accent); cursor: pointer; font-size: 1.2em; transition: 0.2s; background: transparent; border: none; }
        
        #thumbnail-area { display: none; margin: 15px 0; border-radius: 10px; overflow: hidden; border: 1px solid var(--accent); background: #000; position: relative; }
        #thumb-img { width: 100%; display: block; opacity: 0.7; }
        #video-info { position: absolute; bottom: 0; left: 0; right: 0; background: rgba(0,0,0,0.85); padding: 10px; font-size: 12px; text-align: left; border-top: 1px solid var(--accent); }

        select { width: 100%; padding: 12px; border-radius: 10px; background: var(--bg); color: var(--text); border: 1px solid var(--accent); margin-bottom: 15px; outline: none; }
        
        .start-btn { background: transparent; color: var(--status); border: 2px solid var(--status); padding: 15px; border-radius: 10px; width: 100%; font-weight: bold; cursor: pointer; text-transform: uppercase; transition: 0.3s; }
        .start-btn:hover { background: var(--status); color: #fff; }
        
        #progress-overlay { display: none; position: absolute; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.9); border-radius:20px; z-index:100; flex-direction:column; justify-content:center; align-items:center; }
        .spinner { width: 40px; height: 40px; border: 4px solid #f3f3f3; border-top: 4px solid var(--accent); border-radius: 50%; animation: spin 1s linear infinite; }
        
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }

        .social-area { margin-top: 25px; display: flex; justify-content: center; gap: 12px; flex-wrap: wrap; }
        .social-btn { width: 45px; height: 45px; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; text-decoration: none; font-size: 18px; border: 2px solid transparent; transition: 0.3s; }
        .fb { background: #1877f2; } 
        .tk { background: #000; border: 1px solid #fff; } 
        .ig { background: linear-gradient(45deg, #f09433, #bc1888); }
        .yt { background: #ff0000; }
        .social-btn:hover { transform: translateY(-5px); border-color: var(--accent); }
    </style>
</head>
<body onload="requestNotify()">
    <div style="position:fixed; top:20px; right:20px; cursor:pointer; font-size:1.5em; color:var(--accent);" onclick="toggleTheme()">
        <i class="fas fa-moon" id="theme-icon"></i>
    </div>
    
    <img src="/my_photo" class="profile-pic" alt="Omor">
    <h1>OMOR DOWNLOADER</h1>
    
    <div class="main-box">
        <div id="progress-overlay">
            <div class="spinner"></div>
            <p style="color:var(--accent); margin-top:10px;">Processing Download...</p>
        </div>

        <div class="input-group">
            <input type="text" id="url" placeholder="Paste link here..." oninput="fetchPreview()">
            <button class="fas fa-paste paste-btn" onclick="handlePaste()"></button>
        </div>

        <div id="thumbnail-area">
            <img id="thumb-img" src="">
            <div id="video-info">
                <b id="video-title"></b><br>
                <span id="video-meta" style="color: var(--accent);"></span>
            </div>
        </div>

        <select id="quality">
            <option value="best">Best Quality</option>
            <option value="mp3">Audio (MP3)</option>
            <option value="1080">1080p</option>
            <option value="720">720p</option>
            <option value="480">480p</option>
        </select>

        <button onclick="initiateDownload()" class="start-btn">START DOWNLOAD</button>
    </div>

    <div class="social-area">
        <a href="FB_URL" target="_blank" class="social-btn fb"><i class="fab fa-facebook-f"></i></a>
        <a href="TK_URL" target="_blank" class="social-btn tk"><i class="fab fa-tiktok"></i></a>
        <a href="IG_URL" target="_blank" class="social-btn ig"><i class="fab fa-instagram"></i></a>
        <a href="YT_URL" target="_blank" class="social-btn yt"><i class="fab fa-youtube"></i></a>
    </div>

    <script>
        function requestNotify() { if(Notification.permission !== 'granted') Notification.requestPermission(); }
        function toggleTheme() { document.body.classList.toggle('light-mode'); }

        async function handlePaste() {
            try {
                const text = await navigator.clipboard.readText();
                if(text) { 
                    document.getElementById('url').value = text; 
                    fetchPreview(); 
                }
            } catch(e) { alert("Please allow clipboard access or paste manually."); }
        }

        async function fetchPreview() {
            const url = document.getElementById('url').value;
            if(url.length < 8) return;
            const res = await fetch('/get_info?url=' + encodeURIComponent(url));
            const data = await res.json();
            if(data.thumbnail) {
                document.getElementById('thumbnail-area').style.display = 'block';
                document.getElementById('thumb-img').src = data.thumbnail;
                document.getElementById('video-title').innerText = data.title;
                document.getElementById('video-meta').innerText = `Duration: ${data.duration} | Size: ~${data.size}`;
            }
        }

        function initiateDownload() {
            const url = document.getElementById('url').value;
            const q = document.getElementById('quality').value;
            if(!url) return alert('Please paste a link!');
            
            document.getElementById('progress-overlay').style.display = 'flex';
            window.location.href = `/download?url=${encodeURIComponent(url)}&q=${q}`;
            
            setTimeout(() => {
                document.getElementById('progress-overlay').style.display = 'none';
                if(Notification.permission === 'granted') {
                    new Notification("OMOR DL", { body: "Download started!", icon: "/my_photo" });
                }
            }, 6000);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_CODE.replace("FB_URL", MY_FACEBOOK).replace("TK_URL", MY_TIKTOK).replace("IG_URL", MY_INSTAGRAM).replace("YT_URL", MY_YOUTUBE))

@app.route('/my_photo')
def my_photo():
    paths = [PHOTO_PATH, "faruk.jpg", "/sdcard/Download/faruk.jpg", "static/faruk.jpg"]
    for p in paths:
        if os.path.exists(p): return send_file(p)
    return "Photo not found", 404

@app.route('/get_info')
def get_info():
    url = request.args.get('url')
    try:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            filesize = info.get('filesize_approx') or info.get('filesize') or 0
            size_mb = f"{round(filesize / 1000000, 2)} MB" if filesize else "N/A"
            duration = time.strftime('%M:%S', time.gmtime(info.get('duration', 0)))
            return jsonify({
                'thumbnail': info.get('thumbnail'),
                'title': info.get('title')[:60],
                'duration': duration,
                'size': size_mb
            })
    except: return jsonify({'error': 'failed'})

@app.route('/download')
def download():
    url = request.args.get('url')
    q = request.args.get('q')
    ydl_opts = {'outtmpl': 'downloads/%(title)s.%(ext)s'}
    
    if q == 'mp3':
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        })
    else:
        ydl_opts['format'] = f'bestvideo[height<={q}]+bestaudio/best' if q.isdigit() else 'best'

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        file = ydl.prepare_filename(info)
        if q == 'mp3': file = os.path.splitext(file)[0] + ".mp3"
        return send_file(file, as_attachment=True)

if __name__ == "__main__":
    if not os.path.exists('downloads'): os.makedirs('downloads')
    app.run(host='0.0.0.0', port=5000, debug=True)
    
