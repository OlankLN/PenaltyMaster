import sys
import pygame
from pygame import Surface, Rect
from pygame.font import Font

from const import WIN_WIDTH, WIN_HEIGHT, MENU_OPTION, C_DARK_GREEN, C_YELLOW, C_WHITE, FONT_TITLE, FONT_HUD
from Menu import Menu
from Match import Match


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption('Penalty Master')

    def run(self):
        while True:
            menu = Menu(self.window)
            choice = menu.run()

            if choice == MENU_OPTION[0]:  # START GAME
                match = Match(self.window)
                won = match.run()
                self._show_end_screen(won)
            elif choice == MENU_OPTION[1]:  # EXIT
                pygame.quit()
                sys.exit()

    def _show_end_screen(self, won: bool):
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            self.window.fill(C_DARK_GREEN)

            title = 'VOCE VENCEU!' if won else 'VOCE PERDEU!'
            color = C_YELLOW if won else C_WHITE
            self._text(FONT_TITLE, title, color, (WIN_WIDTH / 2, WIN_HEIGHT / 2 - 30))
            self._text(FONT_HUD, 'Pressione ENTER para voltar ao menu', C_WHITE,
                       (WIN_WIDTH / 2, WIN_HEIGHT / 2 + 30))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    return

    def _text(self, size: int, text: str, color: tuple, center_pos: tuple):
        font: Font = pygame.font.SysFont('Arial', size, bold=True)
        surf: Surface = font.render(text, True, color)
        rect: Rect = surf.get_rect(center=center_pos)
        self.window.blit(surf, rect)