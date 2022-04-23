import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from spaceship import Spaceship
from bullet import Bullet
from alien import Alien
from button import Button


class AlienInvasion:
    def __init__(self):
        """Game initialization and base create"""
        pygame.init()
        self.settings = Settings()
        self._prepare_screen()
        pygame.display.set_caption("Inwazja Obcych")
        self.stats = GameStats(self)
        self.spaceship = Spaceship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.play_button = Button(self, "PLAY!")

        self._create_fleet()

    def run_game(self):
        """Main part"""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.spaceship.update()
                self._bullet_update()
                self._update_aliens()

            self._update_screen()

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.spaceship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        if not self.stats.game_active:
            self.play_button.draw_button()
        pygame.display.flip()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                self._check_play_button(mouse_position)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_play_button(self, mouse_position):
        if self.play_button.rect.collidepoint(mouse_position):
            self.stats.reset_stats()
            self.stats.game_active = True
            """Clear aliens and bullets lists"""
            self.aliens.empty()
            self.bullets.empty()
            """Creating new fleet / Center spaceship"""
            self._create_fleet()
            self.spaceship.center_spaceship()

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.spaceship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.spaceship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_h:
            self.settings.bullet_width = 300

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.spaceship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.spaceship.moving_left = False

    def _prepare_screen(self):
        if self.settings.full_screen:
            self.screen = pygame.display.set_mode((0, 0),
                                                  pygame.FULLSCREEN)
            self.settings.screen_width = self.screen.get_rect().width
            self.settings.screen_height = self.screen.get_rect().height
        else:
            self.screen = pygame.display.set_mode((self.settings.screen_width,
                                                   self.settings.screen_height))

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _bullet_update(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collision()

    def _check_bullet_alien_collision(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if not self.aliens:
            """Clear the screen of bullets and create new fleet"""
            self.bullets.empty()
            self._create_fleet()

    def _create_fleet(self):
        alien = Alien(self)
        """Calculate the number of aliens in row"""
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_of_aliens_x = available_space_x // (2 * alien_width)
        """Calculate the number of rows"""
        spaceship_height = self.spaceship.rect.height
        available_space_y = (self.settings.screen_height
                             - (3 * alien_height) - spaceship_height)
        number_rows = available_space_y // (2 * alien_height)
        for row_number in range(number_rows):
            for alien_number in range(number_of_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.spaceship, self.aliens):
            self._spaceship_hit()
        self._check_if_is_alien_bottom()

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _spaceship_hit(self):
        if self.stats.spaceships_left > 0:
            self.stats.spaceships_left -= 1
            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            self.spaceship.center_spaceship()
            sleep(0.7)
        else:
            self.stats.game_active = False

    def _check_if_is_alien_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._spaceship_hit()
                break


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
