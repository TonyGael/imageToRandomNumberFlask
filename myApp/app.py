from flask import Flask, request, render_template, redirect, url_for
from PIL import Image
import pytesseract
import re
import random
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'

# Ruta principal para cargar la imagen
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)

            # Procesar la imagen y extraer números
            image = Image.open(filename)
            text = pytesseract.image_to_string(image)
            numbers = re.findall(r'\b\d+\b', text)
            decimal_numbers = [int(number) for number in numbers]

            if decimal_numbers:
                selected_number = random.choice(decimal_numbers)
                return render_template('index.html', numbers=decimal_numbers, selected_number=selected_number)
            else:
                return render_template('index.html', message="No numbers found in the image.")

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)