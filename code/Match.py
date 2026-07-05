import random
import sys
import pygame
from pygame import Surface, Rect
from pygame.font import Font

from const import (
    WIN_WIDTH, WIN_HEIGHT, C_WHITE, C_BLACK, C_YELLOW, C_RED, C_GRAY, C_GREEN_FIELD,
    ASSET_GOAL, ASSET_GOLEIRO, ASSET_BOLA,
    BG_HEIGHT, GOAL_LEFT, GOAL_RIGHT, GOAL_TOP, GOAL_BOTTOM, ZONE_WIDTH,
    BALL_TARGET_Y_RATIO, BALL_START_POS,
    GOLEIRO_BBOX, GOLEIRO_DISPLAY_HEIGHT,
    BOLA_BBOX, BOLA_DISPLAY_SIZE,
    BAR_LEFT, BAR_RIGHT, BAR_Y, BAR_HEIGHT, BAR_BASE_SPEED, BAR_SPEED_INCREMENT,
    MAX_KICKS, GOALS_TO_WIN, SAVES_TO_LOSE,
    KICK_ANIM_DURATION, RESULT_PAUSE_DURATION,
    FONT_HUD, FONT_RESULT,
)


class Match:
    """
    Maquina de estados de uma cobranca:
      'aiming'    -> barra de timing se movendo, esperando ESPACO
      'animating' -> bola indo em direcao ao gol / goleiro se jogando
      'result'    -> mostra GOL! ou DEFENDEU! por um tempo
      'done'      -> partida encerrada (3 gols ou 3 defesas ou 5 cobrancas)
    """

    def __init__(self, window: Surface):
        self.window = window
        self._load_assets()

        self.kick_number = 0
        self.player_goals = 0
        self.keeper_saves = 0

        self.bar_width = BAR_RIGHT - BAR_LEFT
        self.bar_pos = 0.0
        self.bar_dir = 1

        self.state = 'aiming'
        self.state_start_time = 0

        self.chosen_zone = None   # 0=esquerda, 1=centro, 2=direita
        self.keeper_zone = None
        self.is_goal = False
        self.result_text = ''

        self.ball_pos = list(BALL_START_POS)

    # ------------------------------------------------------------------
    # Carregamento de assets
    # ------------------------------------------------------------------

    def _load_assets(self):
        # Fundo do gol, redimensionado para a largura da janela
        raw_goal = pygame.image.load(ASSET_GOAL).convert()
        self.img_goal = pygame.transform.smoothscale(raw_goal, (WIN_WIDTH, BG_HEIGHT))

        # Goleiro: recorta so o personagem (remove a margem transparente) e escala
        raw_goleiro = pygame.image.load(ASSET_GOLEIRO).convert_alpha()
        x_min, y_min, x_max, y_max = GOLEIRO_BBOX
        trimmed_goleiro = raw_goleiro.subsurface(Rect(x_min, y_min, x_max - x_min, y_max - y_min)).copy()
        aspect = trimmed_goleiro.get_width() / trimmed_goleiro.get_height()
        keeper_w = round(GOLEIRO_DISPLAY_HEIGHT * aspect)
        self.img_goleiro = pygame.transform.smoothscale(trimmed_goleiro, (keeper_w, GOLEIRO_DISPLAY_HEIGHT))

        # Bola: mesmo processo de recorte + escala
        raw_bola = pygame.image.load(ASSET_BOLA).convert_alpha()
        x_min, y_min, x_max, y_max = BOLA_BBOX
        trimmed_bola = raw_bola.subsurface(Rect(x_min, y_min, x_max - x_min, y_max - y_min)).copy()
        self.img_bola = pygame.transform.smoothscale(trimmed_bola, (BOLA_DISPLAY_SIZE, BOLA_DISPLAY_SIZE))

    def run(self) -> bool:
        """Executa a partida. Retorna True se o jogador venceu, False caso contrario."""
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.state == 'aiming':
                        self._lock_bar()

            self._update()
            self._draw()
            pygame.display.flip()

            if self.state == 'done':
                return self.player_goals >= GOALS_TO_WIN

    # ------------------------------------------------------------------
    # Logica
    # ------------------------------------------------------------------

    def _bar_speed(self) -> float:
        return BAR_BASE_SPEED + self.kick_number * BAR_SPEED_INCREMENT

    def _update(self):
        if self.state == 'aiming':
            speed = self._bar_speed()
            self.bar_pos += self.bar_dir * speed
            if self.bar_pos >= self.bar_width:
                self.bar_pos = self.bar_width
                self.bar_dir = -1
            elif self.bar_pos <= 0:
                self.bar_pos = 0
                self.bar_dir = 1

        elif self.state == 'animating':
            elapsed = pygame.time.get_ticks() - self.state_start_time
            progress = min(elapsed / KICK_ANIM_DURATION, 1.0)
            target_x = GOAL_LEFT + ZONE_WIDTH * (self.chosen_zone + 0.5)
            target_y = GOAL_TOP + (GOAL_BOTTOM - GOAL_TOP) * BALL_TARGET_Y_RATIO
            self.ball_pos[0] = BALL_START_POS[0] + (target_x - BALL_START_POS[0]) * progress
            self.ball_pos[1] = BALL_START_POS[1] + (target_y - BALL_START_POS[1]) * progress
            if progress >= 1.0:
                self._resolve_kick()

        elif self.state == 'result':
            elapsed = pygame.time.get_ticks() - self.state_start_time
            if elapsed >= RESULT_PAUSE_DURATION:
                self._next_kick_or_finish()

    def _lock_bar(self):
        relative = self.bar_pos / self.bar_width  # 0.0 a 1.0
        if relative < 1 / 3:
            zone = 0
        elif relative < 2 / 3:
            zone = 1
        else:
            zone = 2

        self.chosen_zone = zone
        self.keeper_zone = random.choice((0, 1, 2))  # 100% aleatorio, sem pistas
        self.ball_pos = list(BALL_START_POS)
        self.state = 'animating'
        self.state_start_time = pygame.time.get_ticks()

    def _resolve_kick(self):
        self.is_goal = self.chosen_zone != self.keeper_zone
        if self.is_goal:
            self.player_goals += 1
            self.result_text = 'GOOOL!'
        else:
            self.keeper_saves += 1
            self.result_text = 'DEFENDEU!'
        self.state = 'result'
        self.state_start_time = pygame.time.get_ticks()

    def _next_kick_or_finish(self):
        self.kick_number += 1
        if (self.player_goals >= GOALS_TO_WIN or
                self.keeper_saves >= SAVES_TO_LOSE or
                self.kick_number >= MAX_KICKS):
            self.state = 'done'
        else:
            self.bar_pos = 0.0
            self.bar_dir = 1
            self.state = 'aiming'
            self.keeper_zone = None

    # ------------------------------------------------------------------
    # Desenho
    # ------------------------------------------------------------------

    def _draw(self):
        # fundo: imagem do gol no topo + grama solida no restante da janela
        self.window.fill(C_GREEN_FIELD)
        self.window.blit(self.img_goal, (0, 0))

        # goleiro sempre visivel; usa o centro (zona 1) se ainda nao decidiu pra onde pular
        zona_goleiro = self.keeper_zone if self.keeper_zone is not None else 1
        keeper_x = GOAL_LEFT + ZONE_WIDTH * (zona_goleiro + 0.5)
        keeper_rect = self.img_goleiro.get_rect()
        keeper_rect.centerx = round(keeper_x)
        keeper_rect.bottom = GOAL_BOTTOM
        self.window.blit(self.img_goleiro, keeper_rect)

        # bola
        pos = self.ball_pos if self.state in ('animating', 'result', 'done') else list(BALL_START_POS)
        ball_rect = self.img_bola.get_rect(center=(round(pos[0]), round(pos[1])))
        self.window.blit(self.img_bola, ball_rect)

        # barra de timing
        bar_bg = Rect(BAR_LEFT, BAR_Y, self.bar_width, BAR_HEIGHT)
        pygame.draw.rect(self.window, C_GRAY, bar_bg)
        third = self.bar_width / 3
        pygame.draw.line(self.window, C_BLACK, (BAR_LEFT + third, BAR_Y),
                          (BAR_LEFT + third, BAR_Y + BAR_HEIGHT), 2)
        pygame.draw.line(self.window, C_BLACK, (BAR_LEFT + 2 * third, BAR_Y),
                          (BAR_LEFT + 2 * third, BAR_Y + BAR_HEIGHT), 2)
        marker_x = BAR_LEFT + self.bar_pos
        pygame.draw.rect(self.window, C_RED, Rect(marker_x - 3, BAR_Y - 6, 6, BAR_HEIGHT + 12))

        # HUD
        self._text(FONT_HUD, f'Gols: {self.player_goals}/{GOALS_TO_WIN}', C_YELLOW, (100, BG_HEIGHT + 25))
        self._text(FONT_HUD, f'Defesas: {self.keeper_saves}/{SAVES_TO_LOSE}', C_YELLOW,
                   (WIN_WIDTH - 100, BG_HEIGHT + 25))
        self._text(FONT_HUD, f'Cobranca {min(self.kick_number + 1, MAX_KICKS)}/{MAX_KICKS}',
                   C_WHITE, (WIN_WIDTH / 2, BG_HEIGHT + 25))

        if self.state == 'aiming':
            self._text(FONT_HUD, 'ESPACO - Travar a barra', C_WHITE, (WIN_WIDTH / 2, BAR_Y + 45))

        if self.state in ('result', 'done'):
            color = C_YELLOW if self.is_goal else C_RED
            self._text(FONT_RESULT, self.result_text, color, (WIN_WIDTH / 2, GOAL_TOP - 30))

    def _text(self, size: int, text: str, color: tuple, center_pos: tuple):
        font: Font = pygame.font.SysFont('Arial', size, bold=True)
        surf: Surface = font.render(text, True, color)
        rect: Rect = surf.get_rect(center=center_pos)
        self.window.blit(surf, rect)