import sys
import pygame
from pygame import Surface, Rect
from pygame.font import Font

from NameEntry import NameEntry
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

            if choice == MENU_OPTION[0]:      # '1 PLAYER'
                names = self._collect_names(1)
                self._play_match(names)
            elif choice == MENU_OPTION[1]:    # '2 PLAYERS'
                names = self._collect_names(2)
                self._play_match(names)
            elif choice == MENU_OPTION[2]:    # 'EXIT'
                pygame.quit()
                sys.exit()

    def _collect_names(self, num_players: int) -> list:
        name_entry = NameEntry(self.window)
        names = []
        for i in range(num_players):
            prompt = f'Digite o nome do Jogador {i + 1}:'
            names.append(name_entry.run(prompt))
        return names

    def _play_match(self, names: list):
        match = Match(self.window, names)
        result = match.run()
        self._show_end_screen(result)

    def _show_end_screen(self, result: dict):
        players = result['players']
        winner_index = result['winner_index']

        if len(players) == 1:
            won = winner_index == 0
            title = 'VOCE VENCEU!' if won else 'VOCE PERDEU!'
            subtitle = f'{players[0].name} - Gols: {players[0].goals}'
            title_color = C_YELLOW if won else C_WHITE
        else:
            vencedor = players[winner_index]
            title = f'{vencedor.name} VENCEU!'
            title_color = C_YELLOW
            subtitle = f'{players[0].name}: {players[0].goals} gols   |   {players[1].name}: {players[1].goals} gols'

        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            self.window.fill(C_DARK_GREEN)

            self._text(FONT_TITLE, title, title_color, (WIN_WIDTH / 2, WIN_HEIGHT / 2 - 50))
            self._text(FONT_HUD, subtitle, C_WHITE, (WIN_WIDTH / 2, WIN_HEIGHT / 2))
            self._text(FONT_HUD, 'Pressione ENTER para voltar ao menu', C_WHITE,
                       (WIN_WIDTH / 2, WIN_HEIGHT / 2 + 50))

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