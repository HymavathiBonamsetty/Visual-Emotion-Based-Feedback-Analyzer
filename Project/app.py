import os
import real_time_video1,real_time_video2
from flask import Flask, render_template, request, redirect, url_for

UPLOAD_FOLDER = 'static/uploads/'

app = Flask(__name__,static_url_path='/static')
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/live_video')
def live_video():
    real_time_video1.start()
    return redirect(url_for('index'))

@app.route('/upload_video', methods=['POST','GET'])
def upload_video():
    if request.method=='POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        else:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            real_time_video2.start(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
