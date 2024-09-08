import pygame as pg
import sys
import time
import random

pg.init()

class Game:
    def __init__(self):
        self.width = 600
        self.height = 300
        self.win = pg.display.set_mode((self.width, self.height))
        self.clock = pg.time.Clock()

        # Load ground images
        self.ground1 = pg.image.load("assets/ground.png").convert_alpha()
        self.ground1_rect = self.ground1.get_rect(center=(300, 250))

        self.ground2 = pg.image.load("assets/ground.png").convert_alpha()
        self.ground2_rect = self.ground2.get_rect(center=(900, 250))

        # Load fonts and labels
        self.font = pg.font.Font("assets/font.ttf", 20)
        self.label_score = self.font.render("Score: 0", True, (0, 0, 0))
        self.label_score_rect = self.label_score.get_rect(center=(500, 20))

        self.label_restart = self.font.render("Restart Game", True, (0, 0, 0))
        self.label_restart_rect = self.label_restart.get_rect(center=(300, 150))

        # Load sounds
        self.dead_sound = pg.mixer.Sound("assets/sfx/dead.mp3")
        self.jump_sound = pg.mixer.Sound("assets/sfx/jump.mp3")
        self.points_sound = pg.mixer.Sound("assets/sfx/points.mp3")

        self.dino = Dino()
        self.game_lost = False
        self.move_speed = 250
        self.enemy_spawn_counter = 0
        self.enemy_spawn_time = 80
        self.score = 0
        self.enemy_group = pg.sprite.Group()

        self.gameLoop()

    def checkCollisions(self):
        # Check for collision between Dino and enemies
        if pg.sprite.spritecollide(self.dino, self.enemy_group, False, pg.sprite.collide_mask):
            self.stopGame()

    def stopGame(self):
        # Handle game over logic
        self.game_lost = True
        self.dead_sound.play()

    def restart(self):
        # Restart the game state
        self.game_lost = False
        self.score = 0
        self.enemy_spawn_counter = 0
        self.move_speed = 250
        self.label_score = self.font.render("Score: 0", True, (0, 0, 0))
        self.dino.resetDino()

        for enemy in self.enemy_group:
            enemy.deleteMyself()

    def gameLoop(self):
        # Main game loop
        last_time = time.time()
        while True:
            new_time = time.time()
            dt = new_time - last_time
            last_time = new_time

            # Event handling
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    if not self.game_lost:
                        self.dino.jumpDino(dt)
                        self.jump_sound.play()
                    else:
                        self.restart()

            # Update display
            self.win.fill((255, 255, 255))

            if not self.game_lost:
                # Move ground images to create a scrolling effect
                self.ground1_rect.x -= int(self.move_speed * dt)
                self.ground2_rect.x -= int(self.move_speed * dt)

                if self.ground1_rect.right < 0:
                    self.ground1_rect.x = 600
                if self.ground2_rect.right < 0:
                    self.ground2_rect.x = 600

                # Increment score
                self.score += 0.1
                self.label_score = self.font.render(f"Score: {int(self.score)}", True, (0, 0, 0))

                # Update dino and enemies
                self.dino.update(dt)
                self.enemy_group.update(dt)

                # Spawn enemies based on the timer
                if self.enemy_spawn_counter == self.enemy_spawn_time:
                    if random.randint(0, 1) == 0:
                        self.enemy_group.add(Bird(self.enemy_group, self.move_speed))
                    else:
                        self.enemy_group.add(Tree(self.enemy_group, self.move_speed))
                    self.enemy_spawn_counter = 0
                self.enemy_spawn_counter += 1

                # Speed up game as score increases
                if int(self.score) % 30 == 0:
                    self.move_speed += 5
                    for enemy in self.enemy_group:
                        enemy.setMoveSpeed(self.move_speed)

                # Play sound every 100 points
                if int(self.score + 1) % 100 == 0:
                    self.points_sound.play()

                # Draw sprites
                self.win.blit(self.dino.image, self.dino.rect)
                for enemy in self.enemy_group:
                    self.win.blit(enemy.image, enemy.rect)

                self.checkCollisions()
            else:
                # Display restart message when game is lost
                self.win.blit(self.label_restart, self.label_restart_rect)

            # Render ground and score
            self.win.blit(self.ground1, self.ground1_rect)
            self.win.blit(self.ground2, self.ground2_rect)
            self.win.blit(self.label_score, self.label_score_rect)
            pg.display.update()
            self.clock.tick(60)


