import json
import os
from pathlib import Path
from typing import Optional

from cryptography.fernet import Fernet
import keyring


class ProviderStore:
    """Provider metadata store with keyring first and encrypted-file fallback.

    Metadata is stored in `providers.json` (non-secret fields).
    Secrets are stored using the OS keyring when available; otherwise they are
    encrypted and written to `providers.secrets.json` using a locally-generated
    Fernet key stored in `.aide-secrets.key`.
    """

    SERVICE = "aide"

    def __init__(self, storage_dir: Optional[Path] = None):
        self.storage_dir = Path(storage_dir) if storage_dir else Path(__file__).parent
        self.file = self.storage_dir / "providers.json"
        self.secrets_file = self.storage_dir / "providers.secrets.json"
        self.key_file = self.storage_dir / ".aide-secrets.key"
        self._ensure_files()

    def _ensure_files(self) -> None:
        if not self.file.exists():
            self._write_metadata({})
        if not self.secrets_file.exists():
            self._write_secrets({})
        if not self.key_file.exists():
            self.key_file.write_bytes(Fernet.generate_key())

    def _read_metadata(self) -> dict:
        try:
            return json.loads(self.file.read_text())
        except Exception:
            return {}

    def _write_metadata(self, data: dict) -> None:
        self.file.write_text(json.dumps(data, indent=2))

    def _read_secrets(self) -> dict:
        try:
            return json.loads(self.secrets_file.read_text())
        except Exception:
            return {}

    def _write_secrets(self, data: dict) -> None:
        self.secrets_file.write_text(json.dumps(data, indent=2))

    def _get_cipher(self) -> Fernet:
        key = os.getenv("AIDE_ENCRYPTION_KEY")
        if key:
            return Fernet(key.encode("utf-8"))
        return Fernet(self.key_file.read_bytes())

    def list_providers(self) -> dict:
        data = self._read_metadata()
        result = {}
        for name, meta in data.items():
            has_key = self._has_secret(name)
            result[name] = {**meta, "has_key": has_key}
        return result

    def _has_secret(self, name: str) -> bool:
        try:
            if keyring.get_password(self.SERVICE, name) is not None:
                return True
        except Exception:
            pass
        secrets = self._read_secrets()
        return name in secrets

    def save_provider(self, name: str, metadata: dict, api_key: Optional[str] = None) -> None:
        data = self._read_metadata()
        data[name] = metadata
        self._write_metadata(data)
        if api_key is None:
            return
        try:
            keyring.set_password(self.SERVICE, name, api_key)
        except Exception:
            secrets = self._read_secrets()
            cipher = self._get_cipher()
            secrets[name] = cipher.encrypt(api_key.encode("utf-8")).decode("utf-8")
            self._write_secrets(secrets)

    def get_provider(self, name: str) -> dict | None:
        data = self._read_metadata()
        meta = data.get(name)
        if not meta:
            return None
        key = None
        try:
            key = keyring.get_password(self.SERVICE, name)
        except Exception:
            key = None
        if key is None:
            secrets = self._read_secrets()
            if name in secrets:
                cipher = self._get_cipher()
                key = cipher.decrypt(secrets[name].encode("utf-8")).decode("utf-8")
        return {**meta, "api_key": key}

    def delete_provider(self, name: str) -> bool:
        data = self._read_metadata()
        if name in data:
            data.pop(name)
            self._write_metadata(data)
            try:
                keyring.delete_password(self.SERVICE, name)
            except Exception:
                pass
            secrets = self._read_secrets()
            if name in secrets:
                secrets.pop(name)
                self._write_secrets(secrets)
            return True
        return False
