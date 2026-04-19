import sounddevice as sd
import numpy as np
import wave
import os
import matplotlib.pyplot as plt
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

#  Paramètres 
DUREE     = 10        # secondes
CANAUX    = 1         # mono
NIVEAUX   = 256       # 8 bits = 256 niveaux
DOSSIER   = os.path.expanduser(os.getenv("OUTPUT_DIR", "./"))

#  Fonction d'enregistrement 
def enregistrer(fe, nom_fichier):
    print(f"\n>>> Enregistrement {nom_fichier} (Fe={fe} Hz, {DUREE}s)...")
    print("Wakhal ...!")

    # Enregistrement en float32
    audio = sd.rec(
        int(DUREE * fe),
        samplerate=fe,
        channels=CANAUX,
        dtype='float32'
    )
    sd.wait()  # attend la fin
    print("Enregistrement terminé.")

    # Quantification sur 256 niveaux (8 bits unsigned)
    # float32 est entre -1.0 et 1.0 on mappe sur 0..255
    audio_8bit = np.clip(audio, -1.0, 1.0)
    audio_8bit = ((audio_8bit + 1.0) / 2.0 * 255).astype(np.uint8)

    # Sauvegarde en WAV
    chemin = os.path.join(DOSSIER, nom_fichier)
    with wave.open(chemin, 'w') as f:
        f.setnchannels(CANAUX)
        f.setsampwidth(1)        # 1 octet = 8 bits
        f.setframerate(fe)
        f.writeframes(audio_8bit.tobytes())

    taille = os.path.getsize(chemin)
    print(f"Fichier sauvegardé : {chemin}")
    print(f"Taille réelle     : {taille} octets ({taille/1024:.1f} Ko)")
    print(f"Taille théorique  : {fe * 1 * 1 * DUREE} octets")

    return audio_8bit, fe, chemin

#  Fonction d'analyse visuelle 
def analyser(audio1, fe1, audio2, fe2):
    fig, axes = plt.subplots(2, 2, figsize=(12, 6))
    fig.suptitle("Comparaison Fe=8000Hz vs Fe=44100Hz (8 bits, Mono)", fontsize=13)

    for ax_row, audio, fe, label in zip(
        axes,
        [audio1, audio2],
        [fe1, fe2],
        ["Fe = 8000 Hz", "Fe = 44100 Hz"]
    ):
        t = np.linspace(0, DUREE, len(audio))

        # Forme d'onde
        ax_row[0].plot(t, audio, linewidth=0.5, color='steelblue')
        ax_row[0].set_title(f"Forme d'onde — {label}")
        ax_row[0].set_xlabel("Temps (s)")
        ax_row[0].set_ylabel("Amplitude (0-255)")

        # Spectre de fréquences
        spectre = np.abs(np.fft.rfft(audio.flatten()))
        freqs   = np.fft.rfftfreq(len(audio.flatten()), d=1/fe)
        ax_row[1].plot(freqs, spectre, linewidth=0.5, color='coral')
        ax_row[1].set_title(f"Spectre de fréquences — {label}")
        ax_row[1].set_xlabel("Fréquence (Hz)")
        ax_row[1].set_ylabel("Amplitude")
        ax_row[1].set_xlim(0, fe / 2)

    plt.tight_layout()
    plt.savefig(os.path.join(DOSSIER, "comparaison.png"), dpi=150)
    plt.show()
    print("\nGraphique sauvegardé : comparaison.png")

#  Main 
if __name__ == "__main__":
    os.makedirs(DOSSIER, exist_ok=True)

    # Enregistrement 1 — Fe = 8000 Hz
    input("\nAppuie sur ENTRÉE pour commencer l'enregistrement à 8000 Hz...")
    audio1, fe1, _ = enregistrer(8000, "voix_8000Hz.wav")

    # Enregistrement 2 — Fe = 44100 Hz
    input("\nAppuie sur ENTRÉE pour commencer l'enregistrement à 44100 Hz...")
    audio2, fe2, _ = enregistrer(44100, "voix_44100Hz.wav")

    # Analyse comparative
    print("\n Analyse comparative ")
    print(f"Fe=8000  Hz → taille théorique : {8000*1*1*10} octets = {8000*10/1024:.1f} Ko")
    print(f"Fe=44100 Hz → taille théorique : {44100*1*1*10} octets = {44100*10/1024:.1f} Ko")
    print(f"Rapport de taille : 44100/8000 = {44100/8000:.2f}x")

    analyser(audio1, fe1, audio2, fe2)
