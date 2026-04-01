import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, request
from main import hitung_tsukamoto

app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)

@app.route("/", methods=['GET', 'POST'])
def home():
    hasil_stok = None
    detail = None

    if request.method == 'POST':
        harga   = float(request.form.get('harga', 0))
        terjual = float(request.form.get('terjual', 0))
        hasil_stok, mH, mT = hitung_tsukamoto(harga, terjual)

        detail = {
            'harga_rendah':    round(mH['rendah'], 3),
            'harga_sedang':    round(mH['sedang'], 3),
            'harga_tinggi':    round(mH['tinggi'], 3),
            'terjual_sedikit': round(mT['sedikit'], 3),
            'terjual_sedang':  round(mT['sedang'],  3),
            'terjual_banyak':  round(mT['banyak'],  3),
        }

    return render_template('index.html', hasil=hasil_stok, detail=detail)