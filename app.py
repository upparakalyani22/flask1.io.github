from flask import Flask, render_template, request, redirect, url_for, flash, make_response, session
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = "secret123"

# Folder where uploaded files will be saved
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure upload directory exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/hello/<name>')
def hello(name):
    return f"Hello {name}, welcome to Flask!"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        session['user'] = username
        flash("Login Successful!")
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    user = session.get('user')
    return render_template('dashboard.html', user=user)

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("Logged out successfully")
    return redirect(url_for('home'))

@app.route('/set-cookie')
def set_cookie():
    response = make_response("Cookie has been set")
    response.set_cookie('course', 'flask')
    return response

@app.route('/get-cookie')
def get_cookie():
    course = request.cookies.get('course')
    return f"Cookie value is: {course}"

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files.get("file")
        if not file or file.filename.strip() == "":
            flash("No file selected", "error")
            return redirect(url_for("upload"))

        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash("File uploaded successfully!", "success")
        return redirect(url_for("upload"))

    return render_template('upload.html')

# Custom 404 error page
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(debug=True)
