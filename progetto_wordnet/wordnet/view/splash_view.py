# splash_view.py
import sys
from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget, QHBoxLayout,
    QPushButton, QLabel, QGraphicsDropShadowEffect, QFileDialog,
    QMessageBox, QApplication
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon


class SplashScreenView(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller  # riferimento al Controller
        self.setWindowTitle("Emotion Network Visualizer")
        self.setWindowIcon(QIcon("img/icon.png"))
        self.setStyleSheet("background-color: #121212; color: white;")

        self.setFixedSize(800, 500)
        # Rimuove la barra del titolo (stile splash)
        self.setWindowFlags(Qt.FramelessWindowHint)

        # Layout principale
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Barra superiore con pulsante Close
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

    def center_on_screen(self):
        """
        Centra la finestra sullo schermo principale.
        """
        frame_gm = self.frameGeometry()
        screen_center = QApplication.primaryScreen().availableGeometry().center()
        frame_gm.moveCenter(screen_center)
        self.move(frame_gm.topLeft())

    # -------------------
    # Metodi collegati ai pulsanti,
    # ciascuno delega l'azione al Controller
    # -------------------

    def close_app(self):
        self.controller.close_app()

    def load_wordnet_file(self):
        self.controller.load_wordnet_file()

    def start_app(self):
        self.controller.start_app()

    def show_info(self):
        self.controller.show_info()

    # -------------------
    # Metodi di utilità: la View può mostrare messaggi modali
    # -------------------
    def show_error_message(self, titolo, messaggio):
        QMessageBox.critical(self, titolo, messaggio)

    def show_info_message(self, titolo, messaggio):
        QMessageBox.information(self, titolo, messaggio)
