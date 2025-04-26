from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import random

app = Flask(__name__)

costo_apertura = 10
punti_sbusto = 100

carte_prob = {
    "Comune": 0.7,
    "Non Comune": 0.2,
    "Rara": 0.09,
    "Ultra Rara": 0.01
}

punti_carte = {
    "Comune": 1,
    "Non Comune": 5,
    "Rara": 10,
    "Ultra Rara": 50
}

carte = [
    {"Nome": "Bulbasaur", "Generazione": 1, "Rarità": "Non Comune", "Attacco": 14, "Difesa": 64, "Valore_Punti": 3},
    {"Nome": "Charmander", "Generazione": 1, "Rarità": "Comune", "Attacco": 49, "Difesa": 30, "Valore_Punti": 1},
    {"Nome": "Squirtle", "Generazione": 1, "Rarità": "Comune", "Attacco": 37, "Difesa": 70, "Valore_Punti": 1},
    {"Nome": "Pikachu", "Generazione": 1, "Rarità": "Rara", "Attacco": 67, "Difesa": 56, "Valore_Punti": 6},
    {"Nome": "Eevee", "Generazione": 1, "Rarità": "Comune", "Attacco": 98, "Difesa": 29, "Valore_Punti": 1},
    {"Nome": "Snorlax", "Generazione": 1, "Rarità": "Comune", "Attacco": 16, "Difesa": 70, "Valore_Punti": 1},
    {"Nome": "Gengar", "Generazione": 1, "Rarità": "Non Comune", "Attacco": 80, "Difesa": 36, "Valore_Punti": 3},
    {"Nome": "Dragonite", "Generazione": 1, "Rarità": "Non Comune", "Attacco": 59, "Difesa": 12, "Valore_Punti": 3},
    {"Nome": "Mewtwo", "Generazione": 1, "Rarità": "Comune", "Attacco": 70, "Difesa": 69, "Valore_Punti": 1},
    {"Nome": "Charizard", "Generazione": 1, "Rarità": "Comune", "Attacco": 30, "Difesa": 88, "Valore_Punti": 1},
    {"Nome": "Chikorita", "Generazione": 2, "Rarità": "Comune", "Attacco": 79, "Difesa": 29, "Valore_Punti": 1},
    {"Nome": "Cyndaquil", "Generazione": 2, "Rarità": "Non Comune", "Attacco": 41, "Difesa": 90, "Valore_Punti": 3},
    {"Nome": "Totodile", "Generazione": 2, "Rarità": "Comune", "Attacco": 79, "Difesa": 82, "Valore_Punti": 1},
    {"Nome": "Togepi", "Generazione": 2, "Rarità": "Rara", "Attacco": 72, "Difesa": 72, "Valore_Punti": 6},
    {"Nome": "Ampharos", "Generazione": 2, "Rarità": "Rara", "Attacco": 40, "Difesa": 76, "Valore_Punti": 6},
    {"Nome": "Scizor", "Generazione": 2, "Rarità": "Comune", "Attacco": 18, "Difesa": 66, "Valore_Punti": 1},
    {"Nome": "Umbreon", "Generazione": 2, "Rarità": "Non Comune", "Attacco": 22, "Difesa": 11, "Valore_Punti": 3},
    {"Nome": "Espeon", "Generazione": 2, "Rarità": "Comune", "Attacco": 25, "Difesa": 42, "Valore_Punti": 1},
    {"Nome": "Tyranitar", "Generazione": 2, "Rarità": "Comune", "Attacco": 44, "Difesa": 36, "Valore_Punti": 1},
    {"Nome": "Suicune", "Generazione": 2, "Rarità": "Non Comune", "Attacco": 40, "Difesa": 56, "Valore_Punti": 3},
    {"Nome": "Treecko", "Generazione": 3, "Rarità": "Comune", "Attacco": 67, "Difesa": 39, "Valore_Punti": 1},
    {"Nome": "Torchic", "Generazione": 3, "Rarità": "Comune", "Attacco": 66, "Difesa": 66, "Valore_Punti": 1},
    {"Nome": "Mudkip", "Generazione": 3, "Rarità": "Comune", "Attacco": 26, "Difesa": 45, "Valore_Punti": 1},
    {"Nome": "Gardevoir", "Generazione": 3, "Rarità": "Non Comune", "Attacco": 27, "Difesa": 76, "Valore_Punti": 3},
    {"Nome": "Aggron", "Generazione": 3, "Rarità": "Comune", "Attacco": 93, "Difesa": 63, "Valore_Punti": 1},
    {"Nome": "Salamence", "Generazione": 3, "Rarità": "Non Comune", "Attacco": 29, "Difesa": 91, "Valore_Punti": 3},
    {"Nome": "Metagross", "Generazione": 3, "Rarità": "Comune", "Attacco": 73, "Difesa": 63, "Valore_Punti": 1},
    {"Nome": "Latias", "Generazione": 3, "Rarità": "Comune", "Attacco": 57, "Difesa": 65, "Valore_Punti": 1},
    {"Nome": "Latios", "Generazione": 3, "Rarità": "Rara", "Attacco": 11, "Difesa": 92, "Valore_Punti": 6},
    {"Nome": "Rayquaza", "Generazione": 3, "Rarità": "Comune", "Attacco": 78, "Difesa": 67, "Valore_Punti": 1},
    {"Nome": "Turtwig", "Generazione": 4, "Rarità": "Non Comune", "Attacco": 22, "Difesa": 71, "Valore_Punti": 3},
    {"Nome": "Chimchar", "Generazione": 4, "Rarità": "Comune", "Attacco": 17, "Difesa": 82, "Valore_Punti": 1},
    {"Nome": "Piplup", "Generazione": 4, "Rarità": "Non Comune", "Attacco": 28, "Difesa": 45, "Valore_Punti": 3},
    {"Nome": "Lucario", "Generazione": 4, "Rarità": "Comune", "Attacco": 86, "Difesa": 93, "Valore_Punti": 1},
    {"Nome": "Garchomp", "Generazione": 4, "Rarità": "Rara", "Attacco": 70, "Difesa": 63, "Valore_Punti": 6},
    {"Nome": "Togekiss", "Generazione": 4, "Rarità": "Comune", "Attacco": 26, "Difesa": 10, "Valore_Punti": 1},
    {"Nome": "Electivire", "Generazione": 4, "Rarità": "Comune", "Attacco": 41, "Difesa": 85, "Valore_Punti": 1},
    {"Nome": "Magmortar", "Generazione": 4, "Rarità": "Rara", "Attacco": 13, "Difesa": 29, "Valore_Punti": 6},
    {"Nome": "Darkrai", "Generazione": 4, "Rarità": "Rara", "Attacco": 97, "Difesa": 52, "Valore_Punti": 6},
    {"Nome": "Arceus", "Generazione": 4, "Rarità": "Comune", "Attacco": 22, "Difesa": 84, "Valore_Punti": 1},
]

giocatore = {
    "punti": punti_sbusto,
    "collezione": []
}

def seleziona_carta():
    carta = random.choice(carte)
    return carta

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
        pacchetto.append(carta)
        giocatore["punti"] += carta["Valore_Punti"]

    giocatore["collezione"].extend(pacchetto)
    digli = "In questo pacchetto hai trovato: "
    for carta in pacchetto:
        print(carta["Nome"] + " (Rarità: " + carta["Rarità"] + ", Attacco: " + str(carta["Attacco"]) + ", Difesa: " + str(carta["Difesa"]) + ")")
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