class Dino(pg.sprite.Sprite):
    def __init__(self):
        super(Dino, self).__init__()
        # Load dino images
        self.dino_run_list = [pg.image.load("assets/dino1.png").convert_alpha(),
                              pg.image.load("assets/dino2.png").convert_alpha()]
        self.dino_crouch_list = [pg.image.load("assets/dino_crouch1.png").convert_alpha(),
                                 pg.image.load("assets/dino_crouch2.png").convert_alpha()]

        self.image = self.dino_run_list[0]
        self.mask = pg.mask.from_surface(self.image)
        self.resetDino()
        self.gravity = 10
        self.jump_speed = 250

    def update(self, dt):
        # Handle crouching and animation
        keys = pg.key.get_pressed()
        if keys[pg.K_DOWN]:
            self.crouch = True
        else:
            self.crouch = False

        if self.is_on_ground:
            # Switch between run and crouch animations
            if self.anim_counter == 5:
                if self.crouch:
                    self.image = self.dino_crouch_list[self.image_switch]
                    self.rect = pg.Rect(200, 220, 55, 30)
                else:
                    self.image = self.dino_run_list[self.image_switch]
                    self.rect = pg.Rect(200, 200, 43, 51)

                self.mask = pg.mask.from_surface(self.image)
                self.image_switch = 1 - self.image_switch  # Toggle between 0 and 1
                self.anim_counter = 0
            self.anim_counter += 1
        else:
            # Handle jump movement
            self.velocity_y += self.gravity * dt
            self.rect.y += self.velocity_y
            if self.rect.y >= 200:
                self.is_on_ground = True
                self.rect.y = 200

    def jumpDino(self, dt):
        # Jump only when the Dino is on the ground
        if self.is_on_ground:
            self.velocity_y = -self.jump_speed * dt
            self.is_on_ground = False

    def resetDino(self):
        # Reset dino state
        self.rect = pg.Rect(200, 200, 43, 51)
        self.image_switch = 1
        self.anim_counter = 0
        self.crouch = False
        self.is_on_ground = True
        self.velocity_y = 0


class Bird(pg.sprite.Sprite):
    def __init__(self, enemy_group, move_speed):
        super(Bird, self).__init__()
        # Load bird images
        self.img_list = [pg.image.load("assets/bird1.png").convert_alpha(),
                         pg.image.load("assets/bird2.png").convert_alpha()]
        self.image = self.img_list[0]
        self.mask = pg.mask.from_surface(self.image)
        self.rect = pg.Rect(600, 180, 42, 31)
        self.anim_counter = 0
        self.speed = move_speed
        self.enemy_group = enemy_group
        self.image_switch = 1

    def update(self, dt):
        # Animate bird and move
        if self.anim_counter == 8:
            self.image = self.img_list[self.image_switch]
            self.image_switch = 1 - self.image_switch  # Toggle between 0 and 1
            self.anim_counter = 0
        self.anim_counter += 1

        self.rect.x -= self.speed * dt
        if self.rect.right < 0:
            self.deleteMyself()

    def setMoveSpeed(self, move_speed):
        self.speed = move_speed

    def deleteMyself(self):
        # Remove bird from the game
        self.kill()
        del self


class Tree(pg.sprite.Sprite):
    def __init__(self, enemy_group, move_speed):
        super(Tree, self).__init__()
        # Load random tree image
        self.img_list = [pg.image.load(f"assets/trees/tree{i}.png").convert_alpha() for i in range(1, 6)]
        self.image = random.choice(self.img_list)
        self.mask = pg.mask.from_surface(self.image)
        self.rect = pg.Rect(600, 208, 25, 51)
        self.speed = move_speed
        self.enemy_group = enemy_group

    def update(self, dt):
        # Move tree
        self.rect.x -= self.speed * dt
        if self.rect.right < 0:
            self.deleteMyself()

    def setMoveSpeed(self, move_speed):
        self.speed = move_speed

    def deleteMyself(self):
        # Remove tree from the game
        self.kill()
        del self

if __name__ == "__main__":
    Game()
