import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, request
from main import hitung_tsukamoto

app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    error  = None
    if request.method == 'POST':
        try:
            unit  = float(request.form.get('unit', 0))
            harga = float(request.form.get('harga', 0))
            if unit < 0 or harga < 0:
                raise ValueError("Nilai tidak boleh negatif")
            result = hitung_tsukamoto(unit, harga)
        except (ValueError, ZeroDivisionError) as e:
            error = str(e)
    return render_template('index.html', result=result, error=error,
                           prev_unit=request.form.get('unit', ''),
                           prev_harga=request.form.get('harga', ''))