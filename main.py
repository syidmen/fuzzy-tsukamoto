from flask import Flask, render_template, request

app = Flask(__name__)

def fuzzifikasi_unit(x):
    if x <= 100:
        sedikit = 1.0
    elif x <= 200:
        sedikit = (200 - x) / 100
    else:
        sedikit = 0.0

    if x <= 150 or x >= 500:
        sedang = 0.0
    elif x <= 350:
        sedang = (x - 150) / 200
    else:
        sedang = (500 - x) / 150

    if x <= 500:
        banyak = 0.0
    elif x < 600:
        banyak = (x - 500) / 100
    else:
        banyak = 1.0

    return round(sedikit, 4), round(sedang, 4), round(banyak, 4)


def fuzzifikasi_harga(y):
    if y <= 1_000_000:
        murah = 1.0
    elif y < 3_000_000:
        murah = (3_000_000 - y) / 2_000_000
    else:
        murah = 0.0

    if y <= 1_000_000 or y >= 10_000_000:
        sedang = 0.0
    elif y <= 6_500_000:
        sedang = (y - 1_000_000) / 5_500_000
    else:
        sedang = (10_000_000 - y) / 3_500_000

    if y <= 8_000_000:
        mahal = 0.0
    elif y < 15_000_000:
        mahal = (y - 8_000_000) / 7_000_000
    else:
        mahal = 1.0

    return round(murah, 4), round(sedang, 4), round(mahal, 4)


RULES = [
    ('R1', 'sedikit', 'murah',  'berkurang'),
    ('R2', 'sedikit', 'sedang', 'berkurang'),
    ('R3', 'sedikit', 'mahal',  'berkurang'),
    ('R4', 'sedang',  'murah',  'bertambah'),
    ('R5', 'sedang',  'sedang', 'berkurang'),
    ('R6', 'sedang',  'mahal',  'berkurang'),
    ('R7', 'banyak',  'murah',  'bertambah'),
    ('R8', 'banyak',  'sedang', 'bertambah'),
    ('R9', 'banyak',  'mahal',  'bertambah'),
]

RULE_DESCRIPTIONS = {
    'R1': 'Sedikit AND Murah → Berkurang',
    'R2': 'Sedikit AND Sedang → Berkurang',
    'R3': 'Sedikit AND Mahal → Berkurang',
    'R4': 'Sedang AND Murah → Bertambah',
    'R5': 'Sedang AND Sedang → Berkurang',
    'R6': 'Sedang AND Mahal → Berkurang',
    'R7': 'Banyak AND Murah → Bertambah',
    'R8': 'Banyak AND Sedang → Bertambah',
    'R9': 'Banyak AND Mahal → Bertambah',
}


