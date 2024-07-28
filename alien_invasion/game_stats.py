class GameStats:
    """track statistics for alien invasion game"""

    def __init__(self, ai_game):
        """initialise statistics"""
        self.settings = ai_game.settings
        self.reset_stats()
        #load highscore from file
        self.load_high_score()


    def load_high_score(self):
        """load highscore from file"""
        try:
            with open('highscore.txt', 'r') as file:
                self.high_score = int(file.read())
        except FileNotFoundError:
            self.high_score = 0

    
    def reset_stats(self):
        """initialise statistics that can change throughout the game"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1