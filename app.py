from flask import Flask, request, jsonify, render_template
import numpy as np
import cv2
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.efficientnet import preprocess_input

app = Flask(__name__)

# ── Load both models once at startup ──────────────
print("Loading models...")
DEEPFAKE_MODEL = load_model('models/deepfake_model.keras')
AGE_MODEL      = load_model('models/age_model.keras')
print("Models loaded!")

# ── Helper function ────────────────────────────────
def prepare_image(image_path):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (224, 224))
    img = np.expand_dims(img, axis=0)
    img = preprocess_input(img)
    return img

# ── Main route ─────────────────────────────────────
@app.route('/')
def index():
    return render_template('index.html')

# ── Prediction route ───────────────────────────────
@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # Save uploaded image temporarily
    temp_path = 'static/temp_upload.jpg'
    file.save(temp_path)

    try:
        img = prepare_image(temp_path)

        # ── Step 1: Deepfake Detection ─────────────
        deepfake_pred = DEEPFAKE_MODEL.predict(img)[0][0]
        is_real = deepfake_pred > 0.5

        if not is_real:
            return jsonify({
                'status': 'denied',
                'reason': 'deepfake',
                'message': 'Access Denied — Deepfake detected!',
                'deepfake_confidence': float(deepfake_pred)
            })

        # ── Step 2: Age Detection ──────────────────
        age_pred = AGE_MODEL.predict(img)[0][0]
        is_adult = age_pred < 0.5

        if not is_adult:
            return jsonify({
                'status': 'denied',
                'reason': 'age',
                'message': 'Access Denied — Must be 18 or older!',
                'age_confidence': float(age_pred)
            })

        # ── Step 3: Access Granted ─────────────────
        return jsonify({
            'status': 'granted',
            'message': 'Access Granted!',
            'deepfake_confidence': float(deepfake_pred),
            'age_confidence': float(age_pred)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

if __name__ == '__main__':
    app.run(debug=True )