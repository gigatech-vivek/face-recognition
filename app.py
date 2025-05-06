import logging
from flask import Flask, request, jsonify, render_template
import os
from deepface import DeepFace

app = Flask(__name__)

# Setup logging
logging.basicConfig(level=logging.DEBUG)

# Folder to store uploaded images
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/verify", methods=["POST"])
def verify_faces():
    try:
        # Get uploaded images
        image1 = request.files['image1']
        image2 = request.files['image2']

        # Save the images to the uploads folder
        image1_path = os.path.join(app.config['UPLOAD_FOLDER'], image1.filename)
        image2_path = os.path.join(app.config['UPLOAD_FOLDER'], image2.filename)

        image1.save(image1_path)
        image2.save(image2_path)

        # Log the uploaded images for debugging
        logging.debug(f"Image 1 saved at: {image1_path}")
        logging.debug(f"Image 2 saved at: {image2_path}")

        # Verify faces using DeepFace
        result = DeepFace.verify(image1_path, image2_path)

        # Log result for debugging
        logging.debug(f"Verification result: {result}")

        # Remove the uploaded images
        os.remove(image1_path)
        os.remove(image2_path)

        return jsonify(result)
    except Exception as e:
        logging.error(f"Error during face verification: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
