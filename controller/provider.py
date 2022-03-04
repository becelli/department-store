from model.classes.database import Database
from model.classes import provider as p


class ProviderController:
    def __init__(self, db_name):
        self.db = Database(db_name)

    def select_random_provider(self):
        return self.db.select_random_provider()

    def select_provider_by_id(self, id: int):
        return self.db.select_provider_by_id(id)

    def select_all_providers(self):
        return self.db.select_all_providers()

    def insert_provider(self, provider: p.Provider):
        return self.db.insert_provider(provider)
