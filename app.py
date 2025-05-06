from flask import Flask, request, jsonify
from deepface import DeepFace
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/verify", methods=["POST"])
def verify_faces():
    if "image1" not in request.files or "image2" not in request.files:
        return jsonify({"error": "Please upload both image1 and image2"}), 400

    image1 = request.files["image1"]
    image2 = request.files["image2"]

    path1 = os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(image1.filename))
    path2 = os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(image2.filename))

    image1.save(path1)
    image2.save(path2)

    try:
        # Use TensorFlow-powered FaceNet for verification
        result = DeepFace.verify(img1_path=path1, img2_path=path2, 
                                 model_name="Facenet", enforce_detection=False)
        return jsonify({
            "verified": result["verified"],
            "distance": result["distance"]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def home():
    return "✅ Face Recognition API with TensorFlow is running!"

if __name__ == "__main__":
    app.run()
