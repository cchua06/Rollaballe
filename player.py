import pygame

# Initialize mixer for player sounds
pygame.mixer.init()

# Physics
ACCELERATION = 0.85
FRICTION = 0.15
MAX_SPEED = 5
GRAVITY = 2
FREE_FALL = 4

# Width and initialized height
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 700
START_HEIGHT = 200

class Player(pygame.sprite.Sprite):

    def __init__(self, x, y, radius):
        super().__init__()
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = -GRAVITY
        self.radius = radius
        self.accelerationmultiplier = 1.0
        self.maxspeedmultiplier = 1.0
        self.gravity = -GRAVITY
        self.free_fall = FREE_FALL
        self.falling = False
        self.was_falling = False  # To track the previous falling state
        # Smiling image
        self.smiling_image = pygame.image.load('imgs/smiling.png').convert_alpha()  # Load the image
        self.smiling_image = pygame.transform.scale(self.smiling_image, (2 * radius, 2 * radius))  # Scale image to fit radius
        # Scared image
        self.scared_image = pygame.image.load('imgs/scared.png').convert_alpha()  # Load the image
        self.scared_image = pygame.transform.scale(self.scared_image, (2 * radius, 2 * radius))  # Scale image to fit radius
        # Load music
        self.falling_sound = pygame.mixer.Sound('sounds/falling.ogg')
        self.falling_sound.set_volume(0.3)
        self.splat_sound = pygame.mixer.Sound('sounds/splat.ogg')
        self.landing_sound = pygame.mixer.Sound('sounds/landing.ogg')

    def reset(self):
        self.x = SCREEN_WIDTH // 2
        self.y = START_HEIGHT
        self.dx = 0
        self.accelerationmultiplier = 1.0
        self.maxspeedmultiplier = 1.0
        self.dy = -GRAVITY
        self.gravity = -GRAVITY
        self.free_fall = FREE_FALL
        self.falling = False
        self.was_falling = False  # Reset the previous falling state

    #Mute player sounds
    def mute(self):
        self.falling_sound.set_volume(0)
        self.splat_sound.set_volume(0)
        self.landing_sound.set_volume(0)

    #Unmute player sounds
    def unmute(self):
        self.falling_sound.set_volume(0.3)
        self.splat_sound.set_volume(1)
        self.landing_sound.set_volume(1)
    
    # Check if the ball is on top of a platform
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
    
    # Check if the ball bounces on the side of the platform
    def is_horizontally_collided(self, platforms):
        for platform in platforms:
            if (self.x + self.radius > platform.x and
                self.x - self.radius < platform.x + platform.width and
                self.y + self.radius > platform.y and
                self.y - self.radius < platform.y + platform.height):
                # Right side hit
                if self.x - self.radius < platform.x + platform.width and self.x + self.radius > platform.x + platform.width:
                    return 2
                # Left side hit
                elif self.x + self.radius > platform.x and self.x - self.radius < platform.x:
                    return 1
        return 0

    def update_difficulty(self, difficulty):
        self.gravity = difficulty * -GRAVITY
        self.free_fall = difficulty * FREE_FALL
        self.accelerationmultiplier = (float) (1.0 + ((difficulty - 1) * 0.1))
        self.maxspeedmultiplier = (float) (1.0 + ((difficulty - 1) * 0.1))

    # Player movement
    def update(self, keys, screen_width, platforms):
        if keys[pygame.K_LEFT]:
            self.dx = max(-(MAX_SPEED * self.maxspeedmultiplier), self.dx - ACCELERATION * self.accelerationmultiplier)
        elif keys[pygame.K_RIGHT]:
            self.dx = min((MAX_SPEED * self.maxspeedmultiplier), self.dx + ACCELERATION * self.accelerationmultiplier)
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

        # Adjust falling ball
        if self.is_vertically_collided(platforms):
            self.dy = self.gravity
        else:
            self.dy = self.gravity + self.free_fall
        self.y += int(self.dy)

        # Handle falling sound
        if self.falling and not self.was_falling:
            self.falling_sound.play()
        elif not self.falling and self.was_falling:
            self.landing_sound.play()
            self.falling_sound.stop()
        
        self.was_falling = self.falling  # Update previous falling state

    # Drawing
    def draw(self, screen):
        top_left_x = self.x - self.radius
        top_left_y = self.y - self.radius
        if self.falling:
            screen.blit(self.scared_image, (top_left_x, top_left_y))
        else:
            screen.blit(self.smiling_image, (top_left_x, top_left_y))

    # Check if the player is out of the screen
    def game_over(self):
        if (self.y < self.radius / 2 or self.y > SCREEN_HEIGHT):
            self.falling_sound.stop()
            self.splat_sound.play()
            return True
        return False
