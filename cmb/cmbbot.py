from disco.bot.bot import Bot


class CmbBot(Bot):
    def __init__(self, client, config):
        super().__init__(client, config=config)
