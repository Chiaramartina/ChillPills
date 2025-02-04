# Emotion Network Visualizer

Emotion Network Visualizer è un'applicazione per la visualizzazione interattiva di reti di emozioni, basata su PyQt5 e PyVis.

## Requisiti
Per eseguire questa applicazione, assicurati di avere i seguenti requisiti:

- Python 3.8+
- pip (Python Package Installer)

## Installazione
1. Clona il repository o scarica i file del progetto:
   ```bash
   git clone Chiaramartina/ChillPills
      
```
2. Crea ed attiva un ambiente virtuale (opzionale ma consigliato):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Su macOS/Linux
   venv\Scripts\activate  # Su Windows
   ```
3. Installa le dipendenze richieste:

   ```bash
   pip install -r requirements.txt
   ```

## Esecuzione
Per avviare l'applicazione, eseguire il seguente comando:
```bash
python main.py
```

L'applicazione avvierà una GUI in cui potrai selezionare emozioni e generare una rete interattiva.

## Struttura del Progetto
```
wordnet/
├── data/
│   ├── default_wordnet.json    # Database JSON delle emozioni
├── img/
│   ├── icon.png                  # Icona dell'applicazione
├── lib/                          # Librerie di supporto per la rete interattiva
│   ├── bindings/
│   ├── tom-select/
│   ├── vis-9.1.2/
├── view/                         # Componenti dell'interfaccia grafica
│   ├── emotion_view.py           # Interfaccia principale
│   ├── splash_view.py            # Splash screen iniziale
├── controller_model.py           # Controller principale
├── emotion_network.html          # File HTML generato per la rete
├── main.py                       # Punto di ingresso dell'applicazione
├── requirements.txt              # Elenco delle dipendenze
```

## Funzionalità
- **Splash Screen**: Interfaccia di benvenuto per l'utente.
- **Selezione delle Emozioni**: L'utente può selezionare emozioni da una lista.
- **Generazione della Rete**: Una rete di emozioni viene generata in un file HTML e visualizzata tramite PyQt5 WebEngine.

## Dipendenze
Le principali librerie utilizzate sono:
- **PyQt5**: Framework per GUI in Python
- **PyQtWebEngine**: Per l'integrazione di contenuti web nella GUI
- **pyvis**: Per la creazione della rete interattiva
- **QtMaterial**: Per applicare uno stile moderno all'interfaccia

Queste dipendenze sono elencate nel file `requirements.txt` e possono essere installate con `pip install -r requirements.txt`.

## Note
Se si verificano problemi con `PyQtWebEngine`, assicurati che sia compatibile con la versione di Python installata.

## Autori
- **Chiara Martina**
- **Marco Miozza**

## Contatti
Per segnalare bug o suggerimenti, contatta:
- marco.miozza@studio.unibo.it
- chiara.martina3@studio.unibo.it