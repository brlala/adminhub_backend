import urllib.request

from app.server.models.bot import BotSchemaDbOut


class DbConfig:
    def __init__(self):
        # with urllib.request.urlopen('http://localhost:5000/bot/me') as response:
        #     config = response.json()
        # self.config = BotSchemaDbOut(**config)
        # self.portal = self.config.portal
        pass


db_config = DbConfig()
