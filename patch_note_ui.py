import sys
import os
import subprocess
import locale

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel,
    QTextEdit, QMessageBox, QComboBox, QProgressBar, QHBoxLayout
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QUrl
from PyQt6.QtGui import QDesktopServices, QTextCharFormat, QColor, QIcon


class WorkerThread(QThread):
    """Thread pour exécuter main.py sans bloquer l'UI."""
    update_log = pyqtSignal(str)
    progress = pyqtSignal(int)
    finished = pyqtSignal(bool)

    def __init__(self, file_path, system):
        super().__init__()
        self.file_path = file_path
        self.system = system

    def run(self):
        """Exécute main.py et envoie les logs et la progression."""
        process = subprocess.Popen(
            ["python", "main.py", self.file_path, self.system],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding=locale.getpreferredencoding()  # 🔥 Auto-détection de l'encodage Windows
        )

        total_steps = 6  # Nombre d'étapes du pipeline (estimation)
        step_count = 0

        for line in process.stdout:
            self.update_log.emit(line.strip())
            if "Exécution" in line:
                step_count += 1
                progress_value = int((step_count / total_steps) * 100)
                self.progress.emit(progress_value)

        process.stdout.close()
        process.wait()
        self.finished.emit(process.returncode == 0)


class PatchNoteUI(QWidget):
    """Interface graphique améliorée pour l'analyse des patch notes."""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Initialise l'interface graphique."""
        self.setWindowTitle("Patch Notes Analyzer")
        self.setGeometry(100, 100, 700, 500)
        self.setStyleSheet("""
            QWidget {
                background-color: #f4f4f4;
                font-size: 14px;
                font-family: Arial, sans-serif;
            }
            QPushButton {
                background-color: #0078D7;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #005A9E;
            }
            QTextEdit {
                background-color: white;
                border: 1px solid #ccc;
                padding: 10px;
                font-size: 14px;
            }
            QProgressBar {
                border: 1px solid #aaa;
                text-align: center;
                background: white;
                height: 20px;
                border-radius: 5px;
            }
            QProgressBar::chunk {
                background-color: #0078D7;
                border-radius: 5px;
            }
            QLabel {
                font-size: 14px;
                margin-bottom: 5px;
            }
            QComboBox {
                padding: 5px;
                font-size: 14px;
            }
        """)

        layout = QVBoxLayout()

        # Sélection du système
        self.label_system = QLabel("Choisissez un système :", self)
        layout.addWidget(self.label_system)

        self.system_selector = QComboBox(self)
        self.system_selector.addItems(["Sciforma", "BC"])
        layout.addWidget(self.system_selector)

        # Bouton sélection fichier
        self.btn_select_file = QPushButton("Choisir un fichier HTML", self)
        self.btn_select_file.setIcon(QIcon("icons/open-file.png"))  # Ajout d'une icône
        self.btn_select_file.clicked.connect(self.select_file)
        layout.addWidget(self.btn_select_file)

        # Label affichage du fichier sélectionné
        self.label_file = QLabel("Aucun fichier sélectionné", self)
        layout.addWidget(self.label_file)

        # Bouton Exécution du pipeline
        self.btn_run = QPushButton("Lancer l'analyse", self)
        self.btn_run.setIcon(QIcon("icons/run.png"))  # Ajout d'une icône
        self.btn_run.setEnabled(False)
        self.btn_run.clicked.connect(self.run_pipeline)
        layout.addWidget(self.btn_run)

        # Barre de progression
        self.progress = QProgressBar(self)
        self.progress.setMinimum(0)
        self.progress.setMaximum(100)
        self.progress.setValue(0)
        layout.addWidget(self.progress)

        # Zone de logs
        self.text_logs = QTextEdit(self)
        self.text_logs.setReadOnly(True)
        layout.addWidget(self.text_logs)

        # Bouton Ouvrir le fichier Master
        self.btn_open_master = QPushButton("Ouvrir le fichier Master", self)
        self.btn_open_master.setIcon(QIcon("icons/open.png"))  # Ajout d'une icône
        self.btn_open_master.setEnabled(False)
        self.btn_open_master.clicked.connect(self.open_master_file)
        layout.addWidget(self.btn_open_master)

        self.setLayout(layout)
        self.filepath = None
        self.master_filename = None

    def select_file(self):
        """Ouvre un explorateur pour sélectionner un fichier HTML."""
        file, _ = QFileDialog.getOpenFileName(self, "Sélectionner un fichier HTML", "", "Fichiers HTML (*.html)")
        if file:
            self.filepath = file
            self.label_file.setText(os.path.basename(file))
            self.btn_run.setEnabled(True)

    def run_pipeline(self):
        """Exécute main.py avec le fichier HTML sélectionné et le système choisi."""
        if not self.filepath:
            QMessageBox.critical(self, "Erreur", "Veuillez sélectionner un fichier HTML.")
            return

        self.text_logs.clear()
        self.progress.setValue(0)

        system = self.system_selector.currentText()
        self.text_logs.append(f"[INFO] Lancement de l'analyse pour : {self.filepath} (Système: {system})")

        base_name = os.path.splitext(os.path.basename(self.filepath))[0]
        self.master_filename = f"{base_name}_Master.xlsx"

        # Désactiver les boutons pendant l'exécution
        self.btn_run.setEnabled(False)
        self.btn_open_master.setEnabled(False)

        # Lancer le traitement dans un thread séparé
        self.worker_thread = WorkerThread(self.filepath, system)
        self.worker_thread.update_log.connect(self.append_log)
        self.worker_thread.progress.connect(self.progress.setValue)
        self.worker_thread.finished.connect(self.pipeline_finished)
        self.worker_thread.start()

    def append_log(self, message):
        """Ajoute un message aux logs avec coloration selon le type."""
        fmt = QTextCharFormat()
        if "[ERREUR]" in message or "erreur" in message.lower():
            fmt.setForeground(QColor("red"))
        elif "[SUCCÈS]" in message or "succès" in message.lower():
            fmt.setForeground(QColor("green"))
        else:
            fmt.setForeground(QColor("black"))

        self.text_logs.setCurrentCharFormat(fmt)
        self.text_logs.append(message)

    def pipeline_finished(self, success):
        """Active le bouton pour ouvrir le fichier Master après exécution."""
        self.btn_run.setEnabled(True)
        if success:
            self.text_logs.append("\n[SUCCÈS] Analyse terminée !")
            QMessageBox.information(self, "Succès", "Analyse terminée ! Le fichier Master a été généré.")
            self.btn_open_master.setEnabled(True)
        else:
            self.text_logs.append("\n[ERREUR] Une erreur est survenue.")
            QMessageBox.critical(self, "Erreur", "Une erreur est survenue pendant l'exécution.")

    def open_master_file(self):
        """Ouvre le fichier Master généré."""
        if self.master_filename and os.path.exists(self.master_filename):
            QDesktopServices.openUrl(QUrl.fromLocalFile(self.master_filename))
        else:
            QMessageBox.critical(self, "Erreur", "Fichier Master introuvable.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PatchNoteUI()
    window.show()
    sys.exit(app.exec())
