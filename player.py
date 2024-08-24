import pygame

#Physics
ACCELERATION = 0.85
FRICTION = 0.15
MAX_SPEED = 5
GRAVITY = 2
FREE_FALL = 4

#Width and initialized height
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 700
START_HEIGHT = 200

class Player(pygame.sprite.Sprite):

    def __init__(self, x, y, radius, color, gravity, free_fall):
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = -gravity
        self.radius = radius
        self.color = color
        self.gravity = -gravity
        self.free_fall = free_fall
        #Smiling image
        self.smiling_image = pygame.image.load('imgs/smiling.png').convert_alpha()  # Load the image
        self.smiling_image = pygame.transform.scale(self.smiling_image, (2 * radius, 2 * radius))  # Scale image to fit radius
        #Scared image
        self.scared_image = pygame.image.load('imgs/scared.png').convert_alpha()  # Load the image
        self.scared_image = pygame.transform.scale(self.scared_image, (2 * radius, 2 * radius))  # Scale image to fit radius
        self.falling = False

    def reset(self):
        self.x = SCREEN_WIDTH // 2
        self.y = START_HEIGHT
        self.dx = 0
        self.dy = -self.gravity
    
    #Check if the ball is on top of a platform
    def is_vertically_collided(self, platforms):
        for platform in platforms:
            if (self.x + self.radius > platform.x and
                self.x - self.radius < platform.x + platform.width and
                self.y + self.radius >= platform.y and
                self.y + self.radius <= platform.y + platform.height):
                self.y = platform.y - self.radius
                self.falling = False
                return True
        self.falling = True
        return False
    
    #Check if the ball bounces on the side of the platform
    def is_horizontally_collided(self, platforms):
        for platform in platforms:
            if (self.x + self.radius > platform.x and
            self.x - self.radius < platform.x + platform.width and
            self.y + self.radius > platform.y and
            self.y - self.radius < platform.y + platform.height):
                #Right side hit
                if self.x - self.radius < platform.x + platform.width and self.x + self.radius > platform.x + platform.width:
                    return 2
                #Left side hit
                elif self.x + self.radius > platform.x and self.x - self.radius < platform.x:
                    return 1
        return 0

    def update_difficulty(self, difficulty):
        self.gravity = difficulty * -GRAVITY
        self.free_fall = difficulty * FREE_FALL

    #Player movement
    def update(self, keys, screen_width, platforms):
        if keys[pygame.K_LEFT]:
            self.dx = max(-MAX_SPEED, self.dx - ACCELERATION)
        elif keys[pygame.K_RIGHT]:
            self.dx = min(MAX_SPEED, self.dx + ACCELERATION)
        else:
            self.dx *= FRICTION
        
        self.x += self.dx

        horizontal_collision_state = self.is_horizontally_collided(platforms)

        if self.x - self.radius < 0:
            self.x = self.radius
            self.dx = abs(self.dx)
        elif self.x + self.radius > screen_width:
            self.x = screen_width - self.radius
            self.dx = -abs(self.dx)

        if horizontal_collision_state == 2:
            self.dx = abs(self.dx)
        elif horizontal_collision_state == 1:
            self.dx = -abs(self.dx)

        #Adjust falling ball
        if self.is_vertically_collided(platforms):
            self.dy = self.gravity
        else:
            self.dy = self.gravity + self.free_fall
        self.y += (int) (self.dy)
        
    #Drawing
    def draw(self, screen):
        top_left_x = self.x - self.radius
        top_left_y = self.y - self.radius
        if (self.falling):
            screen.blit(self.scared_image, (top_left_x, top_left_y))
        else:
            screen.blit(self.smiling_image, (top_left_x, top_left_y))

    #Check if the player is out of the screen
    def game_over(self):
        return self.y < self.radius / 2 or self.y > SCREEN_HEIGHT