from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route("/baixar", methods=["POST"])
def baixar():
    data = request.json
    url = data.get("url")
    nome = "podcast"

    try:
        subprocess.call(f"yt-dlp -f bestaudio --extract-audio --audio-format mp3 {url} -o static/{nome}.mp3", shell=True)
        subprocess.call(f"yt-dlp -f bestvideo {url} -o static/gameplay.mp4", shell=True)

        return jsonify({
            "audio_url": f"/static/{nome}.mp3",
            "video_url": f"/static/gameplay.mp4"
        })
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)
