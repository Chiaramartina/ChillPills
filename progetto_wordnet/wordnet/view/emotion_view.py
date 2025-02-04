import sys
from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QListWidget, QPushButton, QTextEdit, QLabel, QLineEdit,
    QMessageBox,
)
from PyQt5.QtWebEngineWidgets import QWebEngineView  # Per visualizzare il file HTML della rete
from PyQt5.QtCore import QUrl  # Per gestire i percorsi dei file
from PyQt5.QtGui import QIcon,QPalette, QColor
from pyvis.network import Network  # Per creare e gestire reti interattive


class EmotionAppView(QMainWindow):
    """
    Classe principale della finestra per la visualizzazione della rete di emozioni.
    Rappresenta la vista principale dell'applicazione e gestisce l'interfaccia utente.
    """
    def __init__(self, controller, model):
        """
        Inizializza la finestra principale con il layout, i widget e i collegamenti.

        :param controller: Riferimento al controller principale.
        :param model: Riferimento al modello contenente i dati delle emozioni.
        """
        super().__init__()
        self.controller = controller  # Collegamento al controller
        self.model = model  # Collegamento al modello

        # Configurazione della finestra principale
        self.setWindowTitle("Emotion Network Visualizer")
        self.setWindowIcon(QIcon("img/icon.png"))
        self.setGeometry(100, 100, 1400, 900)

        # --- Colonna sinistra ---
        # Lista delle emozioni (multi-selezione)
        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QListWidget.MultiSelection)
        self.list_widget.setStyleSheet("font-size: 24px; padding: 10px;")

        # Riempie la lista con le emozioni dal modello
        for e in self.model.emotions.keys():
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
            border: none;
        """)
        # Collega il pulsante al metodo nel controller
        self.plot_button.clicked.connect(self.controller.generate_selected_network)

        # Legenda per i colori e le relazioni
        self.legend = QTextEdit()
        self.legend.setReadOnly(True)  # Solo lettura
        self.legend.setHtml("""
        <b>Legenda:</b><br><br>
        <span style="color:#A7C957;">● Sinonimi </span><br><br>
        <span style="color:#BF3100;">● Contrari</span><br><br>
        <span style="color:#F5BB00;">● Iponimi </span><br><br>
        <span style="color:#1982C4;">● Iperonimi </span><br><br>
        <span style="color:#E2E2E2;">● Relazionati </span><br><br>
        """)
        self.legend.setFixedHeight(304)  # Altezza fissa
        self.legend.setStyleSheet("""
            font-size: 24px; 
            background-color: #2C2C3E; 
            color: #F0F0F0; 
            padding: 10px; 
            border-radius: 10px;
            border: none;
        """)

        # Layout per la colonna sinistra
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.list_widget, stretch=3)
        left_layout.addWidget(self.plot_button, stretch=2)
        left_layout.addWidget(self.legend, stretch=4)

        # --- Colonna destra ---
        # Barra di ricerca
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Cerca una parola...")
        self.search_input.setStyleSheet("font-size: 18px; padding: 6px; color: white;")

        self.search_button = QPushButton("Cerca")
        self.search_button.setFixedHeight(40)
        self.search_button.setStyleSheet("""
            font-size: 18px;
            background-color: #9D4EDD; 
            color: white; 
            border-radius: 8px; 
            padding: 8px;
            border: none;
        """)
        
        # Collega il pulsante al metodo di ricerca nel controller
        self.search_button.clicked.connect(self.controller.search_word)

        # Layout per la barra di ricerca
        search_layout = QHBoxLayout()
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)

        # Visualizzatore HTML per la rete
        self.web_view = QWebEngineView()

        # Area dei dettagli della rete
        self.details = QTextEdit()
        self.details.setReadOnly(True)  # Solo lettura
        self.details.setStyleSheet("""
            font-size: 22px; 
            line-height: 1.6; 
            background-color: #2C2C3E; 
            color: #F0F0F0; 
            padding: 10px; 
            border-radius: 10px;
            border: none;
        """)
        self.details.setHtml("<h2>Dettagli:</h2><br>")

        # Layout per la colonna destra
        right_layout = QVBoxLayout()
        right_layout.addLayout(search_layout)
        right_layout.addWidget(self.web_view, stretch=7)
        right_layout.addWidget(self.details, stretch=3)

        # Layout principale
        main_layout = QHBoxLayout()
        main_layout.addLayout(left_layout, stretch=1)
        main_layout.addLayout(right_layout, stretch=3)

        # Configura il layout della finestra
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)
        self.showMaximized()

    # --- Metodi per interagire con il controller e il modello ---
    def get_selected_emotions(self):
        """
        Restituisce le emozioni selezionate nella lista.
        :return: Lista di emozioni selezionate (in minuscolo).
        """
        return [item.text().lower() for item in self.list_widget.selectedItems()]

    def alert_no_emotions_selected(self):
        """
        Mostra un avviso se nessuna emozione è stata selezionata.
        """
        QMessageBox.information(self, "Info", "Nessuna emozione selezionata!")

    def set_details_html(self, html):
        """
        Imposta l'HTML dell'area dei dettagli.
        :param html: Stringa HTML da visualizzare.
        """
        self.details.setHtml(html)

    def load_html_in_view(self, path):
        """
        Carica l'HTML (della rete PyVis) nella QWebEngineView.
        :param path: Percorso del file HTML.
        """
        if isinstance(path, QUrl):
            self.web_view.setUrl(path)
        else:
            self.web_view.setUrl(QUrl.fromLocalFile(path))


    def get_search_text(self):
        """
        Restituisce il testo inserito nella barra di ricerca.
        :return: Testo della barra di ricerca (senza spazi iniziali o finali).
        """
        return self.search_input.text().strip()

    def alert_no_network(self):
        """
        Mostra un avviso se la rete non è stata generata.
        """
        QMessageBox.warning(self, "Attenzione", 
                            "Non esiste ancora una rete da cercare. Generala prima!")

    def highlight_word_in_view(self, word):
        """
        Esegue uno script JS per cercare e colorare il nodo corrispondente.
        :param word: Parola da evidenziare nella rete.
        """
        highlight_js = f"""
        var found = false;
        var target = '{word}'.toLowerCase();

        // Controlliamo tutti i nodi
        window.nodes.get().forEach(function(n) {{
            if (n.id.toLowerCase() === target) {{
                n.color = 'red';
                window.nodes.update(n);
                found = true;
            }}
        }});

        if (!found) {{
            window.network.fit();
            alert("La parola '{word}' non è presente nella rete corrente.");
        }}
        """
        # Esegue lo script JS nella pagina caricata
        self.web_view.page().runJavaScript(highlight_js)

    def patch_html_for_javascript_globals(self, html_content: str) -> str:
        """
        Inietta variabili globali nel file HTML per manipolare i nodi via JS.
        Questo rende accessibili 'nodes', 'edges' e 'network' a livello globale.

        :param html_content: Contenuto HTML originale.
        :return: Contenuto HTML modificato.
        """
        snippet_nodes = "var nodes = new vis.DataSet("
        replace_nodes = "var nodes = new vis.DataSet(\nwindow.nodes = nodes;\n"

        snippet_edges = "var edges = new vis.DataSet("
        replace_edges = "var edges = new vis.DataSet(\nwindow.edges = edges;\n"

        snippet_network = "var network = new vis.Network("
        replace_network = "var network = new vis.Network(\nwindow.network = network;\n"

        new_html = html_content
        new_html = new_html.replace(snippet_nodes, replace_nodes)
        new_html = new_html.replace(snippet_edges, replace_edges)
        new_html = new_html.replace(snippet_network, replace_network)

        return new_html
