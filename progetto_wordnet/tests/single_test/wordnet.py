import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget,
    QListWidget, QPushButton, QHBoxLayout, QTextEdit, QLabel
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

        # Layout principale
        layout = QVBoxLayout()

        # Titolo
        self.title = QLabel("Emotion Network Visualizer")
        self.title.setStyleSheet("font-size: 32px; font-weight: bold; text-align: center;")
        self.title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title)

        # Pulsante Avvia
        self.start_button = QPushButton("Avvia")
        self.start_button.setStyleSheet("""
            QPushButton {
                font-size: 20px;
                background-color: #6200EE;
                color: white;
                padding: 10px 20px;
                border-radius: 20px;
            }
            QPushButton:hover {
                background-color: #3700B3;
            }
        """)
        self.start_button.clicked.connect(self.start_app)
        layout.addWidget(self.start_button, alignment=Qt.AlignCenter)

        # Container centrale
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.showMaximized()

    def start_app(self):
        self.main_window = EmotionApp()
        self.main_window.show()
        self.close()


class EmotionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Emotion Network Visualizer")
        self.setWindowIcon(QIcon("img\\icon.png"))
        self.setGeometry(100, 100, 1400, 900)

        # Carica i dati dal file JSON
        json_file = "extended_emotions.json"
        with open(json_file, 'r') as file:
            data = json.load(file)
            self.emotions = data["emozioni"]

        # Lista delle emozioni
        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QListWidget.MultiSelection)
        self.list_widget.setStyleSheet("font-size: 24px; padding: 10px;")
        for emotion in self.emotions.keys():
            self.list_widget.addItem(emotion.capitalize())

        # Pulsante per generare grafico
        self.plot_button = QPushButton("Genera Rete")
        self.plot_button.setFixedHeight(50)
        self.plot_button.setStyleSheet("font-size: 18px; background-color: #6200EE; color: white; border-radius: 10px; padding: 10px;")
        self.plot_button.clicked.connect(self.generate_network)

        # Visualizzatore web per grafico
        self.web_view = QWebEngineView()

        # Dettagli emozioni selezionate
        self.details = QTextEdit()
        self.details.setReadOnly(True)
        self.details.setStyleSheet("font-size: 22px; line-height: 1.6; background-color: #121212; color: #FFFFFF; padding: 10px; border-radius: 10px;")
        self.details.setHtml("<b>Dettagli delle emozioni selezionate:</b><br>")

        # Legenda
        legend_text = """
        <b>Legenda:</b><br><br>
        <span style="color:#4E77B6;">● Emozioni principali</span><br><br>
        <span style="color:#A8E6CF;">● Sinonimi </span><br><br>
        <span style="color:#FF8B94;">● Contrari</span><br><br>
        <span style="color:#FFD3B6;">● Iponimi </span><br><br>
        <span style="color:#D4B2D8;">● Iperonimi </span><br><br>
        <span style="color:#E2E2E2;">● Relazioni correlate </span>
        """
        self.legend = QTextEdit()
        self.legend.setReadOnly(True)
        self.legend.setHtml(legend_text)
        self.legend.setFixedHeight(304)
        self.legend.setStyleSheet("font-size: 24px; background-color: #2C2C3E; color: #F0F0F0; padding: 10px; border-radius: 10px;")

        # Layout della colonna sinistra
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.list_widget, stretch=3)
        left_layout.addWidget(self.plot_button, stretch=2)
        left_layout.addWidget(self.legend, stretch=4)

        # Layout della colonna destra
        right_layout = QVBoxLayout()
        right_layout.addWidget(self.web_view, stretch=7)
        right_layout.addWidget(self.details, stretch=3)

        # Layout principale orizzontale
        main_layout = QHBoxLayout()
        main_layout.addLayout(left_layout, stretch=1)
        main_layout.addLayout(right_layout, stretch=3)

        # Imposta il layout principale
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)
        self.showMaximized()

    def generate_network(self):
        # Recupera le emozioni selezionate
        selected_emotions = [item.text().lower() for item in self.list_widget.selectedItems()]
        if not selected_emotions:
            return

        # Crea un oggetto Network (pyvis)
        net = Network(height="600px", width="100%", directed=False)
        net.set_options('''
        {
          "physics": { "enabled": true },
          "layout": { "improvedLayout": true },
          "interaction": { "hover": true }
        }
        ''')

        details_text = "<b>Dettagli delle emozioni selezionate:</b><br><br>"

        MAIN_COLOR = "#BDE0FE"      # Emozioni principali (scuro)
        SYN_COLOR = "#A8E6CF"       # Sinonimi
        ANT_COLOR = "#FF8B94"       # Contrari
        HYPONYM_COLOR = "#FFD3B6"   # Iponimi
        HYPERNYM_COLOR = "#D4B2D8"  # Iperonimi
        RELATED_COLOR = "#E2E2E2"   # Relazioni correlate

        for emotion in selected_emotions:
            # Nodo principale: colore scuro
            net.add_node(
                emotion,
                label=emotion.capitalize(),
                color=MAIN_COLOR
            )

            # Dettagli testuali
            details_text += (
                f"<b>{emotion.capitalize()}:</b> "
                f"{self.emotions[emotion].get('details', 'N/A')}<br><br>"
            )

            # SINONIMI - colore pastello
            for synonym in self.emotions[emotion].get("synonyms", []):
                net.add_node(synonym, label=synonym.capitalize(), color=MAIN_COLOR)
                net.add_edge(emotion, synonym, color=SYN_COLOR, width=3)

            # CONTRARI - colore pastello
            for antonym in self.emotions[emotion].get("antonyms", []):
                net.add_node(antonym, label=antonym.capitalize(), color=MAIN_COLOR)
                net.add_edge(emotion, antonym, color=ANT_COLOR, width=3)

            # IPONIMI - colore pastello
            for hyponym in self.emotions[emotion].get("hyponyms", []):
                net.add_node(hyponym, label=hyponym.capitalize(), color=MAIN_COLOR)
                net.add_edge(emotion, hyponym, color=HYPONYM_COLOR, width=3)

            # IPERONIMI - colore pastello
            for hypernym in self.emotions[emotion].get("hypernyms", []):
                net.add_node(hypernym, label=hypernym.capitalize(), color=MAIN_COLOR)
                net.add_edge(emotion, hypernym, color=HYPERNYM_COLOR, width=3)

            # RELAZIONI CORRELATE - colore pastello
            for related in self.emotions[emotion].get("related", []):
                net.add_node(related, label=related.capitalize(), color=MAIN_COLOR)
                net.add_edge(emotion, related, color=RELATED_COLOR, width=3)

        # Aggiorna i dettagli in GUI
        self.details.setHtml(details_text)

        # Salva il file HTML
        net.save_graph("emotion_network.html")

        # Per iniettare un background chiaro o scuro al div della rete:
        with open("emotion_network.html", "r", encoding="utf-8") as f:
            html_content = f.read()
            
        html_content = html_content.replace(
            '<div id="mynetwork"',
            '<div id="mynetwork" style="background-color: white;"'
        )

        with open("emotion_network.html", "w", encoding="utf-8") as f:
            f.write(html_content)

        # Visualizza il file nel QWebEngineView
        self.web_view.setUrl(QUrl.fromLocalFile(sys.path[0] + "/emotion_network.html"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("img\\icon.png"))
    apply_stylesheet(app, theme="dark_teal.xml")

    splash = SplashScreen()
    splash.show()
    sys.exit(app.exec_())
