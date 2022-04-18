class Settings:
    """Game settings"""
    def __init__(self):
        """Initialization"""
# Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (137, 181, 240)
        self.full_screen = False

# Spaceship settings
        self.spaceship_speed = 1.5

# Bullets settings
        self.bullet_speed = 1.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullet_allowed = 5

# Aliens settings
        self.alien_speed = 0.2
        self.fleet_drop_speed = 10
        self.fleet_direction = 1
