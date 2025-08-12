from flask import Flask, request, jsonify
import requests
from flask_cors import CORS  # <-- import CORS

app = Flask(__name__)
CORS(app)

# URL of your existing video microservice
VIDEO_SERVICE_URL = "http://localhost:7006/videos"

@app.route('/search', methods=['GET'])
def search_videos():
    query = request.args.get('q', '').strip().lower()

    # Fetch all videos from the video microservice
    try:
        resp = requests.get(VIDEO_SERVICE_URL)
        resp.raise_for_status()
        videos = resp.json()
    except requests.RequestException as e:
        return jsonify({"error": f"Could not fetch videos: {e}"}), 500

    if not query:
        # Return all videos if no search query provided
        return jsonify(videos)

    # Filter videos by title or description match
    results = [
    v for v in videos
    if query in v.get("filename", "").lower()  # or whatever key exists
       or query in v.get("description", "").lower()
    ]


    return jsonify(results)

if __name__ == "__main__":
    app.run(port=7007, debug=True)
