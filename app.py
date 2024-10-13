import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QWidget
import requests

class ChatApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Chat App')
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.text_edit = QTextEdit(self)
        self.layout.addWidget(self.text_edit)

        self.input_line = QLineEdit(self)
        self.input_line.returnPressed.connect(self.send_message)
        self.layout.addWidget(self.input_line)

        self.send_button = QPushButton('Send', self)
        self.send_button.clicked.connect(self.send_message)
        self.layout.addWidget(self.send_button)

        self.central_widget.setLayout(self.layout)

    def send_message(self):
        user_input = self.input_line.text()
        self.display_message(f'You: {user_input}')

        bot_response = self.get_api_response(user_input)
        self.display_message(f'Bot: {bot_response}')

        self.input_line.clear()

    def display_message(self, message):
        current_text = self.text_edit.toPlainText()
        self.text_edit.setPlainText(f'{current_text}\n{message}')
        self.text_edit.verticalScrollBar().setValue(self.text_edit.verticalScrollBar().maximum())

    def get_api_response(self, user_input):
    # Replace 'your_api_key_here' with your actual Hugging Face API key
        api_key = "xyz"
        endpoint = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-v0.1"

        headers = {"Authorization": f"Bearer {api_key}"}
        payload = {"inputs": user_input}

        response = requests.post(endpoint, headers=headers, json=payload)

        if response.status_code == 200:
            try:
                response_json = response.json()
                generated_text = response_json[0]["generated_text"] if isinstance(response_json, list) else response_json.get("generated_text")
                return generated_text
            except (ValueError, KeyError):
                return "Error parsing the Hugging Face API response"
        else:
            return "Error communicating with the Hugging Face API"

if __name__ == '__main__':
    app = QApplication(sys.argv)
    chat_app = ChatApp()
    chat_app.show()
    sys.exit(app.exec_())
