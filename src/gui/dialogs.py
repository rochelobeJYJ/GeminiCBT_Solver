from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QDialogButtonBox, QComboBox, QGroupBox)

# Available model presets
MODEL_PRESETS = [
    "gemini-2.5-flash",
    "gemini-3.0-flash",
]

DEFAULT_MODEL = "gemini-2.5-flash"

class ApiKeyDialog(QDialog):
    def __init__(self, parent=None, current_model: str = ""):
        super().__init__(parent)
        self.setWindowTitle("설정")
        self.setFixedSize(420, 280)
        
        layout = QVBoxLayout()
        layout.setSpacing(12)
        
        # --- API Key Section ---
        api_group = QGroupBox("API Key")
        api_layout = QVBoxLayout()
        
        instructions = QLabel("Gemini API Key를 입력해주세요:")
        self.key_input = QLineEdit()
        self.key_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        api_layout.addWidget(instructions)
        api_layout.addWidget(self.key_input)
        api_group.setLayout(api_layout)
        
        # --- Model Section ---
        model_group = QGroupBox("모델 선택")
        model_layout = QVBoxLayout()
        
        # Preset model combo box
        preset_row = QHBoxLayout()
        preset_label = QLabel("프리셋:")
        self.model_combo = QComboBox()
        self.model_combo.setEditable(False)
        for model in MODEL_PRESETS:
            self.model_combo.addItem(model)
        self.model_combo.addItem("직접 입력...")
        
        preset_row.addWidget(preset_label)
        preset_row.addWidget(self.model_combo, stretch=1)
        
        # Custom model input
        custom_row = QHBoxLayout()
        custom_label = QLabel("모델명:")
        self.custom_model_input = QLineEdit()
        self.custom_model_input.setPlaceholderText("예: gemini-2.5-flash-preview-05-20")
        self.custom_model_input.setEnabled(False)
        
        custom_row.addWidget(custom_label)
        custom_row.addWidget(self.custom_model_input, stretch=1)
        
        model_layout.addLayout(preset_row)
        model_layout.addLayout(custom_row)
        model_group.setLayout(model_layout)
        
        # Connect combo box change
        self.model_combo.currentIndexChanged.connect(self._on_model_combo_changed)
        
        # Set current model
        self._set_current_model(current_model)
        
        # --- Buttons ---
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        
        layout.addWidget(api_group)
        layout.addWidget(model_group)
        layout.addWidget(buttons)
        self.setLayout(layout)
    
    def _on_model_combo_changed(self, index):
        """Enable custom input only when '직접 입력...' is selected."""
        is_custom = (index == self.model_combo.count() - 1)
        self.custom_model_input.setEnabled(is_custom)
        if is_custom:
            self.custom_model_input.setFocus()
    
    def _set_current_model(self, model_name: str):
        """Set the dialog to show the current model."""
        if not model_name:
            model_name = DEFAULT_MODEL
        
        # Check if it's one of the presets
        preset_index = -1
        for i, preset in enumerate(MODEL_PRESETS):
            if preset == model_name:
                preset_index = i
                break
        
        if preset_index >= 0:
            self.model_combo.setCurrentIndex(preset_index)
        else:
            # It's a custom model
            self.model_combo.setCurrentIndex(self.model_combo.count() - 1)
            self.custom_model_input.setText(model_name)
            self.custom_model_input.setEnabled(True)

    def get_key(self):
        return self.key_input.text()
    
    def get_model(self) -> str:
        """Return the selected model name."""
        index = self.model_combo.currentIndex()
        if index == self.model_combo.count() - 1:
            # Custom input
            custom = self.custom_model_input.text().strip()
            return custom if custom else DEFAULT_MODEL
        else:
            return MODEL_PRESETS[index]
