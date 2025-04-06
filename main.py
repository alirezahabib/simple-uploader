from flask import Flask, request, render_template_string, send_from_directory
import os

app = Flask(__name__)

# Directory to store uploaded files
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# HTML template for the upload page
UPLOAD_PAGE = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Upload Files</title>
</head>
<body>
    <h1>Upload Files</h1>
    <form action="/upload" method="post" enctype="multipart/form-data">
        <input type="file" name="files" multiple>
        <button type="submit">Upload</button>
    </form>
    <p>{{ message }}</p>
    <a href="/files">View Uploaded Files</a>
</body>
</html>
"""

# HTML template for the files page
FILES_PAGE = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Uploaded Files</title>
</head>
<body>
    <h1>Uploaded Files</h1>
    <ul>
        {% for file in files %}
        <li><a href="/files/{{ file }}">{{ file }}</a></li>
        {% endfor %}
    </ul>
    <a href="/">Go Back</a>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(UPLOAD_PAGE, message="")

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'files' not in request.files:
        return render_template_string(UPLOAD_PAGE, message="No files part in the request")

    files = request.files.getlist('files')

    for file in files:
        if file.filename:  # Check if the file has a name
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

    return render_template_string(UPLOAD_PAGE, message=f"Uploaded {len(files)} file(s) successfully!")

@app.route('/files', defaults={'filename': None})
@app.route('/files/<filename>')
def files(filename):
    if filename:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    else:
        files = os.listdir(app.config['UPLOAD_FOLDER'])
        return render_template_string(FILES_PAGE, files=files)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
