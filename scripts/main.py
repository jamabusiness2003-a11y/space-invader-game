from settings.imports import *
from settings.constants import *
from settings.support import import_frames, audio_importer
from sprites import *
from utility.button import Button
from utility.gamestate import GameState

class Game:

    def __init__(self): 
        pygame.init()
        self.window = pygame.display.set_mode(WINDOW)
        pygame.display.set_caption('Spaces Invader')
        self.clock = pygame.time.Clock()
        self.running = True 

        # setup
        self.load_images()

        # level and layeout setup
        self.level = 1
        self.invader_rows = 3
        self.invader_cols = 5

        # sprites
        self.all_sprites = AllSprites()
        self.laser_sprites = pygame.sprite.Group()
        self.player_group = pygame.sprite.GroupSingle()
        self.invader_lasers = pygame.sprite.Group()
        self.player_lasers = pygame.sprite.Group()
        self.invader_sprites = InvaderSprites(self.create_invaders, self.invader_rows, self.invader_cols)
         
        # player setup
        self.player = Player(self.all_sprites, self.create_lasers)
        pygame.display.set_icon(self.player.image)
        self.player_group.add(self.player)

        # font and score
        self.font = pygame.font.Font(join('font', 'kenvector_future.ttf'))
        self.score = 0

        # states and buttons
        self.current_state = GameState.MAIN_MENU
        self.setup_buttons()

        # flag
        self.level_transitioning = False

        # sounds
        self.current_volume = 0.3
        self.audio = audio_importer('sounds')
        self.audio['music'].set_volume(self.current_volume)
        self.audio['music'].play(loops=-1)
        
    def display_winner(self):
        self.create_background()
        self.draw_text(WINDOW_W / 2, 100, 'You Win !!!', YELLOW, 50)

    def display_game_over(self):
        self.create_background()
        self.draw_text(WINDOW_W / 2, 100, 'Game Over !!!', RED, 50)

    def setup_buttons(self):
        self.start_button = Button(WINDOW_W / 2, WINDOW_H / 2, 'buttonRed', 'Play', BLACK)
        self.quit_button = Button(WINDOW_W / 2, WINDOW_H / 2 + 50, 'buttonRed', 'Quit', BLACK)
        self.resume_button = Button(WINDOW_W / 2, WINDOW_H / 2, 'buttonRed', 'Resume', BLACK)
        self.retry_button = Button(WINDOW_W / 2, WINDOW_H / 2, 'buttonRed', 'Retry', BLACK)
        self.main_menu_button = Button(WINDOW_W / 2, WINDOW_H / 2 + 50, 'buttonRed', 'Main Menu', BLACK)
        self.next_level_button = Button(WINDOW_W / 2, WINDOW_H / 2, 'buttonRed', 'Next Level', BLACK)
        self.main_menu_button_2 = Button(WINDOW_W / 2, WINDOW_H - 50, 'buttonRed', 'Main Menu', BLACK)
        self.settings_button = Button(WINDOW_W / 2, WINDOW_H / 2 + 100, 'buttonRed', 'Settings', BLACK)

    def draw_text(self, x, y, text, text_color, size):
        font = pygame.font.Font(join('font', 'kenvector_future.ttf'), size)
        text_surf = font.render(text, False, text_color)
        text_rect = text_surf.get_frect(center = (x, y))
        self.window.blit(text_surf, text_rect)

    def load_images(self):
        raw_laserP_frames = import_frames('images', 'BlueLaser', 'BigLaser', 'SlimLaser')
        self.laserP_frames = [aspect_ratio(5, 28, frame, frame.get_size()) for frame in raw_laserP_frames]

        raw_explosion_frames = import_frames('images', 'BlueExplosion', 'BigExplosion')
        self.explosion_frames = [aspect_ratio(30, 30, frame, frame.get_size()) for frame in raw_explosion_frames]

        raw_explosion_frames_2 = import_frames('images', 'RedExplosion', 'BigExplosion')
        self.explosion_frames_2 = [aspect_ratio(30, 30, frame, frame.get_size()) for frame in raw_explosion_frames_2] 
    
    def display_score(self):
        self.draw_text(WINDOW_W / 2, 50, f'Score : {self.score}', WHITE, 35)

    def display_level(self):
        self.draw_text(WINDOW_W - 150, 50, f'Level {self.level}', WHITE, 35)

    def add_score(self, amount):
        self.score += amount

    def create_background(self):
        bg_surf = pygame.image.load(join('images', 'Backgrounds', 'black.png')).convert()

        bg_width, bg_height = bg_surf.get_size()
        
        for x in range(0, WINDOW_W, bg_width):
            for y in range(0, WINDOW_H, bg_height):
                bg_rect = bg_surf.get_frect(topleft = (x, y))
                self.window.blit(bg_surf, bg_rect)

    def create_lasers(self, pos, direction):
        match direction:
            case -1:
                Player_Laser(pos, self.laserP_frames, direction, (self.all_sprites, self.player_lasers))
            case 1:
                Invader_Laser(pos, direction, (self.all_sprites, self.invader_lasers))

    def create_invaders(self, pos):
       self.invader = Invader(pos, self.create_lasers, self.all_sprites)
       return self.invader
        
    def collisions(self):
        # player laser -> invaders
        for laser_p in self.player_lasers:
            collided_sprites = laser_p.check_collision(self.invader_sprites)
            if collided_sprites:
                laser_p.kill()
                self.audio['explosion-fx'].play()
                self.add_score(30)
                Explosion(self.explosion_frames, laser_p.rect.x, laser_p.rect.y, self.all_sprites)
                self.invader_sprites.increase_speed(2.5)

        # invader laser -> player
        for laser_i in self.invader_lasers:
            if pygame.sprite.spritecollide(laser_i, self.player_group, False, pygame.sprite.collide_mask):
                laser_i.damage(self.player, 30)
                laser_i.kill()
                self.audio['explosion-fx'].play()
                Explosion(self.explosion_frames_2, laser_i.rect.x, laser_i.rect.y, self.all_sprites)
                if self.player.health == 0:
                    self.player.destroy()

    def display_main_menu_screen(self):
        self.create_background()
        self.draw_text(WINDOW_W / 2, 100, 'Space Invader', GREEN, 50)
        self.start_button.draw(self.window)
        self.quit_button.draw(self.window)
        self.settings_button.draw(self.window)

    def display_pause_menu(self, alpha=255):
        overlay = pygame.Surface(self.window.get_size(), SRCALPHA)
        overlay.fill((0,0,0,alpha))
        self.window.blit(overlay, (0,0))
        self.resume_button.draw(self.window)
        self.draw_text(WINDOW_W / 2, 100, 'Paused', YELLOW, 50)

    def display_settings(self):
        self.create_background()
        self.draw_text(WINDOW_W / 2, 100, 'Settings', GREEN, 50)
        self.main_menu_button_2.draw(self.window)
        self.volume_bar()

    def volume_bar(self):
        keys = pygame.key.get_pressed()

        if keys[K_LEFT]:
            self.current_volume = max(0.0, self.current_volume - 0.01)
        elif keys[K_RIGHT]:
            self.current_volume = min(1.0, self.current_volume + 0.01)


        self.audio['music'].set_volume(self.current_volume)

        pygame.draw.rect(self.window, RED, (WINDOW_W / 2 - 80, WINDOW_H / 2, 150, 15),2)
        pygame.draw.rect(self.window, GREEN, (WINDOW_W / 2 - 80, WINDOW_H / 2, int(150 * self.current_volume), 15))

        self.draw_text(WINDOW_W / 2, WINDOW_H / 2 - 50, f'Volume {int(self.current_volume * 100)}%', WHITE, 30)

    def restart_game(self):
        # restart the music
        self.audio['music'].stop()
        self.audio['music'].play(loops = -1)

        # clear the groups
        self.all_sprites.empty()
        self.laser_sprites.empty()
        self.player_group.empty()
        self.invader_sprites.empty()
        self.invader_lasers.empty()
        self.player_lasers.empty()

        # reset the score and level
        self.score = 0
        self.invader_rows = 3
        self.invader_cols = 5
        
        # recreate the player
        self.player = Player(self.all_sprites, self.create_lasers)
        pygame.display.set_icon(self.player.image)
        self.player_group.add(self.player)

        # recreate the invaders
        self.invader_sprites = InvaderSprites(self.create_invaders, self.invader_rows, self.invader_cols)

    def next_level(self):
        # increase the level
        self.level += 1
        if self.level <= 5:
            self.invader_rows += 1
            self.invader_cols += (1 if self.level % 2 == 0 else 0)

        # restart the music
        self.audio['music'].stop()
        self.audio['music'].play(loops = -1)

        # clear previous level data
        self.all_sprites.empty()
        self.laser_sprites.empty()
        self.player_group.empty()
        self.invader_sprites.empty()
        self.invader_lasers.empty()
        self.player_lasers.empty()

        
        # recreate the player and invaders
        self.player = Player(self.all_sprites, self.create_lasers)
        pygame.display.set_icon(self.player.image)
        self.player_group.add(self.player)

        self.invader_sprites = InvaderSprites(self.create_invaders, self.invader_rows, self.invader_cols)

        # increase difficulty
        self.increase_difficulty()

        # back to gameplay
        self.current_state = GameState.GAMEPLAY

        self.level_transitioning = False

    def increase_difficulty(self):
        self.invader_sprites.increase_speed(0.5 + self.level * 2)
        for laser_i in self.invader_lasers:
            laser_i.speed += 0.2

    def handle_event(self, events):
        keys = pygame.key.get_just_pressed()
        for event in events:
            if event.type == QUIT:
                self.running = False
                sys.exit()

        match self.current_state:
            case GameState.MAIN_MENU:
                if self.start_button.is_clicked(events):
                    self.current_state = GameState.GAMEPLAY
                elif self.settings_button.is_clicked(events):
                    self.current_state = GameState.SETTINGS
                elif self.quit_button.is_clicked(events):
                    self.running = False
                    sys.exit()
            case GameState.GAMEPLAY:
                if not self.invader_sprites:
                    self.current_state = GameState.GAME_OVER
                elif self.player.health == 0: 
                    self.current_state = GameState.GAME_OVER
                elif keys[K_p]:
                    self.current_state = GameState.PAUSE
            case GameState.PAUSE:
                if self.resume_button.is_clicked(events) or keys[K_p]:
                    self.current_state = GameState.GAMEPLAY
            case GameState.GAME_OVER:
                if not self.invader_sprites:
                    if self.next_level_button.is_clicked(events):
                        self.next_level()
                    elif self.main_menu_button.is_clicked(events):
                        self.level = 1
                        self.restart_game()
                        self.current_state = GameState.MAIN_MENU
                elif self.player.health == 0:
                    if self.retry_button.is_clicked(events) or keys[K_n]:
                        self.level = 1
                        self.restart_game()
                        self.current_state = GameState.GAMEPLAY
                    elif self.main_menu_button.is_clicked(events):
                        self.level = 1
                        self.restart_game()
                        self.current_state = GameState.MAIN_MENU
            case GameState.SETTINGS:
                if self.main_menu_button_2.is_clicked(events):
                    self.current_state = GameState.MAIN_MENU

    def handle_states(self, dt):
        match self.current_state:
            case GameState.MAIN_MENU:
                self.display_main_menu_screen()
            case GameState.GAMEPLAY:
                # update
                self.all_sprites.update(dt)
                self.invader_sprites.update(dt)
                self.collisions()
                # draw
                self.create_background()
                self.all_sprites.draw()
                self.invader_sprites.draw(self.window)
                self.display_score()
                self.display_level()
                if self.player.alive():
                    self.player.health_bar(self.window)
            case GameState.PAUSE:
                self.create_background()
                self.all_sprites.draw()
                self.invader_sprites.draw(self.window)
                self.display_score()
                self.display_level()
                if self.player.alive():
                    self.player.health_bar(self.window)
                self.display_pause_menu(100)
            case GameState.GAME_OVER:
                if not self.invader_sprites:
                    self.display_winner()
                    self.next_level_button.draw(self.window)
                    self.main_menu_button.draw(self.window)
                elif self.player.health == 0:
                    self.display_game_over()
                    self.retry_button.draw(self.window)
                    self.main_menu_button.draw(self.window)
            case GameState.SETTINGS:
                self.display_settings()

    def run(self):
        while self.running:

            dt = self.clock.tick(FRAMERATE) / 1000
            events = pygame.event.get()

            self.handle_event(events)
            self.handle_states(dt)

            pygame.display.update()

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()