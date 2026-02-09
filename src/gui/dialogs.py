from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QLabel, 
    QLineEdit, QDialogButtonBox)

class ApiKeyDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("API 설정")
        self.setFixedSize(400, 150)
        
        layout = QVBoxLayout()
        
        instructions = QLabel("Gemini API Key를 입력해주세요:")
        self.key_input = QLineEdit()
        self.key_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        
        layout.addWidget(instructions)
        layout.addWidget(self.key_input)
        layout.addWidget(buttons)
        self.setLayout(layout)

    def get_key(self):
        return self.key_input.text()
