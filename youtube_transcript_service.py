from flask import Flask, request, jsonify
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi
import re

app = Flask(__name__)
CORS(app)  # Enable CORS for Make to call this service

def extract_video_id(url):
    """Extract YouTube video ID from various URL formats"""
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n?#]+)',
        r'youtube\.com\/embed\/([^&\n?#]+)',
        r'youtube\.com\/v\/([^&\n?#]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "YouTube Transcript API"})

@app.route('/transcript', methods=['POST'])
def get_transcript():
    """
    Extract transcript from YouTube video
    
    Request body:
    {
        "youtube_url": "https://www.youtube.com/watch?v=VIDEO_ID"
    }
    
    Response:
    {
        "video_id": "VIDEO_ID",
        "transcript": "Full transcript text...",
        "language": "en"
    }
    """
    try:
        data = request.get_json()
        youtube_url = data.get('youtube_url')
        
        if not youtube_url:
            return jsonify({"error": "youtube_url is required"}), 400
        
        # Extract video ID
        video_id = extract_video_id(youtube_url)
        if not video_id:
            return jsonify({"error": "Invalid YouTube URL"}), 400
        
        # Get transcript
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        
        # Combine all transcript segments into one text
        full_transcript = " ".join([item['text'] for item in transcript_list])
        
        # Clean up transcript (remove extra spaces, newlines)
        full_transcript = re.sub(r'\s+', ' ', full_transcript).strip()
        
        return jsonify({
            "video_id": video_id,
            "transcript": full_transcript,
            "language": transcript_list[0].get('language', 'en') if transcript_list else 'en',
            "length": len(full_transcript)
        })
    
    except Exception as e:
        return jsonify({
            "error": str(e),
            "message": "Failed to extract transcript. Video may not have captions available."
        }), 500

@app.route('/', methods=['GET'])
def home():
    """Home endpoint with API documentation"""
    return jsonify({
        "service": "YouTube Transcript Extraction API",
        "version": "1.0.0",
        "endpoints": {
            "GET /health": "Health check",
            "POST /transcript": "Extract transcript from YouTube URL",
            "GET /": "This documentation"
        },
        "usage": {
            "endpoint": "POST /transcript",
            "body": {
                "youtube_url": "https://www.youtube.com/watch?v=VIDEO_ID"
            },
            "response": {
                "video_id": "VIDEO_ID",
                "transcript": "Full transcript text",
                "language": "en",
                "length": 12345
            }
        }
    })

if __name__ == '__main__':
    # For local development
    app.run(host='0.0.0.0', port=5000, debug=True)
