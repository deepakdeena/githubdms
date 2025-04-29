import os
import fitz  # PyMuPDF for PDF processing
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS to allow frontend access

UPLOAD_FOLDER = 'uploads'
IMAGE_FOLDER = 'extracted_images'

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(IMAGE_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_pdf():
    """Handles PDF file upload and extracts images."""
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    print(f"File saved at: {file_path}")

    images = extract_images_from_pdf(file_path)
    return jsonify({"images": images})  # Returns extracted image URLs

def extract_images_from_pdf(pdf_path):
    """Extracts images from a given PDF and saves them."""
    doc = fitz.open(pdf_path)
    image_paths = []

    for i, page in enumerate(doc):
        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            img_ext = base_image["ext"]
            img_filename = f"image_{i}_{img_index}.{img_ext}"
            img_path = os.path.join(IMAGE_FOLDER, img_filename)

            with open(img_path, "wb") as img_file:
                img_file.write(image_bytes)

            image_paths.append(f"/images/{img_filename}")  # Relative path for frontend use

    print(f"Extracted {len(image_paths)} images")
    return image_paths

@app.route('/images/<filename>')
def get_image(filename):
    """Serves extracted images."""
    return send_from_directory(IMAGE_FOLDER, filename)

@app.route('/get_all_images', methods=['GET'])
def get_all_images():
    """Returns a list of all extracted images."""
    images = [f"/images/{img}" for img in os.listdir(IMAGE_FOLDER) if img.endswith(('png', 'jpg', 'jpeg'))]
    return jsonify({"images": images})

if __name__ == '__main__':
    app.run(debug=True)
