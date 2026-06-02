from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB_NAME = 'absensi.db'


# Fungsi untuk inisialisasi database
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS absensi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            kelas TEXT NOT NULL,
            status TEXT NOT NULL,
            waktu TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


# Route Utama: Menampilkan form dan tabel absensi
@app.route('/')
def index():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    # Mengambil data terbaru di atas
    c.execute('SELECT * FROM absensi ORDER BY id DESC')
    data_absen = c.fetchall()
    conn.close()
    return render_template('index.html', data_absen=data_absen)


# Route untuk memproses form absensi
@app.route('/absen', methods=['POST'])
def absen():
    nama = request.form['nama']
    kelas = request.form['kelas']
    status = request.form['status']

    # Mengambil waktu saat ini (format: YYYY-MM-DD HH:MM:SS)
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('INSERT INTO absensi (nama, kelas, status, waktu) VALUES (?, ?, ?, ?)',
              (nama, kelas, status, waktu))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))


# Route untuk menghapus data (opsional/jika ada kesalahan input)
@app.route('/hapus/<int:id>')
def hapus(id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('DELETE FROM absensi WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))


if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)