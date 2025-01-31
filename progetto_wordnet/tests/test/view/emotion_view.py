# emotion_view.py
import sys
from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QListWidget, QPushButton, QTextEdit, QLabel, QLineEdit,
    QMessageBox
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon
from pyvis.network import Network


class EmotionAppView(QMainWindow):
    def __init__(self, controller, model):
        super().__init__()
        self.controller = controller
        self.model = model

        self.setWindowTitle("Emotion Network Visualizer")
        self.setWindowIcon(QIcon("img/icon.png"))
        self.setGeometry(100, 100, 1400, 900)

        # Colonna sinistra
        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QListWidget.MultiSelection)
        self.list_widget.setStyleSheet("font-size: 24px; padding: 10px;")

        # Riempi lista con le emozioni presenti nel Model
        for e in self.model.emotions.keys():
            self.list_widget.addItem(e.capitalize())

        self.plot_button = QPushButton("Genera Rete")
        self.plot_button.setFixedHeight(50)
        self.plot_button.setStyleSheet("""
            font-size: 18px; 
            background-color: #9D4EDD; 
            color: white; 
            border-radius: 10px; 
            padding: 10px;
        """)
        self.plot_button.clicked.connect(self.controller.generate_selected_network)

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

        # Colonna destra
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
        self.search_button.clicked.connect(self.controller.search_word)

        search_layout = QHBoxLayout()
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)

        self.web_view = QWebEngineView()

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

        main_layout = QHBoxLayout()
        main_layout.addLayout(left_layout, stretch=1)
        main_layout.addLayout(right_layout, stretch=3)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)
        self.showMaximized()

    def get_selected_emotions(self):
        return [item.text().lower() for item in self.list_widget.selectedItems()]

    def alert_no_emotions_selected(self):
        QMessageBox.information(self, "Info", "Nessuna emozione selezionata!")

    def set_details_html(self, html):
        self.details.setHtml(html)

    def load_html_in_view(self, path):
        """
        Carica l'HTML (della rete PyVis) nella QWebEngineView.
        """
        self.web_view.setUrl(QUrl.fromLocalFile(path))

    def get_search_text(self):
        return self.search_input.text().strip()

    def alert_no_network(self):
        QMessageBox.warning(self, "Attenzione", 
                            "Non esiste ancora una rete da cercare. Generala prima!")

    def highlight_word_in_view(self, word):
        """
        Esegue uno script JS per cercare e colorare il nodo corrispondente.
        """
        highlight_js = f"""
        var found = false;
        var target = '{word}'.toLowerCase();

        // Controlliamo tutti i nodi
        window.nodes.get().forEach(function(n) {{
            if (n.id.toLowerCase() === target) {{
                n.color = 'orange';
                window.nodes.update(n);
                found = true;
            }}
        }});

        if (!found) {{
            window.network.fit();
            alert("La parola '{word}' non è presente nella rete corrente.");
        }}
        """
        self.web_view.page().runJavaScript(highlight_js)

    def patch_html_for_javascript_globals(self, html_content: str) -> str:
        """
        Inietta variabili globali nel file HTML per manipolare i nodi via JS.
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
