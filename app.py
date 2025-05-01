from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import random

app = Flask(__name__)

costo_apertura = 10
punti_sbusto = 100

punti_carte = {
    "Comune": 2,
    "Non Comune": 7,
    "Rara": 12,
    "Ultra Rara": 50
}

giocatore = {
    "punti": punti_sbusto,
    "collezione": []
}

def carica_carte():
        df = pd.read_csv("pokemon.csv")
        carte = []
        for _, row in df.iterrows():
            carte.append({
                "Nome": row["Nome"],
                "Rarità": row["Rarità"],
                "Attacco": row["Attacco"],
                "Difesa": row["Difesa"],
                "Valore_Punti": punti_carte.get(row["Rarità"])
            })
        return carte
        return []

carte_disponibili = carica_carte()

def seleziona_carta():
    numero_casuale = random.randint(1, 100)
    if 1 <= numero_casuale <= 70:
        rarita = "Comune"
    elif 71 <= numero_casuale <= 90:
        rarita = "Non Comune"
    elif 91 <= numero_casuale <= 99:
        rarita = "Rara"
    else:
        rarita = "Ultra Rara"

    carte_filtrate = [carta for carta in carte_disponibili if carta["Rarità"] == rarita]
    return random.choice(carte_filtrate)

@app.route("/")
def home():
    return render_template("index.html", punti=giocatore["punti"], collezione=giocatore["collezione"])

@app.route("/apri-pacchetto", methods=["POST"])
def sbusta():
    if giocatore["punti"] < costo_apertura:
        digli = "Non hai abbastanza punti sbusto per aprire un pacchetto."
        return render_template("index.html", punti=giocatore["punti"], collezione=giocatore["collezione"], digli=digli)

    giocatore["punti"] -= costo_apertura
    pacchetto = []

    for i in range(5):
        carta = seleziona_carta()
        if carta:
            pacchetto.append(carta)
            giocatore["punti"] += carta["Valore_Punti"]

    giocatore["collezione"].extend(pacchetto)
    digli = "In questo pacchetto hai trovato: " + ", ".join([carta["Nome"] for carta in pacchetto])
    return render_template("index.html", punti=giocatore["punti"], collezione=giocatore["collezione"], digli=digli)

@app.route("/salva-collezione", methods=["POST"])
def salva_collezione():
    df = pd.DataFrame(giocatore["collezione"])
    file = "collezione.csv"
    df.to_csv(file, index=False)
    digli = "Collezione salvata con successo nel file " + file
    return render_template("index.html", punti=giocatore["punti"], collezione=giocatore["collezione"], digli=digli)

if __name__ == "__main__":
    app.run(debug=True)