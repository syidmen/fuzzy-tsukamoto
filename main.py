from flask import Flask, render_template, request

app = Flask(__name__)

def hitung_tsukamoto(harga, terjual):
    # --- 1. FUZZIFIKASI (Input) ---
    # Harga (Murah: 1-5 jt, Mahal: 5-10 jt)
    def harga_murah(x):
        if x <= 5: return 1
        if x >= 10: return 0
        return (10 - x) / (10 - 5)

    def harga_mahal(x):
        if x <= 5: return 0
        if x >= 10: return 1
        return (x - 5) / (10 - 5)

    # Terjual (Sedikit: 0-20 unit, Banyak: 20-50 unit)
    def terjual_sedikit(x):
        if x <= 20: return 1
        if x >= 50: return 0
        return (50 - x) / (50 - 20)

    def terjual_banyak(x):
        if x <= 20: return 0
        if x >= 50: return 1
        return (x - 20) / (50 - 20)

    # --- 2. RULE & INFERENSI (Output Mono) ---
    # Misal Output Stok: Berkurang (10-30), Bertambah (30-60)
    # R1: JIKA Harga Murah DAN Terjual Banyak, MAKA Stok Bertambah
    # R2: JIKA Harga Mahal DAN Terjual Sedikit, MAKA Stok Berkurang
    
    # Derajat Keanggotaan (Alpha Predikat)
    a1 = min(harga_murah(harga), terjual_banyak(terjual))
    a2 = min(harga_mahal(harga), terjual_sedikit(terjual))

    # Nilai Z (Invers output Tsukamoto)
    # Bertambah: z = 30 + (a * (60-30))
    # Berkurang: z = 30 - (a * (30-10))
    z1 = 30 + (a1 * 30)
    z2 = 30 - (a2 * 20)

    # --- 3. DEFUZZIFIKASI (Weighted Average) ---
    if (a1 + a2) == 0: return 0
    hasil = (a1 * z1 + a2 * z2) / (a1 + a2)
    return round(hasil)

@app.route("/", methods=['GET', 'POST'])
def home():
    hasil_stok = None
    if request.method == 'POST':
        harga = float(request.form.get('harga', 0))
        terjual = float(request.form.get('terjual', 0))
        hasil_stok = hitung_tsukamoto(harga, terjual)
        
    return render_template('index.html', hasil=hasil_stok)

if __name__ == "__main__":
    app.run(debug=True)