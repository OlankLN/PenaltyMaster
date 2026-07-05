import sys
import pygame
from pygame import Surface, Rect
from pygame.font import Font

from const import WIN_WIDTH, WIN_HEIGHT, C_WHITE, C_YELLOW, ASSET_MENU, MENU_OPTION, FONT_HUD


class Menu:
    def __init__(self, window: Surface):
        self.window = window
        raw_bg = pygame.image.load(ASSET_MENU).convert()
        self.img_bg = pygame.transform.smoothscale(raw_bg, (WIN_WIDTH, WIN_HEIGHT))

        # painel semitransparente para o texto ficar legivel sobre a arte
        self.panel = pygame.Surface((WIN_WIDTH, 220), pygame.SRCALPHA)
        self.panel.fill((0, 0, 0, 140))

    def run(self) -> str:
        option = 0
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)

            # a arte do menu.png ja tem o titulo "PENALTY MASTER" desenhado
            self.window.blit(self.img_bg, (0, 0))
            self.window.blit(self.panel, (0, WIN_HEIGHT - 220))

            base_y = WIN_HEIGHT - 190
            for i, opt in enumerate(MENU_OPTION):
                color = C_YELLOW if i == option else C_WHITE
                self._text(FONT_HUD, opt, color, (WIN_WIDTH / 2, base_y + i * 35))

            # Controles (exigencia do enunciado: mostrar no menu)
            self._text(FONT_HUD, 'CONTROLES:', C_YELLOW, (WIN_WIDTH / 2, base_y + 90))
            self._text(FONT_HUD, 'SETA CIMA / SETA BAIXO - Navegar no menu', C_WHITE, (WIN_WIDTH / 2, base_y + 115))
            self._text(FONT_HUD, 'ENTER - Confirmar', C_WHITE, (WIN_WIDTH / 2, base_y + 140))
            self._text(FONT_HUD, 'ESPACO - Travar a barra e chutar (durante o jogo)', C_WHITE,
                       (WIN_WIDTH / 2, base_y + 165))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        option = (option + 1) % len(MENU_OPTION)
                    elif event.key == pygame.K_UP:
                        option = (option - 1) % len(MENU_OPTION)
                    elif event.key == pygame.K_RETURN:
                        return MENU_OPTION[option]

    def _text(self, size: int, text: str, color: tuple, center_pos: tuple):
        font: Font = pygame.font.SysFont('Arial', size, bold=True)
        surf: Surface = font.render(text, True, color)
        rect: Rect = surf.get_rect(center=center_pos)
        self.window.blit(surf, rect)