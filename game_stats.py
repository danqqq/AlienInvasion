class GameStats:
    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.spaceships_left = self.settings.spaceships_limit
        self.reset_stats()
        self.score = 0
        self.game_active = False
        self.high_score = 0

    def reset_stats(self):
        self.spaceships_left = self.settings.spaceships_limit
        self.score = 0
