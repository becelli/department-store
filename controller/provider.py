from model.classes.database import Database
from model.classes import provider as p


class ProviderController:
    def __init__(self, db_name):
        self.db = Database(db_name)

    def get_random_provider(self):
        return self.db.select_random_provider()

    def get_provider_by_id(self, id: int):
        return self.db.select_provider_by_id(id)

    def get_all_providers(self):
        return self.db.select_all_providers()

    def get_random_provider(self):
        return self.db.select_random_provider()

    def add_provider(self, provider: p.Provider):
        return self.db.insert_provider(provider)
