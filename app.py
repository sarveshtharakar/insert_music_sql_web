from flask import Flask, render_template, request, redirect, url_for, send_file
import mysql.connector
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'music'

# Configure MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Sarvesh98#",
    database="music"
)

@app.route('/')
def index():
    cursor = db.cursor()
    cursor.execute('SELECT * FROM songs')
    songs = cursor.fetchall()
    cursor.close()
    return render_template('index.html', songs=songs)

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        title = request.form['title']
        artist = request.form['artist']
        file = request.files['file']

        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            cursor = db.cursor()
            cursor.execute('INSERT INTO songs (title, artist, file_path) VALUES (%s, %s, %s)',
                           (title, artist, file_path))
            db.commit()
            cursor.close()

    return redirect(url_for('index'))

@app.route('/play/<int:song_id>')
def play(song_id):
    cursor = db.cursor()
    cursor.execute('SELECT file_path FROM songs WHERE id = %s', (song_id,))
    song = cursor.fetchone()
    cursor.close()

    if song:
        song_path = song[0]
        return send_file(song_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
