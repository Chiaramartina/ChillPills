# Importazione dei moduli e librerie necessarie
import sys
import os
import json

from PyQt5.QtWidgets import QFileDialog, QMessageBox  # Per dialoghi file e messaggi di avviso
from pyvis.network import Network  # Per la creazione di reti interattive
from view.splash_view import SplashScreenView  # Finestra di benvenuto (splash screen)
from view.emotion_view import EmotionAppView  # Finestra principale dell'applicazione


class MainController:
    """
    Classe principale che funge da controller per l'applicazione. Coordina il modello dei dati
    (EmotionModel) e le viste (SplashScreenView, EmotionAppView).
    """

    class EmotionModel:
        """
        Modello interno per gestire i dati delle emozioni. Carica e memorizza le emozioni 
        e le loro relazioni a partire da un file JSON.
        """
        def __init__(self):
            self.emotions = {}

        def load_from_json(self, file_path: str):
            """
            Carica il file JSON specificato e aggiorna il dizionario delle emozioni.

            :param file_path: Percorso al file JSON contenente i dati delle emozioni.
            :raises ValueError: Se il file JSON non contiene il formato atteso.
            """
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if "emozioni" not in data or not isinstance(data["emozioni"], dict):
                    raise ValueError("Il file JSON non contiene la chiave 'emozioni' valida.")
                self.emotions = data["emozioni"]

    def __init__(self, app):
        """
        Inizializza il controller principale e imposta il modello e le viste.

        :param app: Oggetto QApplication per la gestione dell'interfaccia grafica.
        """
        self.app = app
        self.model = MainController.EmotionModel()
        
        # Percorso predefinito al file JSON contenente i dati delle emozioni
        self.json_file = "data\\extended_emotions.json"

        # Creazione e visualizzazione dello splash screen
        self.splash_view = SplashScreenView(controller=self)
        self.splash_view.show()

        # Riferimento alla finestra principale (non creata all'inizio)
        self.emotion_view = None

    def close_app(self):
        """
        Chiude l'intera applicazione.
        """
        self.app.quit()

    def load_wordnet_file(self):
        """
        Permette all'utente di selezionare un file JSON e aggiorna i dati del modello.
        Mostra messaggi di errore in caso di file non valido.
        """
        file_name, _ = QFileDialog.getOpenFileName(
            self.splash_view,
            "Seleziona file WordNet",
            "",
            "JSON Files (*.json);;All Files (*)"
        )

        if file_name:
            try:
                self.model.load_from_json(file_name)
                # Salva il percorso del file caricato
                self.json_file = file_name
            except Exception as e:
                self.splash_view.show_error_message("Errore", f"Il file selezionato non è compatibile:\n{str(e)}")

    def start_app(self):
        """
        Avvia la finestra principale dell'applicazione e chiude lo splash screen.
        """
        try:
            # Carica i dati dal file JSON predefinito se non già caricati
            if not self.model.emotions:
                self.model.load_from_json(self.json_file)
        except Exception as e:
            self.splash_view.show_error_message("Errore", f"Impossibile caricare {self.json_file}:\n{str(e)}")
            return

        # Crea e visualizza la finestra principale
        self.emotion_view = EmotionAppView(controller=self, model=self.model)
        self.emotion_view.show()
        self.splash_view.close()

    def show_info(self):
        """
        Mostra le informazioni sull'applicazione in un messaggio modale.
        """
        info_text = (
            "Emotion Network Visualizer v1.0<br>"
            "Applicazione per la visualizzazione di una rete di emozioni.<br>"
            "Sviluppato da Chiara Martina & Marco Miozza<br><br>"
            "Contatti: marco.miozza@studio.unibo.it "
        )
        self.splash_view.show_info_message("Informazioni", info_text)

    def generate_selected_network(self):
        """
        Genera una rete interattiva basata sulle emozioni selezionate.
        La rete è salvata come file HTML e caricata nella vista principale.

        Funzionamento:
        - I nodi rappresentano emozioni.
        - Gli archi rappresentano relazioni come sinonimi, contrari, ecc.
        """
        if not self.emotion_view:
            return

        # Ottiene le emozioni selezionate dalla vista
        selected_emotions = self.emotion_view.get_selected_emotions()
        if not selected_emotions:
            self.emotion_view.alert_no_emotions_selected()
            return

        # Creazione della rete utilizzando PyVis
        net = Network(height="100%", width="100%", directed=False)
        net.set_options('''
        {
            "physics": { "enabled": true },
            "layout": { "improvedLayout": true },
            "interaction": { "hover": true }
        }
        ''')

        # Colori per i vari tipi di relazioni
        MAIN_COLOR = "#CDB4DB"
        SYN_COLOR = "#A7C957"
        ANT_COLOR = "#BF3100"
        HYPONYM_COLOR = "#F5BB00"
        HYPERNYM_COLOR = "#1982C4"
        RELATED_COLOR = "#E2E2E2"

        details_text = "<b>Dettagli delle emozioni selezionate:</b><br><br>"

        # Aggiunta di nodi e archi alla rete
        for emotion in selected_emotions:
            net.add_node(emotion, label=emotion.capitalize(), color=MAIN_COLOR)
            emotion_data = self.model.emotions.get(emotion, {})
            details_text += f"<b>{emotion.capitalize()}:</b> {emotion_data.get('details', 'N/A')}<br><br>"

            # Sinonimi
            for syn in emotion_data.get("synonyms", []):
                net.add_node(syn, label=syn.capitalize(), color=MAIN_COLOR)
                net.add_edge(emotion, syn, color=SYN_COLOR, width=3)

            # Contrari
            for ant in emotion_data.get("antonyms", []):
                net.add_node(ant, label=ant.capitalize(), color=MAIN_COLOR)
                net.add_edge(emotion, ant, color=ANT_COLOR, width=3)

            # Iponimi
            for hypo in emotion_data.get("hyponyms", []):
                net.add_node(hypo, label=hypo.capitalize(), color=MAIN_COLOR)
                net.add_edge(emotion, hypo, color=HYPONYM_COLOR, width=3)

            # Iperonimi
            for hyper in emotion_data.get("hypernyms", []):
                net.add_node(hyper, label=hyper.capitalize(), color=MAIN_COLOR)
                net.add_edge(emotion, hyper, color=HYPERNYM_COLOR, width=3)

            # Relazionati
            for rel in emotion_data.get("related", []):
                net.add_node(rel, label=rel.capitalize(), color=MAIN_COLOR)
                net.add_edge(emotion, rel, color=RELATED_COLOR, width=3)

        # Salva la rete in un file HTML
        net.save_graph("emotion_network.html")

        # Modifica e salva l'HTML per l'integrazione con PyQt
        with open("emotion_network.html", "r", encoding="utf-8") as f:
            html_content = f.read()

        html_content = self.emotion_view.patch_html_for_javascript_globals(html_content)
        html_content = html_content.replace("height:600px;", "height:100%;")

        custom_style = """
        <style>
        html, body {
            margin: 0;
            padding: 0;
            height: 100vh;
            overflow: hidden;
        }
        #mynetwork {
            width: 100% !important;
            height: calc(100vh - 10px) !important;
            background-color: white;
        }
        </style>
        """
        html_content = html_content.replace("<head>", "<head>\n" + custom_style + "\n")

        # Sovrascrive il file HTML modificato
        with open("emotion_network.html", "w", encoding="utf-8") as f:
            f.write(html_content)

        # Carica la rete nella vista
        full_path = os.path.join(os.getcwd(), "emotion_network.html")
        self.emotion_view.load_html_in_view(full_path)
        self.emotion_view.set_details_html(details_text)

    def search_word(self):
        """
        Evidenzia il nodo corrispondente alla parola cercata nella rete generata.
        """
        if not self.emotion_view:
            return

        word_to_search = self.emotion_view.get_search_text()
        if not word_to_search:
            QMessageBox.warning(self.emotion_view, "Attenzione", "Inserisci una parola da cercare!")
            return

        # Controlla se la rete è stata caricata
        current_url = self.emotion_view.web_view.url().toString()
        if not current_url.endswith("emotion_network.html"):
            self.emotion_view.alert_no_network()
            return

        # Esegui il codice JavaScript per evidenziare il nodo
        self.emotion_view.highlight_word_in_view(word_to_search)
