import pygame.locals
from settings.imports import *
from settings.constants import *
from settings.gametimer import GameTimer
from settings.support import aspect_ratio, audio_importer

class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, frames, groups):
        super().__init__(groups)
        self.frames = frames
        self.frame_index = 0 
        self.animation_speed = 100

    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        self.image = self.frames[int(self.frame_index) % len(self.frames)]

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.window = pygame.display.get_surface()
    
    def draw(self):
        for sprite in self:
            self.window.blit(sprite.image, sprite.rect)

class Player(pygame.sprite.Sprite):
    def __init__(self, groups, create_laser, max_health=100):
        super().__init__(groups)
        self.window = pygame.display.get_surface()
        self.image = pygame.image.load(join('images', 'Player', 'playerShip1_red.png')).convert_alpha()
        self.image = aspect_ratio(40, 40, self.image, self.image.get_size())
        self.rect = self.image.get_frect(center = (WINDOW_W / 2, WINDOW_H - 50))
        # mask            
        self.mask = pygame.mask.from_surface(self.image)
        self.create_laser = create_laser
        self.health = 100
        self.max_health = max_health
        # movement
        self.direction = 1
        self.speed = 500
        # timer
        self.laser_timer = GameTimer(600)
        # audio
        self.audio = audio_importer('sounds')   
        
    def health_bar(self, surface):
        width, heigth = 40, 5
        health_ratio = self.health / self.max_health
        
        pygame.draw.rect(surface, (255,0,0), (self.rect.centerx - 20, self.rect.bottom + 5, width, heigth))
        pygame.draw.rect(surface, (0,255,0), (self.rect.centerx - 20, self.rect.bottom + 5, width * health_ratio, heigth))

    def destroy(self):
        self.kill()       

    def move_input(self):
        keys = pygame.key.get_pressed()
        self.direction = int(keys[K_RIGHT]) - int(keys[K_LEFT])

    def fire_laser(self):
        keys = pygame.key.get_pressed()
        if keys[K_SPACE] and not self.laser_timer:
            self.audio['sfx_laser1'].play()
            self.create_laser((self.rect.centerx + 1.2, self.rect.top - 20), -1)
            self.laser_timer.activate()

    def wall_collision(self):
        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, WINDOW_W)

    def move(self, dt):
        self.rect.x += self.direction * self.speed * dt

    def reset(self):
        self.rect = self.image.get_frect(center = (WINDOW_W / 2, WINDOW_H - 50))

    def update(self, dt):
        self.laser_timer.update()
        self.move_input()
        self.move(dt)
        self.fire_laser()
        self.wall_collision()

class Invader(pygame.sprite.Sprite):
    def __init__(self, pos, create_lasers,*groups):
        super().__init__(*groups)
        # setup
        self.image = pygame.image.load(join('images', 'Invader', f'invader_{randint(1, 18)}.png')).convert_alpha()
        self.image = aspect_ratio(40, 40, self.image, self.image.get_size())
        self.rect = self.image.get_frect(center = pos)
        self.create_lasers = create_lasers
        self.mask = pygame.mask.from_surface(self.image)

        # timer
        self.laser_timer = GameTimer(8000)
        self.delay_timer = GameTimer(3000, None, None, True)
        # flag
        self.shooting = False
    
    @staticmethod
    def get_invader_size():
        image = pygame.image.load(join('images', 'Invader', f'invader_{randint(1,18)}.png')).convert_alpha()
        image = aspect_ratio(40, 40, image, image.get_size())
        return image.get_size()

    def fire_lasers(self):

        if self.delay_timer:
            return

        if not self.laser_timer:
            if not self.shooting and random() < 0.1: # 50% chance of shooting
                self.shooting = True
                self.create_lasers(self.rect.midbottom, 1)
            self.laser_timer.activate()
    
    def update(self, _):
        self.delay_timer.update()
        self.laser_timer.update()
    
class InvaderSprites(pygame.sprite.Group):
    def __init__(self, create_invaders, rows=3, cols=5):
        super().__init__()
        self.rows, self.cols = rows, cols
        self.padding = 20
        self.width_inv, self.height_inv = Invader.get_invader_size()
        self.create_invaders = create_invaders
         # movement
        self.direction = pygame.Vector2(1,0)
        self.speed = 50
        # flag
        self.edge_reached = False

        # create the invaders
        for row in range(1, self.rows + 1):
            for col in range(1, self.cols + 1):
                x = 25 + col * (self.width_inv + self.padding)
                y = 25 + row * (self.height_inv + self.padding)
                invader = self.create_invaders((x, y))
                self.add(invader)
        
    def update(self, dt):
        for invader in self:
            invader.rect.x += self.direction.x * self.speed * dt

        if self:
            leftmost = min([invader.rect.left for invader in self])
            rightmost = max([invader.rect.right for invader in self])

            if not self.edge_reached and (leftmost <= 0 or rightmost >= WINDOW_W):
                self.edge_reached = True
                self.direction *= -1
                for invader in self:
                    invader.rect.y += 10
            elif 0 < leftmost  and rightmost < WINDOW_W:
                self.edge_reached = False

        for invader in self:
            invader.fire_lasers()     
    
    def increase_speed(self, amount):
        self.speed += amount

    def draw(self, surface):
        for invader in self:
            surface.blit(invader.image, invader.rect)

class Player_Laser(AnimatedSprite):
    def __init__(self, pos, frames, direction, groups):
        super().__init__(frames, groups)
        self.image = frames[0]      

        self.rect = self.image.get_frect(center = pos)
        self.mask = pygame.mask.from_surface(self.image)

        self.direction = direction
        self.pos = pygame.Vector2(self.rect.center)
        self.speed = 350

    def check_collision(self, group):
        return pygame.sprite.spritecollide(self, group, True, pygame.sprite.collide_mask)
        
    def update(self, dt):
        self.pos.y += self.direction * self.speed * dt
        self.animate(dt)
        self.rect.center = (round(self.pos.x), round(self.pos.y))
        if self.rect.top <= 0:
            self.kill()

class Invader_Laser(pygame.sprite.Sprite):
    def __init__(self, pos, direction, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('images', 'RedLaser', '10.png')).convert_alpha()
        self.image = aspect_ratio(4.5, 28.5, self.image, self.image.get_size())

        self.rect = self.image.get_frect(center = pos)
        self.direction = direction
        self.speed = 100
        self.mask = pygame.mask.from_surface(self.image)

    def damage(self, player, amount):
        player.health = max(0, player.health - amount)

    def update(self, dt):
        self.rect.centery += self.direction * self.speed * dt
        # mask
        if self.rect.bottom >= WINDOW_H:
            self.kill()

class Explosion(AnimatedSprite):
    def __init__(self, frames, x, y, groups):
        super().__init__(frames, groups)
        self.image = frames[0]
        self.rect = self.image.get_frect(center = (x, y))

        self.rotation = 0
        self.rotation_speed = 100

        self.animation_speed = 5.5

    def destroy(self):
        if int(self.frame_index) >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]


    def update(self, dt):  
        self.animate(dt)
        self.destroy()
        self.rotation += self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(self.image, self.rotation, 1)
        self.rect = self.image.get_frect(center = self.rect.center)