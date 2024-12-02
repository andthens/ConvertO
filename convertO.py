import sys
import xml.etree.ElementTree as ET
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, 
    QPushButton, QLabel, QFileDialog
)
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt, QThread, Signal


def update_names(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        for component in root.findall(".//INTEGRATION_COMPONENT"):
            xml_tag = component.get("XML_TAG")
            if xml_tag:
                component.set("NAME", xml_tag)

            for field in component.findall(".//INTEGRATION_COMPONENT_FIELD"):
                field_xml_tag = field.get("XML_TAG")
                if field_xml_tag:
                    field.set("NAME", field_xml_tag)

        output_file = "updated_" + file_path.split('/')[-1]
        tree.write(output_file, encoding="UTF-8", xml_declaration=True)
        return f"Updated XML file saved as: {output_file}"
    except Exception as e:
        return f"Error: {str(e)}"


class UpdateThread(QThread):
    finished = Signal(str)

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path

    def run(self):
        result = update_names(self.file_path)
        self.finished.emit(result)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ConvertO")
        self.setFixedSize(600, 400)  
        self.setWindowFlags(Qt.FramelessWindowHint) 

        self.top_bar = self.create_top_bar()

        self.pages = QWidget()
        self.pages.setLayout(self.create_home_page())

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.top_bar, alignment=Qt.AlignTop)
        self.main_layout.addWidget(self.pages)

        container = QWidget()
        container.setLayout(self.main_layout)
        self.setCentralWidget(container)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #3B4252;
                color: #ECEFF4;
                background-image: url('icons/background.png');
                background-position: center;
                background-repeat: no-repeat;
            }
            QLabel {
                color: #ECEFF4;
                font-size: 14px;
            }
            QPushButton {
                background-color: #8fbcbb;
                color: #ECEFF4;
                padding: 15px 30px;
                border: none;
                border-radius: 25px;
            }
            QPushButton:hover {
                background-color: #5E81AC;
            }
            QPushButton:pressed {
                background-color: #8fbcbb;
            }
        """)

    def create_top_bar(self):
        top_bar = QHBoxLayout()

        logo_label = QLabel()
        logo_pixmap = QPixmap("icons/logo.png")
        logo_pixmap = logo_pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio) 
        logo_label.setPixmap(logo_pixmap)
        top_bar.addWidget(logo_label, alignment=Qt.AlignLeft)

        button_style = """
            QPushButton {
                color: #ECEFF4;
                border: none;
                background-color: transparent;
                font-size: 16px;
                font-weight: bold;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #4C566A;
                border-radius: 6px;
            }
        """

        minimize_button = QPushButton("−")  
        minimize_button.setFixedSize(40, 40)
        minimize_button.setStyleSheet(button_style)
        minimize_button.clicked.connect(self.showMinimized)

        close_button = QPushButton("✕")
        close_button.setFixedSize(40, 40)
        close_button.setStyleSheet("""
            QPushButton {
                color: #BF616A;
                border: none;
                background-color: transparent;
                font-size: 16px;
                font-weight: bold;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #4C566A;
                border-radius: 6px;
            }
        """)
        close_button.clicked.connect(self.close)

        top_bar.addStretch()
        top_bar.addWidget(minimize_button)
        top_bar.addWidget(close_button)

        top_bar_container = QWidget()
        top_bar_container.setLayout(top_bar)
        top_bar_container.setStyleSheet("background-color: transparent;") 

        return top_bar_container

    def create_home_page(self):
        layout = QVBoxLayout()

        #self.status_label = QLabel("Select a .sif file to update.")
        #self.status_label.setAlignment(Qt.AlignCenter)
        #self.status_label.setStyleSheet("font-weight: bold; font-size: 16px;") 

        upload_button = QPushButton("Upload File")
        upload_button.setStyleSheet("""
            QPushButton {
                background-color: #8fbcbb;
                color: #eceff4;
                font-size: 16px;
                font-weight: bold;
                padding: 15px 30px;
                border: none;
                border-radius: 25px;
            }
            QPushButton:hover {
                background-color: #5E81AC;
            }
            QPushButton:pressed {
                background-color: #4C566A;
            }
        """)
        upload_button.clicked.connect(self.upload_file)

        self.success_message = QLabel("")
        self.success_message.setAlignment(Qt.AlignCenter)
        self.success_message.setStyleSheet("font-weight: bold; color: #A3BE8C; font-size: 16px;")

        self.processing_label = QLabel("")
        self.processing_label.setAlignment(Qt.AlignCenter)
        self.processing_label.setStyleSheet("font-size: 16px; color: #ECEFF4;")

        layout.addStretch()
        #layout.addWidget(self.status_label)
        layout.addWidget(upload_button, alignment=Qt.AlignCenter)
        layout.addWidget(self.processing_label)
        layout.addWidget(self.success_message)
        layout.addStretch() 

        layout.setAlignment(Qt.AlignCenter)

        return layout

    def upload_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open SIF File", "", "SIF Files (*.sif);;All Files (*)"
        )
        if file_path:
            self.processing_label.setText("Processing... Please wait.")
            #self.status_label.setText("") 

            self.thread = UpdateThread(file_path)
            self.thread.finished.connect(self.on_update_finished)
            self.thread.start()

    def on_update_finished(self, result):
        self.processing_label.setText("")
        self.success_message.setText(result)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
