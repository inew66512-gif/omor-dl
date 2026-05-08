import os
from flask import Flask, render_template_string, request, send_file, jsonify
import yt_dlp

app = Flask(__name__)

# Personal Configuration
MY_FACEBOOK = "https://www.facebook.com/kalochele.0070"
MY_TIKTOK = "https://www.tiktok.com/@omor.60?_r=1&_t=ZS-95QqkGPZTVJ"
MY_INSTAGRAM = "https://www.instagram.com/faruk.0070?igsh=MW1rbWwzZmNjMGJhMA=="

# সরাসরি গিটহাবের র ইমেজ লিঙ্ক ব্যবহার করা হয়েছে যাতে ছবি ১০০% দেখা যায়
PHOTO_URL = "https://raw.githubusercontent.com/inew66512-gif/omor-dl/main/faruk.jpg"

HTML_CODE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OMOR DL v3.0</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        :root { --bg: #000; --box: #1a1a1a; --text: #fff; --accent: #00ffff; }
        body { background-color: var(--bg); color: var(--text); font-family: 'Segoe UI', sans-serif; text-align: center; margin: 0; padding: 20px; }
        .profile-pic { width: 110px; height: 110px; border-radius: 50%; border: 3px solid var(--accent); box-shadow: 0 0 15px var(--accent); object-fit: cover; margin-top: 10px; }
        h1 { color: var(--accent); text-transform: uppercase; font-size: 1.6em; margin: 15px 0; text-shadow: 0 0 10px var(--accent); }
        .main-box { background: var(--box); padding: 20px; border-radius: 20px; max-width: 400px; margin: auto; border: 1px solid #333; }
        .input-group { position: relative; margin-bottom: 15px; display: flex; align-items: center; }
        input[type="text"] { width: 100%; padding: 15px; border-radius: 10px; border: 1px solid var(--accent); background: var(--bg); color: var(--text); outline: none; box-sizing: border-box; }
        .paste-btn { position: absolute; right: 10px; color: var(--accent); cursor: pointer; font-size: 1.2em; }
        
        #thumbnail-area { display: none; margin: 15px 0; border-radius: 10px; overflow: hidden; border: 1px solid var(--accent); background: #000; }
        #thumb-img { width: 100%; display: block; }
        #video-title { font-size: 12px; padding: 10px; color: #fff; margin: 0; background: rgba(0,0,0,0.7); }

        select { width: 100%; padding: 12px; border-radius: 10px; background: var(--bg); color: var(--text); border: 1px solid var(--accent); margin-bottom: 15px; outline: none; }
        .start-btn { background: transparent; color: #ff0000; border: 2px solid #ff0000; padding: 15px; border-radius: 10px; width: 100%; font-weight: bold; cursor: pointer; text-transform: uppercase; margin-bottom: 15px; }
        
        .supported-platforms { font-size: 1.2em; color: #555; display: flex; justify-content: center; gap: 15px; padding-top: 10px; border-top: 1px solid #333; }
        .social-area { margin: 25px auto; display: flex; justify-content: center; gap: 15px; }
        .social-btn { width: 55px; height: 55px; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; text-decoration: none; font-size: 22px; border: 2px solid; }
        .fb { background: #1877f2; border-color: #1877f2; } 
        .tk { background: #000; border-color: #fff; } 
        .ig { background: linear-gradient(45deg, #f09433, #bc1888); border-color: #dc2743; }
    </style>
</head>
<body>
    <img src="{{ profile_pic }}" class="profile-pic">
    <h1>OMOR DOWNLOADER</h1>
    <div class="main-box">
        <div class="input-group">
            <input type="text" id="url" placeholder="Paste video link here..." oninput="fetchPreview()">
            <i class="fas fa-paste paste-btn" onclick="handlePaste()"></i>
        </div>

        <div id="thumbnail-area">
            <img id="thumb-img" src="">
            <p id="video-title"></p>
        </div>

        <select id="quality">
            <option value="best">Best Quality (Auto)</option>
            <option value="1080">1080p Full HD</option>
            <option value="720">720p HD</option>
            <option value="480">480p SD</option>
            <option value="mp3">Audio (MP3)</option>
        </select>

        <button onclick="initiateDownload()" class="start-btn">START DOWNLOAD</button>

        <div class="supported-platforms">
            <i class="fab fa-youtube"></i>
            <i class="fab fa-facebook"></i>
            <i class="fab fa-tiktok"></i>
            <i class="fab fa-instagram"></i>
        </div>
    </div>

    <div class="social-area">
        <a href="{{ fb }}" target="_blank" class="social-btn fb"><i class="fab fa-facebook-f"></i></a>
        <a href="{{ tk }}" target="_blank" class="social-btn tk"><i class="fab fa-tiktok"></i></a>
        <a href="{{ ig }}" target="_blank" class="social-btn ig"><i class="fab fa-instagram"></i></a>
    </div>

    <script>
        async function handlePaste() {
            try {
                const text = await navigator.clipboard.readText();
                if(text) { 
                    document.getElementById('url').value = text; 
                }
            } catch(e) { alert("Please paste the link manually."); }
        }
        // ... বাকি জাভাস্ক্রিপ্ট কোড এখানে থাকবে ...
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_CODE, 
                                 profile_pic=PHOTO_URL, 
                                 fb=MY_FACEBOOK, 
                                 tk=MY_TIKTOK, 
                                 ig=MY_INSTAGRAM)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
                const response = await fetch('/get_info?url=' + encodeURIComponent(url));
                const data = await response.json();
                if(data.thumbnail) {
                    area.style.display = 'block';
                    document.getElementById('thumb-img').src = data.thumbnail;
                    document.getElementById('video-title').innerText = data.title;
                }
            } catch(e) { area.style.display = 'none'; }
        }

        function initiateDownload() {
            const url = document.getElementById('url').value;
            const q = document.getElementById('quality').value;
            if(!url) return alert('Link is required!');
            window.location.href = "/download?url=" + encodeURIComponent(url) + "&q=" + q;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    # Replacing URLs into the HTML safely
    page = HTML_CODE.replace("FB_URL", MY_FACEBOOK).replace("TK_URL", MY_TIKTOK).replace("IG_URL", MY_INSTAGRAM)
    return render_template_string(page)

@app.route('/my_photo')
def my_photo():
    if os.path.exists(PHOTO_PATH):
        return send_file(PHOTO_PATH)
    return "Photo not found", 404

@app.route('/get_info')
def get_info():
    url = request.args.get('url')
    if not url: return jsonify({'error': 'No URL'})
    try:
        ydl_opts = {'quiet': True, 'noplaylist': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return jsonify({
                'thumbnail': info.get('thumbnail'),
                'title': info.get('title')
            })
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/download')
def download():
    url = request.args.get('url')
    q = request.args.get('q', 'best')
    try:
        if q == 'mp3':
            fmt = 'bestaudio/best'
        elif q == 'best':
            fmt = 'bestvideo+bestaudio/best'
        else:
            fmt = f'bestvideo[height<={q}]+bestaudio/best'
            
        ydl_opts = {
            'format': fmt,
            'outtmpl': '%(title)s.%(ext)s',
            'noplaylist': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
            if os.path.exists(file_path):
                return send_file(file_path, as_attachment=True)
            return "File download failed."
    except Exception as e:
        # Fixed error message variable for Python
        return f"Download Error: {str(e)}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
