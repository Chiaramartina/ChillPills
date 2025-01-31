import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget,
    QListWidget, QPushButton, QHBoxLayout, QTextEdit, QLabel,
    QGraphicsDropShadowEffect, QMessageBox,
    QFileDialog, QLineEdit
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QIcon
from qt_material import apply_stylesheet
from pyvis.network import Network

class SplashScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Emotion Network Visualizer")
        self.setWindowIcon(QIcon("img\\icon.png"))
        self.setStyleSheet("background-color: #121212; color: white;")
        
        self.setFixedSize(800, 500)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.json_file = "extended_emotions.json"

        # Layout principale
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Barra superiore con Close
        top_bar = QHBoxLayout()
        top_bar.setContentsMargins(0, 0, 0, 0)
        top_bar.setSpacing(0)

        close_button = QPushButton("✕")
        close_button.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: transparent;
                font-size: 18px;
                border: none;
                padding: 5px 10px;
            }
            QPushButton:hover {
                color: red;
                background-color: #333333;
            }
        """)
        close_button.setCursor(Qt.PointingHandCursor)
        close_button.clicked.connect(self.close_app)

        top_bar.addStretch()
        top_bar.addWidget(close_button)

        # Sfondo
        self.background_label = QLabel()
        self.background_label.setScaledContents(True)

        # Widget centrale semi-trasparente
        self.central_widget = QWidget()
        self.central_widget.setObjectName("central_widget")
        self.central_widget.setStyleSheet("""
            QWidget#central_widget {
                background-color: rgba(0, 0, 0, 150); 
                border-radius: 20px;
            }
        """)
        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setBlurRadius(20)
        shadow_effect.setOffset(0, 0)
        self.central_widget.setGraphicsEffect(shadow_effect)

        central_layout = QVBoxLayout(self.central_widget)
        central_layout.setContentsMargins(40, 40, 40, 40)
        central_layout.setSpacing(20)

        # Titolo
        self.title = QLabel("Emotion Network Visualizer")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font-size: 32px; font-weight: bold; color: #FFFFFF;")
        central_layout.addWidget(self.title)

        # Sottotitolo
        self.subtitle = QLabel("Esplora Wordnet")
        self.subtitle.setAlignment(Qt.AlignCenter)
        self.subtitle.setStyleSheet("font-size: 18px; color: #DDDDDD;")
        central_layout.addWidget(self.subtitle)

        # Layout pulsanti centrali
        buttons_layout = QHBoxLayout()

        # Pulsante Avvia
        self.start_button = QPushButton("Avvia")
        self.start_button.setStyleSheet("""
            QPushButton {
                font-size: 24px;
                background-color: #6200EE;
                color: white;
                padding: 15px 30px;
                border-radius: 25px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3700B3;
            }
        """)
        self.start_button.setCursor(Qt.PointingHandCursor)
        self.start_button.clicked.connect(self.start_app)
        buttons_layout.addWidget(self.start_button)

        # Pulsante Carica WordNet
        self.load_wordnet_button = QPushButton("Carica WordNet")
        self.load_wordnet_button.setStyleSheet("""
            QPushButton {
                font-size: 20px;
                background-color: #03DAC5;
                color: black;
                padding: 10px 20px;
                border-radius: 20px;
            }
            QPushButton:hover {
                background-color: #029C92;
            }
        """)
        self.load_wordnet_button.setCursor(Qt.PointingHandCursor)
        self.load_wordnet_button.clicked.connect(self.load_wordnet_file)
        buttons_layout.addWidget(self.load_wordnet_button)

        # Pulsante Info
        self.info_button = QPushButton("Info")
        self.info_button.setStyleSheet("""
            QPushButton {
                font-size: 20px;
                background-color: #BB86FC;
                color: #ffffff;
                padding: 10px 20px;
                border-radius: 20px;
            }
            QPushButton:hover {
                background-color: #8A60C9;
            }
        """)
        self.info_button.setCursor(Qt.PointingHandCursor)
        self.info_button.clicked.connect(self.show_info)
        buttons_layout.addWidget(self.info_button)

        central_layout.addLayout(buttons_layout)

        # Composizione finale
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)

        container_layout.addLayout(top_bar)
        container_layout.addWidget(self.background_label)

        self.background_label.setLayout(QVBoxLayout())
        self.background_label.layout().addWidget(self.central_widget, alignment=Qt.AlignCenter)

        main_layout.addWidget(container)
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        self.center_on_screen()
        self.show()

    def close_app(self):
        QApplication.quit()

    def center_on_screen(self):
        frame_gm = self.frameGeometry()
        screen = QApplication.primaryScreen().availableGeometry().center()
        frame_gm.moveCenter(screen)
        self.move(frame_gm.topLeft())

    def load_wordnet_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Seleziona file WordNet",
            "",
            "JSON Files (*.json);;All Files (*)"
        )
        
        if file_name:
            try:
                with open(file_name, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                if "emozioni" not in data or not isinstance(data["emozioni"], dict):
                    raise ValueError("Il file JSON non contiene la chiave 'emozioni' valida.")
                self.json_file = file_name
            except (json.JSONDecodeError, ValueError) as e:
                QMessageBox.critical(self, "Errore", f"Il file selezionato non è compatibile:\n{str(e)}")

    def start_app(self):
        self.main_window = EmotionApp(json_file=self.json_file)
        self.main_window.show()
        self.close()

    def show_info(self):
        info_text = (
            "Emotion Network Visualizer v1.0<br>"
            "Applicazione per la visualizzazione di una rete di emozioni.<br>"
            "Sviluppato da Chiara Martina & Marco Miozza<br><br>"
            "Contatti: marco.miozza@studio.unibo.it "
        )
        QMessageBox.information(self, "Informazioni", info_text)


class EmotionApp(QMainWindow):
    def __init__(self, json_file="extended_emotions.json"):
        super().__init__()
        self.setWindowTitle("Emotion Network Visualizer")
        self.setWindowIcon(QIcon("img\\icon.png"))
        self.setGeometry(100, 100, 1400, 900)

        with open(json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
            self.emotions = data["emozioni"]

        # --- Colonna sinistra ---
        # Lista delle emozioni
        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QListWidget.MultiSelection)
        self.list_widget.setStyleSheet("font-size: 24px; padding: 10px;")
        for e in self.emotions.keys():
            self.list_widget.addItem(e.capitalize())

        # Pulsante per generare la rete 
        self.plot_button = QPushButton("Genera Rete")
        self.plot_button.setFixedHeight(50)
        self.plot_button.setStyleSheet("""
            font-size: 18px; 
            background-color: #9D4EDD; 
            color: white; 
            border-radius: 10px; 
            padding: 10px;
        """)
        self.plot_button.clicked.connect(self.generate_selected_network)

        # Legenda
        self.legend = QTextEdit()
        self.legend.setReadOnly(True)
        self.legend.setHtml("""
        <b>Legenda:</b><br><br>
        <span style="color:#A7C957;">● Sinonimi </span><br><br>
        <span style="color:#BF3100;">● Contrari</span><br><br>
        <span style="color:#F5BB00;">● Iponimi </span><br><br>
        <span style="color:#1982C4;">● Iperonimi </span><br><br>
        <span style="color:#E2E2E2;">● Relazionati </span><br><br>
        """)
        self.legend.setFixedHeight(304)
        self.legend.setStyleSheet("""
            font-size: 24px; 
            background-color: #2C2C3E; 
            color: #F0F0F0; 
            padding: 10px; 
            border-radius: 10px;
        """)

        left_layout = QVBoxLayout()
        left_layout.addWidget(self.list_widget, stretch=3)
        left_layout.addWidget(self.plot_button, stretch=2)
        left_layout.addWidget(self.legend, stretch=4)

        # --- Colonna destra ---
        # Barra di ricerca
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Cerca una parola...")
        self.search_input.setStyleSheet("font-size: 18px; padding: 6px;")

        self.search_button = QPushButton("Cerca")
        self.search_button.setFixedHeight(40)
        self.search_button.setStyleSheet("""
            font-size: 18px; 
            background-color: #03DAC6; 
            color: black; 
            border-radius: 8px; 
            padding: 8px;
        """)
        self.search_button.clicked.connect(self.search_word)

        search_layout = QHBoxLayout()
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)

        # Visualizzatore per PyVis
        self.web_view = QWebEngineView()

        # Area dettagli
        self.details = QTextEdit()
        self.details.setReadOnly(True)
        self.details.setStyleSheet("""
            font-size: 22px; 
            line-height: 1.6; 
            background-color: #2C2C3E; 
            color: #F0F0F0; 
            padding: 10px; 
            border-radius: 10px;
        """)
        self.details.setHtml("<b>Dettagli:</b><br>")

        right_layout = QVBoxLayout()
        right_layout.addLayout(search_layout)
        right_layout.addWidget(self.web_view, stretch=7)
        right_layout.addWidget(self.details, stretch=3)

        # Layout principale
        main_layout = QHBoxLayout()
        main_layout.addLayout(left_layout, stretch=1)
        main_layout.addLayout(right_layout, stretch=3)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)
        self.showMaximized()

        # NOTA: Non generiamo la rete di default
        # (self.generate_selected_network() verrà chiamato solo se l'utente lo decide)

    def generate_selected_network(self):
        """
        Genera una rete PyVis basata sulle emozioni selezionate.
        La rete è poi caricata nella QWebEngineView.
        """
        selected_emotions = [item.text().lower() for item in self.list_widget.selectedItems()]
        if not selected_emotions:
            QMessageBox.information(self, "Info", "Nessuna emozione selezionata!")
            return

        net = Network(height="100%", width="100%", directed=False)
        net.set_options('''
        {
            "physics": { "enabled": true },
            "layout": { "improvedLayout": true },
            "interaction": { "hover": true }
        }
        ''')

        # Colori
        MAIN_COLOR = "#CDB4DB"
        SYN_COLOR = "#A7C957"
        ANT_COLOR = "#BF3100"
        HYPONYM_COLOR = "#F5BB00"
        HYPERNYM_COLOR = "#1982C4"
        RELATED_COLOR = "#E2E2E2"

        details_text = "<b>Dettagli delle emozioni selezionate:</b><br><br>"

        for emotion in selected_emotions:
            net.add_node(emotion, label=emotion.capitalize(), color=MAIN_COLOR)
            details_text += f"<b>{emotion.capitalize()}:</b> {self.emotions[emotion].get('details', 'N/A')}<br><br>"

            for syn in self.emotions[emotion].get("synonyms", []):
                net.add_node(syn, label=syn.capitalize(), color=MAIN_COLOR)
                net.add_edge(emotion, syn, color=SYN_COLOR, width=3)

            for ant in self.emotions[emotion].get("antonyms", []):
                net.add_node(ant, label=ant.capitalize(), color=MAIN_COLOR)
                net.add_edge(emotion, ant, color=ANT_COLOR, width=3)

            for hypo in self.emotions[emotion].get("hyponyms", []):
                net.add_node(hypo, label=hypo.capitalize(), color=MAIN_COLOR)
                net.add_edge(emotion, hypo, color=HYPONYM_COLOR, width=3)

            for hyper in self.emotions[emotion].get("hypernyms", []):
                net.add_node(hyper, label=hyper.capitalize(), color=MAIN_COLOR)
                net.add_edge(emotion, hyper, color=HYPERNYM_COLOR, width=3)

            for rel in self.emotions[emotion].get("related", []):
                net.add_node(rel, label=rel.capitalize(), color=MAIN_COLOR)
                net.add_edge(emotion, rel, color=RELATED_COLOR, width=3)

        # Salviamo la rete
        net.save_graph("emotion_network.html")

        # Patch: iniettiamo variabili globali nel JS
        with open("emotion_network.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        html_content = self.patch_html_for_javascript_globals(html_content)
        # Rimuoviamo l'altezza fissa e adattiamo
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

        # Sovrascrivi il file HTML
        with open("emotion_network.html", "w", encoding="utf-8") as f:
            f.write(html_content)

        # Carica in QWebEngineView
        self.web_view.setUrl(QUrl.fromLocalFile(sys.path[0] + "/emotion_network.html"))
        self.details.setHtml(details_text)

    def patch_html_for_javascript_globals(self, html_content: str) -> str:
        """
        Inietta `window.nodes = nodes; window.edges = edges; window.network = network;`
        così da poter richiamare 'nodes', 'edges' e 'network' con runJavaScript.
        """
        # Sostituiamo le righe in cui PyVis crea 'nodes' e 'edges'
        # con versioni che rendono disponibili tali oggetti in window.
        # Cerchiamo i punti in cui compaiono:
        #   var nodes = new vis.DataSet([
        #   var edges = new vis.DataSet([
        snippet_nodes = "var nodes = new vis.DataSet("
        replace_nodes = "var nodes = new vis.DataSet(\nwindow.nodes = nodes;\n"

        snippet_edges = "var edges = new vis.DataSet("
        replace_edges = "var edges = new vis.DataSet(\nwindow.edges = edges;\n"

        # Per la variabile network
        snippet_network = "var network = new vis.Network("
        replace_network = "var network = new vis.Network(\nwindow.network = network;\n"

        new_html = html_content
        new_html = new_html.replace(snippet_nodes, replace_nodes)
        new_html = new_html.replace(snippet_edges, replace_edges)
        new_html = new_html.replace(snippet_network, replace_network)

        return new_html

    def search_word(self):
        """
        Non rigeneriamo la rete.
        Eseguiamo uno script JS per cercare la parola e cambiare il colore del nodo.
        """
        word_to_search = self.search_input.text().strip()
        if not word_to_search:
            QMessageBox.warning(self, "Attenzione", "Inserisci una parola da cercare!")
            return

        # Controlliamo se la pagina è stata caricata almeno una volta.
        # (Altrimenti, se l'utente non ha ancora generato la rete, non c'è nulla da modificare)
        if not self.web_view.url().toString().endswith("emotion_network.html"):
            QMessageBox.warning(self, "Attenzione", 
                                "Non esiste ancora una rete da cercare. Generala prima!")
            return

        # JavaScript per evidenziare il nodo col 'color' scelto (es. rosso).
        highlight_js = f"""
        var found = false;
        var target = '{word_to_search}'.toLowerCase();

        // Controlliamo tutti i nodi
        window.nodes.get().forEach(function(n) {{
            if (n.id.toLowerCase() === target) {{
                
                n.color = 'orange';
                window.nodes.update(n);
                found = true;
            }}
        }});

        if (!found) {{
            // Centra la vista su tutti i nodi, così se la rete è grande si vede la parola
            window.network.fit();
           alert("La parola '{word_to_search}' non è presente nella rete corrente.");
        }}
        """
        # Eseguiamo lo script
        self.web_view.page().runJavaScript(highlight_js)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("img\\icon.png"))
    apply_stylesheet(app, theme="dark_teal.xml")

    splash = SplashScreen()
    splash.show()
    sys.exit(app.exec_())