def hitung_tsukamoto(unit, harga):
    mu_sedikit, mu_sedang_u, mu_banyak = fuzzifikasi_unit(unit)
    mu_murah, mu_sedang_h, mu_mahal    = fuzzifikasi_harga(harga)

    mu_unit  = {'sedikit': mu_sedikit, 'sedang': mu_sedang_u, 'banyak': mu_banyak}
    mu_harga = {'murah': mu_murah,     'sedang': mu_sedang_h, 'mahal': mu_mahal}

    rule_detail = []
    for nama, u_lbl, h_lbl, out_lbl in RULES:
        alpha = round(min(mu_unit[u_lbl], mu_harga[h_lbl]), 4)
        if out_lbl == 'berkurang':
            z = round(100 - 80 * alpha, 4)
            fungsi = 'z = 100 − 80α'
        else:
            z = round(20 + 80 * alpha, 4)
            fungsi = 'z = 20 + 80α'

        rule_detail.append({
            'nama':      nama,
            'deskripsi': RULE_DESCRIPTIONS[nama],
            'u_lbl':     u_lbl.capitalize(),
            'h_lbl':     h_lbl.capitalize(),
            'out_lbl':   out_lbl.capitalize(),
            'mu_u':      mu_unit[u_lbl],
            'mu_h':      mu_harga[h_lbl],
            'alpha':     alpha,
            'z':         z,
            'fungsi':    fungsi,
            'alpha_z':   round(alpha * z, 4),
            'aktif':     alpha > 0,
        })

    sum_az = round(sum(r['alpha_z'] for r in rule_detail), 4)
    sum_a  = round(sum(r['alpha']   for r in rule_detail), 4)
    z_star = round(sum_az / sum_a, 4) if sum_a > 0 else 0.0

    keputusan  = 'Bertambah' if z_star > 60 else 'Berkurang'
    keterangan = ('Sangat Bertambah' if z_star > 80
                  else 'Cukup Bertambah' if z_star > 60
                  else 'Cukup Berkurang' if z_star > 40
                  else 'Sangat Berkurang')

    # ── RENTANG GRAFIK ────────────────────────────────────────────────────────
    # Ubah nilai di bawah ini untuk menyesuaikan rentang sumbu X tiap grafik.
    #
    # Grafik Unit HP:
    #   range(N+1) menentukan jumlah titik; dikalikan STEP untuk nilai x-nya.
    #   Contoh saat ini: step=10, range(101) → x dari 0 hingga 1000 unit
    UNIT_STEP  = 10       # <-- ubah step unit HP di sini
    UNIT_MAX_N = 101      # <-- ubah jumlah titik (max = UNIT_STEP * (N-1))
    #
    # Grafik Harga:
    #   Contoh saat ini: step=500.000, range(61) → x dari 0 hingga Rp 30.000.000
    HARGA_STEP  = 500_000  # <-- ubah step harga di sini
    HARGA_MAX_N = 61       # <-- ubah jumlah titik (max = HARGA_STEP * (N-1))
    #
    # Grafik Output (z):
    #   Rentang output tetap 0–100 sesuai fungsi Tsukamoto (tidak perlu diubah)
    # ──────────────────────────────────────────────────────────────────────────

    unit_pts  = [i * UNIT_STEP  for i in range(UNIT_MAX_N)]
    harga_pts = [i * HARGA_STEP for i in range(HARGA_MAX_N)]
    output_pts = list(range(20, 101))

    sc, sdc, bc, mc, shc, mlc = [], [], [], [], [], []
    for xp in unit_pts:
        s, sd, b = fuzzifikasi_unit(xp)
        sc.append(s); sdc.append(sd); bc.append(b)
    for yp in harga_pts:
        m, sh, ml = fuzzifikasi_harga(yp)
        mc.append(m); shc.append(sh); mlc.append(ml)

    out_berkurang, out_bertambah = [], []
    for z in output_pts:
        out_berkurang.append(round((100 - z) / 80, 4))
        out_bertambah.append(round((z - 20) / 80, 4))

    return {
        'unit':        unit,
        'harga':       harga,
        'harga_fmt':   f"Rp {int(harga):,}".replace(',', '.'),
        'mu_sedikit':  mu_sedikit,
        'mu_sedang_u': mu_sedang_u,
        'mu_banyak':   mu_banyak,
        'mu_murah':    mu_murah,
        'mu_sedang_h': mu_sedang_h,
        'mu_mahal':    mu_mahal,
        'rules':       rule_detail,
        'sum_az':      sum_az,
        'sum_a':       sum_a,
        'z_star':      z_star,
        'keputusan':   keputusan,
        'keterangan':  keterangan,
        'chart_unit_labels':  unit_pts,
        'chart_unit_sedikit': sc,
        'chart_unit_sedang':  sdc,
        'chart_unit_banyak':  bc,
        'input_unit_val':     unit,
        'chart_harga_labels': [round(p / 1_000_000, 1) for p in harga_pts],
        'chart_harga_murah':  mc,
        'chart_harga_sedang': shc,
        'chart_harga_mahal':  mlc,
        'input_harga_val':    round(harga / 1_000_000, 2),
        'chart_output_labels':    output_pts,
        'chart_output_berkurang': out_berkurang,
        'chart_output_bertambah': out_bertambah,
        'input_output_val':       z_star,
    }


@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    error  = None
    if request.method == 'POST':
        try:
            unit  = float(request.form.get('unit', 0))
            harga = float(request.form.get('harga', 0))
            if unit < 1 or unit > 1000:
                raise ValueError("Unit HP harus antara 1 – 1.000.")
            if harga < 100_000 or harga > 20_000_000:
                raise ValueError("Harga HP harus antara Rp 100.000 – Rp 20.000.000.")
            result = hitung_tsukamoto(unit, harga)
        except (ValueError, ZeroDivisionError) as e:
            error = str(e)

    return render_template('index.html', result=result, error=error,
                           prev_unit=request.form.get('unit', ''),
                           prev_harga=request.form.get('harga', ''))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)