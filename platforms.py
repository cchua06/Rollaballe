import pygame

class Platform(pygame.sprite.Sprite):

    def __init__(self, x, y, width, color, gravity, difficulty):
        self.x = x
        self.y = y
        self.gravity = gravity
        self.dy = -gravity * difficulty
        self.width = width
        self.height = 20
        self.color = color

    #Check if the platform is out of the screen
    def is_out_of_bounds(self):
        return self.y + self.height < -40

    def update_difficulty(self, difficulty):
        self.gravity = self.gravity * difficulty
        self.dy = -self.gravity

    #Updates
    def update(self):
        self.y += self.dy

    #Drawing
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    #Kill
    def kill(self):
        del(self)