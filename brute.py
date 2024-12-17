import time
import random
import string
from difflib import SequenceMatcher

try:
    import speech_recognition as sr
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False

# Pfad zur von uns generierten sentences.txt
SENTENCE_FILE = r"C:\Users\Raphael\Desktop\aktuelles casting\sentences.txt"

def load_sentences(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines

def categorize_sentences(sentences):
    # Kategorisierung nach Wortanzahl
    difficulty_buckets = {i: [] for i in range(1, 11)}
    
    for s in sentences:
        word_count = len(s.split())
        
        if word_count < 3 or word_count > 20:
            continue
        
        if word_count <= 4:
            diff = 1
        elif word_count <= 6:
            diff = 2
        elif word_count <= 8:
            diff = 3
        elif word_count <= 10:
            diff = 4
        elif word_count <= 12:
            diff = 5
        elif word_count <= 14:
            diff = 6
        elif word_count <= 16:
            diff = 7
        elif word_count <= 18:
            diff = 8
        elif word_count == 19:
            diff = 9
        elif word_count == 20:
            diff = 10
        
        difficulty_buckets[diff].append(s)
    
    return difficulty_buckets

def get_audio_input():
    if not AUDIO_AVAILABLE:
        return None
    r = sr.Recognizer()
    r.pause_threshold = 1.5
    r.energy_threshold = 200
    
    with sr.Microphone() as source:
        print("Sprich jetzt deine Antwort ein (sag 'exit' um zu stoppen):")
        audio = r.listen(source, timeout=10)  
    try:
        text = r.recognize_google(audio, language="de-DE")
        return text
    except sr.UnknownValueError:
        print("Audio konnte nicht verstanden werden.")
    except sr.RequestError:
        print("Konnte nicht auf den Google Service zugreifen.")
    return None

def main():
    difficulty = 1
    max_difficulty = 10
    
    if not AUDIO_AVAILABLE:
        print("Keine Audiounterstützung vorhanden. Bitte SpeechRecognition installieren.")
        return

    all_sentences = load_sentences(SENTENCE_FILE)
    difficulty_buckets = categorize_sentences(all_sentences)

    total_sentences = sum(len(b) for b in difficulty_buckets.values())
    if total_sentences == 0:
        print("Es sind keine passenden Sätze in der Datei vorhanden.")
        return

    for d in range(1, 11):
        if len(difficulty_buckets[d]) == 0:
            print(f"Warnung: Keine Sätze für Schwierigkeit {d} gefunden!")

    print("Willkommen zu deinem Auswendiglern-Training!")
    print("Schwierigkeitsgrad:", difficulty, "(max:", max_difficulty, ")")
    print("Drücke STRG+C oder sage 'exit', um abzubrechen.")

    while True:
        possible_sentences = difficulty_buckets[difficulty]
        fallback_diff = difficulty
        while fallback_diff > 1 and len(possible_sentences) == 0:
            fallback_diff -= 1
            possible_sentences = difficulty_buckets[fallback_diff]

        if len(possible_sentences) == 0:
            print("Es sind keine geeigneten Sätze für deine Schwierigkeitsstufe (oder niedriger) vorhanden.")
            break
        
        current_text = random.choice(possible_sentences)
        
        print("\nMerke dir den folgenden Text (Schwierigkeit {}):".format(difficulty))
        print("----------------------------------------------------")
        print(current_text)
        print("----------------------------------------------------")

        memorize_time = 12
        time.sleep(memorize_time - 3)
        for i in range(3, 0, -1):
            print(f"{i}...")
            time.sleep(1)
        
        for _ in range(50):
            print()

        print("Bitte gib den gemerkten Text jetzt möglichst exakt wieder.")
        answer = get_audio_input()
        if answer is None:
            print("Keine Antwort erkannt, versuche es erneut.")
            continue

        if answer.strip().lower() == "exit":
            print("Beende das Programm. Bis zum nächsten Mal!")
            break

        original_stripped = current_text.strip().rstrip(".").lower()
        answer_stripped = answer.strip().rstrip(".").lower()

        similarity = SequenceMatcher(None, original_stripped, answer_stripped).ratio()
        if similarity > 0.9:
            print("Perfekt wiedergegeben!")
            if difficulty < max_difficulty:
                difficulty += 1
                print("Schwierigkeit erhöht auf", difficulty)
            else:
                print("Du hast bereits die maximale Schwierigkeit erreicht.")
            time.sleep(3)
        else:
            print("Das war nicht exakt richtig.")
            print("Original: ", current_text)
            print("Deine Antwort: ", answer)
            if difficulty > 1:
                difficulty -= 1
                print("Schwierigkeit verringert auf", difficulty)
            else:
                print("Schwierigkeit bleibt auf dem minimalen Wert.")
            print("Nimm dir kurz Zeit, um durchzuatmen, bevor es weitergeht...")
            time.sleep(10)

if __name__ == "__main__":
    main()
