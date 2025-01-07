import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, 
                            QWidget, QTextEdit, QPushButton)
from PyQt5.QtCore import QThread, pyqtSignal
from egg_voice import EggVoiceTerminal

class VoiceThread(QThread):
    response_received = pyqtSignal(str)
    
    def __init__(self, terminal):
        super().__init__()
        self.terminal = terminal
        
    def run(self):
        user_input = self.terminal.listen()
        if user_input:
            response = self.terminal.send_to_egg(user_input)
            if response:
                self.response_received.emit(response)

class EggVoiceApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.terminal = EggVoiceTerminal()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Egg Voice Terminal")
        self.setGeometry(100, 100, 600, 400)
        
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()
        
        # Chat display
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        layout.addWidget(self.chat_display)
        
        # Listen button
        self.listen_btn = QPushButton("Speak to Egg")
        self.listen_btn.clicked.connect(self.start_listening)
        layout.addWidget(self.listen_btn)
        
        main_widget.setLayout(layout)
        
    def start_listening(self):
        self.listen_btn.setEnabled(False)
        self.chat_display.append("Listening...")
        
        self.voice_thread = VoiceThread(self.terminal)
        self.voice_thread.response_received.connect(self.show_response)
        self.voice_thread.finished.connect(lambda: self.listen_btn.setEnabled(True))
        self.voice_thread.start()
        
    def show_response(self, response):
        self.chat_display.append(f"Egg: {response}")
        self.terminal.speak(response)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EggVoiceApp()
    window.show()
    sys.exit(app.exec_())
