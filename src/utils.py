import os
import json
import sys
from pathlib import Path
from cryptography.fernet import Fernet # type: ignore

def get_app_data_path():
    """Returns the path to the AppData folder for storing config."""
    if sys.platform == "win32":
        base_path = os.getenv('APPDATA')
        if not base_path:
            base_path = Path.home()
    else:
        base_path = Path.home()
    
    app_dir = Path(base_path) / "GeminiCBT_Solver"
    return app_dir

DATA_DIR = get_app_data_path()
CONFIG_FILE = DATA_DIR / "config.json"
KEY_FILE = DATA_DIR / ".key"

class ConfigManager:
    def __init__(self):
        self._ensure_data_dir()
        self._ensure_key()
        self.cipher_suite = Fernet(self._load_key())

    def _ensure_data_dir(self):
        if not DATA_DIR.exists():
            DATA_DIR.mkdir(parents=True, exist_ok=True)

    def _ensure_key(self):
        if not KEY_FILE.exists():
            key = Fernet.generate_key()
            with open(KEY_FILE, "wb") as key_file:
                key_file.write(key)

    def _load_key(self):
        return open(KEY_FILE, "rb").read()

    def _load_config(self) -> dict:
        if not CONFIG_FILE.exists():
            return {}
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except:
            return {}

    def _save_config(self, config: dict):
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f)

    def save_api_key(self, api_key: str):
        config = self._load_config()
        encrypted_key = self.cipher_suite.encrypt(api_key.encode())
        config["api_key"] = encrypted_key.decode()
        self._save_config(config)

    def load_api_key(self) -> str:
        config = self._load_config()
        encrypted_key = config.get("api_key")
        if encrypted_key:
            try:
                return self.cipher_suite.decrypt(encrypted_key.encode()).decode()
            except:
                return None
        return None

    def save_model(self, model_name: str):
        config = self._load_config()
        config["model"] = model_name
        self._save_config(config)

    def load_model(self) -> str:
        config = self._load_config()
        return config.get("model", "")
