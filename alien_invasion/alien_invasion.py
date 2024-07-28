import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    """Overall class to manage game assets and behavior"""

    def __init__(self):
        """Initialise the game & creat game resources"""
        pygame.init()

        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        pygame.display.set_caption("Alien Invasion")

        #create an instance to store game stats,
        #and create a scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship_group = pygame.sprite.Group()
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        self.game_active = False
        self.selected_difficulty = None

        # Make difficulty buttons
        self.easy_button = Button(self, "Easy", 700, 300)
        self.medium_button = Button(self, "Medium", 700, 400)
        self.hard_button = Button(self, "Hard", 700, 500)


    def run_difficulty_selection(self):
        """run difficulty selection screen"""
        while not self.selected_difficulty:
            self._check_events()
            self._update_difficulty_screen()
            pygame.display.flip()
            self.clock.tick(60)


    def _update_difficulty_screen(self):
        self.screen.fill(self.settings.bg_colour)
        self.easy_button.draw_button()
        self.medium_button.draw_button()
        self.hard_button.draw_button()

        pygame.display.flip()

    
    def run_game(self):
        """Start the main loop for the game"""
        # Run difficulty selection until a difficulty is chosen
        self.run_difficulty_selection()

        # If a difficulty is chosen, start the game loop
        if self.selected_difficulty:
            self.game_active = True
            while self.game_active:
                self._check_events()
                self._update_screen()
                self.clock.tick(60)
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self._check_bullet_alien_collisions()


    def _check_events(self):
        """respond to key press & mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_difficulty_buttons(mouse_pos)


    def _check_difficulty_buttons(self, mouse_pos):
        """Check if difficulty buttons are clicked"""
        if self.easy_button.rect.collidepoint(mouse_pos):
            self.settings.set_difficulty_level('easy')
            self.selected_difficulty = 'easy'
        elif self.medium_button.rect.collidepoint(mouse_pos):
            self.settings.set_difficulty_level('medium')
            self.selected_difficulty = 'medium'
        elif self.hard_button.rect.collidepoint(mouse_pos):
            self.settings.set_difficulty_level('hard')
            self.selected_difficulty = 'hard'


    def _start_game(self):
        """actions to start game"""
        #get rid of any remaining bullets & aliens
        self.bullets.empty()
        self.aliens.empty()

        #create a new fleet & center the ship
        self._create_fleet()
        self.ship.center_ship() 

        #hide the mouse cursor
        pygame.mouse.set_visible(False)


    def _check_keydown_events(self, event):
        """respond to keypresses"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True  
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True  
        elif event.key == pygame.K_q:
            sys.exit()  
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()


    def _check_keyup_events(self, event):
        """respond to key releases"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False


    def _fire_bullet(self):
        """create new bullet & add it to bullets group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)


    def _update_bullets(self):
        """update position of bullets and get rid of old bullets"""
        #update bullet position
        self.bullets.update()

        #get rid of bullets that have disapeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

       
    def _check_bullet_alien_collisions(self):
        """repsond to bullet, alien collisions"""
        #remove any bullets or aliens that have collided
        collisions = pygame.sprite.groupcollide(
        self.bullets, self.aliens, True, True
        )
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points *len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.aliens:
            #destroy existing bullets & create new fleet
            self.bullets.empty()
            #initiate countdown
            countdown = 3
            while countdown > 0:
                self.screen.fill(self.settings.bg_colour)
                font = pygame.font.SysFont(None, 48)
                countdown_text = font.render(
                    str(countdown), True, (0, 0, 0)
                    )
                countdown_text_rect = countdown_text.get_rect(
                    center=self.screen.get_rect().center
                    )
                self.screen.blit(countdown_text, countdown_text_rect)
                pygame.display.flip()
                pygame.time.delay(1000)
                countdown -= 1

            #display 'wave incoming'
            self.screen.fill(self.settings.bg_colour)
            wave_incoming_text = font.render(
                "Wave Incoming!", True, (0, 0, 0)
                )
            wave_incoming_text_rect = wave_incoming_text.get_rect(
                center=self.screen.get_rect().center
                )
            self.screen.blit(wave_incoming_text, wave_incoming_text_rect)
            pygame.display.flip()
            pygame.time.delay(1000)
            #create new fleet
            self._create_fleet()
            self.settings.increase_speed()
            #increase level
            self.stats.level += 1
            self.sb.prep_level()


    def _ship_hit(self):
        """Respond to ship being hit by an alien"""
        if self.stats.ships_left > 0:
            #decrement ship left & update scoreboard
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            #get rid of an remaining aliens & bullets
            self.bullets.empty()
            self.aliens.empty()

            #create new fleet and center ship
            self._create_fleet()
            self.ship.center_ship()

            #pause
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)


    def _check_aliens_bottom(self):
        """check if any aliens have reached the bottom of the screen"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break


    def _update_aliens(self):
        """check if fleet is at edge then update positions"""
        self._check_fleet_edges()
        self.aliens.update()

        #look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        self._check_aliens_bottom()


    def _create_fleet(self):
        """create the fleet of aliens"""
        #make an alien & keep adding aliens until there are none left
        #spacing between aliens is 1 alien width
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width

            #finished row, reset x value and increment y
            current_x = alien_width
            current_y += 2 * alien_height


    def _create_alien(self, x_position, y_position):
        """create an alien and place it in its row"""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)


    def _check_fleet_edges(self):
        """respond appropriatelyy if any aliens reach edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    
    def _change_fleet_direction(self):
        """drop entire fleet aand change fleet direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1


    def _update_screen(self):
        """Update images on the screen & flip to the new screen"""
        self.screen.fill(self.settings.bg_colour)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)

        #draw score information
        self.sb.show_score()

        pygame.display.flip()


if __name__ == '__main__':
    #Make a game instance & run the game
    ai = AlienInvasion()
    ai.run_game()