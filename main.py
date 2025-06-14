from flask import Flask, request, jsonify
import subprocess

# Define a pasta estática e sua rota
app = Flask(__name__, static_folder="static", static_url_path="/static")

@app.route("/baixar", methods=["POST"])
def baixar():
    data = request.json
    url = data.get("url")
    nome = "podcast"

    try:
        # Baixa o áudio com user-agent e bypass de bloqueio
        subprocess.call(
            f'yt-dlp --force-ipv4 '
            f'--user-agent "Mozilla/5.0" '
            f'--referer "https://www.youtube.com" '
            f'--extract-audio --audio-format mp3 '
            f'--player-client android --no-playlist '
            f'{url} -o static/{nome}.mp3',
            shell=True
        )

        # Baixa o vídeo (opcional)
        subprocess.call(
            f'yt-dlp -f bestvideo {url} -o static/gameplay.mp4',
            shell=True
        )

        return jsonify({
            "audio_url": f"/static/{nome}.mp3",
            "video_url": "/static/gameplay.mp4"
        })

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)
