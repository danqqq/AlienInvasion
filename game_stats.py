class GameStats:
    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.spaceships_left = self.settings.spaceships_limit
        self.reset_stats()
        self.game_active = True

    def reset_stats(self):
        self.spaceships_left = self.settings.spaceships_limit
