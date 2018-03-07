import pygame
import random
import sys
import os

# ------ Global CONSTANTS ----------
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


# ------ Classes ----------
class Alien(pygame.sprite.Sprite):
    """ This class describes enemy's starships. """

    def __init__(self):
        """ Constructor, below super() inherit all from Sprite Class. """
        super().__init__()
        self.image = pygame.Surface([20, 20])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()

    def spawn_ship(self):
        """ This function spawn ship in specified time. """
        self.rect.y = random.randrange(-300, -20)
        self.rect.x = random.randrange(SCREEN_WIDTH)

    def update(self):
        """ Moving aliens """
        self.rect.y += 1

        if self.rect.y > SCREEN_HEIGHT + self.rect.height:
            self.spawn_ship()


class Player(pygame.sprite.Sprite):
    """ This class describes the player. """
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([20, 20])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2
        self.rect.y = 500
        self.vector_x = 0
        self.vector_y = 0


class Shot(pygame.sprite.Sprite):
    """ This class describes shots. """
    def __init__(self):
        super().__init__()

        self.image = pygame.Surface([2, 10])
        self.image.fill(RED)
        self.rect = self.image.get_rect()

    def update(self):
        """ Move the bullets. """
        self.rect.y -= 7



class Game(object):
    """ This class describes an instance of the whole game. If we need to reset
    the game we can create a new instance of this class. """

    def __init__(self):
        """ Constructor, creates all attributes and initialize the game. """

        self.score = 0
        self.game_over = False

        # Create atributes/coords for stars
        self.stars_list = []
        self.stars_speed = []
        for i in range(100):
            x = random.randrange(0, 800)
            y = random.randrange(0, 600)
            star_width = 1
            star_height = 3
            star_speed = random.randrange(2,10)
            self.stars_list.append([x, y, star_width, star_height])
            self.stars_speed.append(star_speed)


        # Creating sprites lists
        self.aliens_list = pygame.sprite.Group()
        self.all_sprites_list = pygame.sprite.Group()
        self.shots_list = pygame.sprite.Group()

        # Sounds
        self.laser = pygame.mixer.Sound("laser.ogg")


        # Images
        self.background = pygame.image.load("galaxy.jpg").convert()

        # Variables need to move background
        self.x = -300
        self.y = 0

        # Create aliens
        for i in range(10):
            alien = Alien()
            alien.rect.x = random.randrange(SCREEN_WIDTH)
            alien.rect.y = random.randrange(-20, -10)

            self.aliens_list.add(alien)
            self.all_sprites_list.add(alien)

        # Create the player
        self.player = Player()
        self.all_sprites_list.add(self.player)



    def process_events(self):
        """ Process all events in the game, for e.g. key pressing etc. """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_over:
                    self.__init__()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    self.laser.play()
                    shot = Shot()
                    shot.rect.x = self.player.rect.x
                    shot.rect.y = self.player.rect.y
                    self.shots_list.add(shot)
                    self.all_sprites_list.add(shot)
                    shot2 = Shot()
                    shot2.rect.x = self.player.rect.x+16
                    shot2.rect.y = self.player.rect.y
                    self.shots_list.add(shot2)
                    self.all_sprites_list.add(shot2)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.rect.x -= 3
        if keys[pygame.K_RIGHT]:
            self.player.rect.x += 3
        if keys[pygame.K_UP]:
            self.player.rect.y -= 3
        if keys[pygame.K_DOWN]:
            self.player.rect.y += 3

        return False

    def run_logic(self):
        """ This method is run each frame. Updates positions, check collisions etc. """

        if not self.game_over:

            # Move all the sprites
            self.all_sprites_list.update()

            # Check each shot if hit
            for shot in self.shots_list:
                aliens_hit_list = pygame.sprite.spritecollide(shot, self.aliens_list, True)
                for alien in aliens_hit_list:
                    self.shots_list.remove(shot)
                    self.all_sprites_list.remove(shot)
                    self.score += 1
                    print(self.score)
                    # You can do something with "alien" here.

            # Check collisions
            aliens_hit_list = pygame.sprite.spritecollide(self.player, self.aliens_list, True)
            for alien in aliens_hit_list:
                if aliens_hit_list:
                    self.game_over = True

            # Move stars
            for i in range(len(self.stars_list)):
                self.stars_list[i][1] += self.stars_speed[i]

                if self.stars_list[i][1] > 600:
                    self.stars_list[i][1] = 0
                    self.stars_list[i][0] = random.randrange(0, 800)

            # Move background image
            self.y += 0.5

            if len(self.aliens_list) == 0:
                self.game_over = True


    def display_frame(self, screen):
        """ Display everything to the screen. """

        # Create backgrounds
        for i in range(30):
            screen.blit(self.background, [self.x, self.y+728*-i])

        if self.game_over:
            font = pygame.font.SysFont("serif", 25)
            text = font.render("Game over, click to restart", True, WHITE)
            center_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
            center_y = (SCREEN_HEIGHT //2) - (text.get_height() //2)
            screen.blit(text, [center_x, center_y])

        if not self.game_over:
            for i in range(len(self.stars_list)):
                pygame.draw.rect(screen, WHITE, self.stars_list[i], 1)
            self.all_sprites_list.draw(screen)


        pygame.display.flip()

def main():
    """ Main program function. """
    pygame.init()

    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Shooting Stars 1.0")

    # Create objects and set the data
    done = False
    clock = pygame.time.Clock()


    # Instance of the Game class
    game = Game()

    # Main game loop
    while not done:

        # Process events
        game.process_events()

        # Update objects.
        game.run_logic()

        # Draw the current frame
        game.display_frame(screen)

        # Pause for the next frame to limit to 60 fps
        clock.tick(60)

    # Close window
    pygame.quit()

# Call the main function, start up the game
if __name__ == "__main__":
    main()


