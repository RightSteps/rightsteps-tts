import os
import json


class Settings:
    api_key: str
    piper_binary: str
    piper_model: str
    sample_rate: int
    channels: int
    bits_per_sample: int

    def __init__(self):
        self.api_key = os.environ['TTS_API_KEY']
        self.piper_binary = os.environ.get('PIPER_BINARY', '/opt/piper/piper')
        self.piper_model = os.environ.get('PIPER_MODEL', '/opt/piper/models/en_GB-cori-medium.onnx')
        self.channels = 1
        self.bits_per_sample = 16
        self.sample_rate = self._load_sample_rate()

    def _load_sample_rate(self) -> int:
        config_path = self.piper_model + '.json'
        try:
            with open(config_path) as f:
                data = json.load(f)
                return data.get('audio', {}).get('sample_rate', 22050)
        except Exception:
            return 22050


settings = Settings()
