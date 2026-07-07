import sys
import pygame
from pygame import Surface, Rect
from pygame.font import Font

from const import WIN_WIDTH, WIN_HEIGHT, C_DARK_GREEN, C_WHITE, C_YELLOW, FONT_TITLE, FONT_HUD, MAX_NAME_LENGTH


class NameEntry:
    def __init__(self, window: Surface):
        self.window = window

    def run(self, prompt: str) -> str:
        name = ''
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            self.window.fill(C_DARK_GREEN)

            self._text(FONT_HUD, prompt, C_WHITE, (WIN_WIDTH / 2, WIN_HEIGHT / 2 - 40))

            # mostra o que ja foi digitado; se estiver vazio, mostra um "_"
            # so pra dar uma pista visual de onde o texto vai aparecer
            texto_exibido = name if name else '_'
            self._text(FONT_TITLE, texto_exibido, C_YELLOW, (WIN_WIDTH / 2, WIN_HEIGHT / 2 + 10))

            self._text(FONT_HUD, 'ENTER para confirmar', C_WHITE, (WIN_WIDTH / 2, WIN_HEIGHT / 2 + 70))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and len(name) > 0:
                        return name
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        if len(name) < MAX_NAME_LENGTH:
                            name += event.unicode

    def _text(self, size: int, text: str, color: tuple, center_pos: tuple):
        font: Font = pygame.font.SysFont('Arial', size, bold=True)
        surf: Surface = font.render(text, True, color)
        rect: Rect = surf.get_rect(center=center_pos)
        self.window.blit(surf, rect)