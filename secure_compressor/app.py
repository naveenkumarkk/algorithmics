from flask import Flask, request, jsonify, render_template, send_from_directory
import os
from werkzeug.utils import secure_filename
from secure_compressor import SecureCompressor
import shutil

app = Flask(__name__)

# Folder configurations
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = os.path.abspath("uploads")
app.config["OUTPUT_FOLDER"] = os.path.abspath("output")


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/compress", methods=["POST"])
def compress():
    password = request.form.get("password")
    uploaded_files = request.files.getlist("files")

    if not password or not uploaded_files:
        return jsonify({"error": "Password and files are required."}), 400

    original_name = secure_filename(uploaded_files[0].filename).split('.')[0]
    folder_path = os.path.join(app.config["UPLOAD_FOLDER"], original_name)
    os.makedirs(folder_path, exist_ok=True)

    for file in uploaded_files:
        file.save(os.path.join(folder_path, secure_filename(file.filename)))

    compressor = SecureCompressor(password)
    encrypted_file_name = f"{original_name}.secure"
    encrypted_file_path = os.path.join(app.config["OUTPUT_FOLDER"], encrypted_file_name)
    compressor.compress_and_encrypt_folder(folder_path, encrypted_file_path)

    return jsonify({
        "message": "Files compressed and encrypted successfully.",
        "output": f"download/{encrypted_file_name}"
    })


@app.route("/decompress", methods=["POST"])
def decompress():
    password = request.form.get("password")
    uploaded_file = request.files.get("file")

    if not password or not uploaded_file:
        return jsonify({"error": "Password and an encrypted file are required."}), 400

    original_name = secure_filename(uploaded_file.filename).split('.')[0]
    encrypted_path = os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(uploaded_file.filename))
    uploaded_file.save(encrypted_path)

    compressor = SecureCompressor(password)
    output_folder = os.path.join(app.config["OUTPUT_FOLDER"], original_name)
    os.makedirs(output_folder, exist_ok=True)
    compressor.decrypt_and_decompress_folder(encrypted_path, output_folder)

    zip_file_name = f"{original_name}.zip"
    zip_file_path = os.path.join(app.config["OUTPUT_FOLDER"], zip_file_name)
    shutil.make_archive(zip_file_path.replace(".zip", ""), 'zip', output_folder)

    return jsonify({
        "message": "Files decrypted and extracted successfully.",
        "output": f"download/{zip_file_name}"
    })


@app.route("/download/<path:filename>")
def download(filename):
    directory = app.config["OUTPUT_FOLDER"]
    safe_filename = secure_filename(filename)

    print(f"Sanitized filename: {safe_filename}")

    file_path = os.path.join(directory, safe_filename)
    if not os.path.exists(file_path):
        return jsonify({"error": f"File {safe_filename} not found in {directory}."}), 404

    return  send_from_directory(directory,safe_filename, as_attachment=True)

@app.route("/test-download")
def test_download():
    directory = app.config["OUTPUT_FOLDER"]
    filename = "Machine_Learning_Adriana_Lima.secure"

    file_path = os.path.join(directory, filename)
    if not os.path.exists(file_path):
        return jsonify({"error": "Test file not found."}), 404

    return send_from_directory(directory, filename, as_attachment=True)



if __name__ == "__main__":
    app.run(debug=True)
