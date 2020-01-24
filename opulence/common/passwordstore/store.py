from dynaconf import settings

from opulence.common.patterns import Singleton


class Store(Singleton):
    def __init__(self, path=None):
        self.keys = settings.API_KEYS

    def get_passwords_list(self):
        return list(self.keys.keys())

    def get_decrypted_password(self, path):
        if path not in self.keys:
            return None
        return self.keys[path]
