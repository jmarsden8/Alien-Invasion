class Settings:
    """A class to store all settings for Alien Invasion"""

    def __init__(self):
        """Initialise game settings"""
        #screen settings
        self.bg_colour = (230, 230, 230)

        #ship  settings
        self.ship_limit = 3

        #bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_colour = (60, 60, 60)
        self.bullets_allowed = 3

        #alien settings
        self.fleet_drop_speed = 10
        #fleet direction: 1 = right, -1 = left
        self.fleet_direction = 1

        #how quickly the game speeds up
        self.speedup_scale = 1.1
        #how quickly alien point value increases
        self.score_scale = 1.5

        self.initialise_dynamic_settings()


    def initialise_dynamic_settings(self):
        """initialise settings that change throughout the game"""
        self.ship_speed = 3
        self.bullet_speed = 4.0
        self.alien_speed = 1.0
        #fleet direction: 1 = right, -1 = left
        self.fleet_direction = 1

        #scoring settings
        self.alien_points = 50


    def set_difficulty_level(self, level):
        if level == 'easy':
            self.ship_speed = 3
            self.bullet_speed = 4.0
            self.alien_speed = 1.0  
        
        elif level == 'medium':
            self.ship_speed = 4
            self.bullet_speed = 5.0
            self.alien_speed = 2.5  
        
        elif level == 'hard':
            self.ship_speed = 5
            self.bullet_speed = 6.0
            self.alien_speed = 4.0  
    

    def increase_speed(self):
        """increase speed settings & alien point values"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)