from flask import Flask, render_template, request

app = Flask(__name__)

def hitung_tsukamoto(harga, terjual):
    # --- 1. FUZZIFIKASI ---

    # HARGA (juta): Rendah 1-4, Sedang 3-7, Tinggi 6-10
    def harga_rendah(x):
        if x <= 3: return 1
        if x >= 5: return 0
        return (5 - x) / (5 - 3)

    def harga_sedang(x):
        if x <= 3 or x >= 7: return 0
        if x == 5: return 1
        if x < 5: return (x - 3) / (5 - 3)
        return (7 - x) / (7 - 5)

    def harga_tinggi(x):
        if x <= 5: return 0
        if x >= 7: return 1
        return (x - 5) / (7 - 5)

    # TERJUAL (unit): Sedikit 0-20, Sedang 15-35, Banyak 30-50
    def terjual_sedikit(x):
        if x <= 15: return 1
        if x >= 25: return 0
        return (25 - x) / (25 - 15)

    def terjual_sedang(x):
        if x <= 15 or x >= 40: return 0
        if x == 25: return 1
        if x < 25: return (x - 15) / (25 - 15)
        return (40 - x) / (40 - 25)

    def terjual_banyak(x):
        if x <= 30: return 0
        if x >= 50: return 1
        return (x - 30) / (50 - 30)

    # Hitung derajat keanggotaan input
    mH = {
        'rendah': harga_rendah(harga),
        'sedang': harga_sedang(harga),
        'tinggi': harga_tinggi(harga),
    }
    mT = {
        'sedikit': terjual_sedikit(terjual),
        'sedang':  terjual_sedang(terjual),
        'banyak':  terjual_banyak(terjual),
    }

    # --- 2. RULES & INFERENSI ---
    # Output Stok: Berkurang (10–30), Bertambah (30–60)
    # Invers monoton naik  → z = 30 + a*(60-30)
    # Invers monoton turun → z = 30 - a*(30-10)

    def z_bertambah(a): return 30 + a * 30   # [30, 60]
    def z_berkurang(a): return 30 - a * 20   # [10, 30]

    # Rules (alpha, z_value)
    rules = [
        # Harga Rendah → cenderung laku → stok bertambah
        (min(mH['rendah'], mT['banyak']),   z_bertambah),
        (min(mH['rendah'], mT['sedang']),   z_bertambah),
        (min(mH['rendah'], mT['sedikit']),  z_berkurang),

        # Harga Sedang
        (min(mH['sedang'], mT['banyak']),   z_bertambah),
        (min(mH['sedang'], mT['sedang']),   z_berkurang),
        (min(mH['sedang'], mT['sedikit']),  z_berkurang),

        # Harga Tinggi → cenderung tidak laku → stok berkurang
        (min(mH['tinggi'], mT['banyak']),   z_berkurang),
        (min(mH['tinggi'], mT['sedang']),   z_berkurang),
        (min(mH['tinggi'], mT['sedikit']),  z_berkurang),
    ]

    # --- 3. DEFUZZIFIKASI (Weighted Average) ---
    total_az = sum(a * z(a) for a, z in rules if a > 0)
    total_a  = sum(a        for a, _ in rules if a > 0)

    if total_a == 0:
        return 0, mH, mT

    hasil = round(total_az / total_a)
    return hasil, mH, mT


@app.route("/", methods=['GET', 'POST'])
def home():
    hasil_stok = None
    detail = None

    if request.method == 'POST':
        harga   = float(request.form.get('harga', 0))
        terjual = float(request.form.get('terjual', 0))
        hasil_stok, mH, mT = hitung_tsukamoto(harga, terjual)

        # Detail untuk ditampilkan di template (opsional)
        detail = {
            'harga_rendah':    round(mH['rendah'], 3),
            'harga_sedang':    round(mH['sedang'], 3),
            'harga_tinggi':    round(mH['tinggi'], 3),
            'terjual_sedikit': round(mT['sedikit'], 3),
            'terjual_sedang':  round(mT['sedang'],  3),
            'terjual_banyak':  round(mT['banyak'],  3),
        }

    return render_template('index.html', hasil=hasil_stok, detail=detail)


if __name__ == "__main__":
    app.run(debug=True)