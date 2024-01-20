# app.py
from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)
data_dir = '/app/data'  # Percorso della directory dati nel contenitore

def carica_dati():
    file_path = os.path.join(data_dir, 'associazioni.json')
    try:
        with open(file_path, 'r') as file:
            dati = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        dati = {}
        salva_dati(dati)  # Crea il file se non esiste o è vuoto
    return dati

def salva_dati(dati):
    file_path = os.path.join(data_dir, 'associazioni.json')
    with open(file_path, 'w') as file:
        json.dump(dati, file)

@app.route('/')
def index():
    dati = carica_dati()
    return render_template('index.html', dati=dati)

@app.route('/associa', methods=['POST'])
def associa():
    numero_fattura = request.form['numero_fattura']
    numero_lotto = request.form['numero_lotto']

    dati = carica_dati()

    # Se la fattura è già presente, aggiungi il lotto, altrimenti crea una nuova entry
    if numero_fattura in dati:
        dati[numero_fattura] += f',{numero_lotto}'
    else:
        dati[numero_fattura] = numero_lotto

    salva_dati(dati)

    return redirect(url_for('index'))

@app.route('/cerca', methods=['GET'])
def cerca():
    numero_cercato = request.args.get('numero_cercato', '')
    
    dati = carica_dati()
    risultato_ricerca = []

    for numero_fattura, lotti in dati.items():
        lotti_split = lotti.split(',')
        for lotto in lotti_split:
            if numero_cercato.lower() in lotto.lower():
                risultato_ricerca.append({'numero_fattura': numero_fattura, 'numero_lotto': lotto})

    return render_template('cerca.html', numero_cercato=numero_cercato, risultato_ricerca=risultato_ricerca)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
