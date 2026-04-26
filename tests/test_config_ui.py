import importlib
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


class FakeApiKeyManager:
    def __init__(self, values=None):
        self.values = dict(values or {})

    def get_api_key(self, key):
        return self.values.get(key, "")

    def set_api_key(self, key, value):
        self.values[key] = value


class ConfigUITest(unittest.TestCase):
    def load_module_in_temp_cwd(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        old_cwd = os.getcwd()
        os.chdir(self._tmp.name)
        self.addCleanup(os.chdir, old_cwd)
        for module_name in [
            "gui.ui_tab_config",
            "shortGPT.config.api_db",
            "shortGPT.database.db_document",
        ]:
            sys.modules.pop(module_name, None)
        return importlib.import_module("gui.ui_tab_config")

    def test_config_reload_values_reflect_keys_saved_after_startup(self):
        module = self.load_module_in_temp_cwd()
        fake_manager = FakeApiKeyManager()

        with patch.object(module, "ApiKeyManager", return_value=fake_manager):
            ui = module.ConfigUI()

        ui.save_keys("sk-after-start", "https://openai.example/v1", "", "", "")

        updates = ui.load_config_values()

        self.assertEqual(updates[0]["value"], ui._masked_value("sk-after-start"))
        self.assertEqual(updates[1]["value"], "https://openai.example/v1")


if __name__ == "__main__":
    unittest.main()
