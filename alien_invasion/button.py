import pygame.font

class Button():
    """clas sto build buttons for the game"""

    def __init__(self, ai_game, msg, x, y):
        """initialise button attributes"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        #set dimensions & properties of the button
        self.width, self.height = 200, 50
        self.button_colour = (0, 135, 0)
        self.text_colour = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        #build buttons rect object and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.x = x
        self.rect.y = y


        #button message needs to prepped only once
        self._prep_msg(msg)
        self.msg_image_rect.center = self.rect.center


    def _prep_msg(self, msg):
        """turn msg to a rendered image and center text on the screen"""
        self.msg_image = self.font.render(msg, True, self.text_colour,
                                          self.button_colour)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center


    def draw_button(self):
        #todo - draw easy med and hard buttons
        """draw blank button & meesage"""
        self.screen.fill(self.button_colour, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)