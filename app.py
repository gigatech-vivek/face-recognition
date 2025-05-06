import os
from flask import Flask, request, render_template, jsonify
from deepface import DeepFace

app = Flask(__name__)

# Folder to store uploaded images
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Route to render the HTML form
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

# Route to handle the face verification
@app.route("/verify", methods=["POST"])
def verify_faces():
    image1 = request.files['image1']
    image2 = request.files['image2']
    
    # Save the uploaded images to the 'uploads' folder
    image1_path = os.path.join(app.config['UPLOAD_FOLDER'], image1.filename)
    image2_path = os.path.join(app.config['UPLOAD_FOLDER'], image2.filename)
    
    image1.save(image1_path)
    image2.save(image2_path)

    # Perform face verification using DeepFace
    result = DeepFace.verify(image1_path, image2_path)

    # Clean up the uploaded images (optional, remove after processing)
    os.remove(image1_path)
    os.remove(image2_path)

    # Return the result
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
