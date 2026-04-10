from flask import Flask, render_template, send_from_directory
import os


app = Flask(__name__, template_folder="templates")

@app.route("/")
def home():
    return render_template("index.html")

 

@app.route('/<folder>/<filename>')
def serve_images(folder, filename):
    return send_from_directory(os.path.join('templates', folder), filename)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5173)  # 🔥 unique port