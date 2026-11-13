from settings.imports import *
from settings.constants import *

class Button:
    def __init__(self, x, y, img_file, text, text_color):
        self.img = pygame.image.load(join('images', 'Button', f'{img_file}.png'))
        self.rect = self.img.get_frect(center = (x, y))
        self.text = text
        self.text_color = text_color
        self.font = pygame.font.Font(join('font', 'kenvector_future.ttf'), 25)

    def draw(self, window):
        temp_img = self.img.copy()

        if self.rect.collidepoint(pygame.mouse.get_pos()):
            temp_img.set_alpha(150)

        window.blit(temp_img, self.rect)

        text_surf = self.font.render(self.text, False, self.text_color)
        text_rect = text_surf.get_frect(center = self.rect.center)
        window.blit(text_surf, text_rect)

    def is_clicked(self, events):
        for event in events:
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                if self.rect.collidepoint(event.pos):
                    return True
        return False
