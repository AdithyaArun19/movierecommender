from flask import Flask, render_template, request, jsonify
import os
import random
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configure upload settings
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'ogg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create uploads directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Emotion-to-movie mapping
emotion_movies = {
    1: {"emotion": "Happy", "movies": ["Inside Out", "Zindagi Na Milegi Dobara", "The Pursuit of Happyness", "La La Land", "Up", "The Intouchables", "Amélie", "The Grand Budapest Hotel"]},
    3: {"emotion": "Sad", "movies": ["The Fault in Our Stars", "Schindler's List", "Grave of the Fireflies", "A Beautiful Mind", "The Green Mile", "Hachi: A Dog's Tale", "Manchester by the Sea", "Blue Valentine"]},
    0: {"emotion": "Angry", "movies": ["John Wick", "Mad Max: Fury Road", "Gladiator", "Fight Club", "The Dark Knight", "Kill Bill: Vol. 1", "300", "The Revenant"]},
    2: {"emotion": "Neutral", "movies": ["Forrest Gump", "The Shawshank Redemption", "Good Will Hunting", "Inception", "The Matrix", "Interstellar", "The Godfather", "Pulp Fiction"]},
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-movies', methods=['POST'])
def get_movies():
    data = request.get_json()
    emotion_number = data.get('emotion_number')

    if emotion_number in emotion_movies:
        movies = random.sample(emotion_movies[emotion_number]["movies"], 3)
        response = {
            "emotion": emotion_movies[emotion_number]["emotion"],
            "movies": movies
        }
    else:
        response = {"error": "Invalid emotion number"}
    
    return jsonify(response)

@app.route('/analyze-audio', methods=['POST'])
def analyze_audio():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file uploaded"})
    
    audio_file = request.files['audio']
    if audio_file.filename == '':
        return jsonify({"error": "No selected file"})
    
    if audio_file and allowed_file(audio_file.filename):
        filename = secure_filename(audio_file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        audio_file.save(filepath)
        
        # TODO: Here you will integrate your emotion detection model
        # For now, we'll return a dummy emotion number (1 for happy)
        emotion_number = 1  # This will be replaced by your model's prediction
        
        # Clean up the uploaded file
        os.remove(filepath)
        
        if emotion_number in emotion_movies:
            movies = random.sample(emotion_movies[emotion_number]["movies"], 3)
            response = {
                "emotion": emotion_movies[emotion_number]["emotion"],
                "movies": movies
            }
        else:
            response = {"error": "Invalid emotion detected"}
        
        return jsonify(response)
    
    return jsonify({"error": "Invalid file type"})

if __name__ == '__main__':
    app.run(debug=True)
