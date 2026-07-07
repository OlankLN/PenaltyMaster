# ============================================================
# PENALTY MASTER - Constantes do jogo
# ============================================================
import os

# ------------------------------------------------------------
# Caminho dos assets (pasta 'asset' irma da pasta 'code')
# ------------------------------------------------------------
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))            # .../code
ASSET_DIR = os.path.join(os.path.dirname(_THIS_DIR), 'asset')     # .../asset


def asset_path(filename: str) -> str:
    return os.path.join(ASSET_DIR, filename)


ASSET_GOAL = asset_path('goal.jpg')
ASSET_MENU = asset_path('menu.png')
ASSET_GOLEIRO = asset_path('goleiro.PNG')
ASSET_BOLA = asset_path('bola.PNG')

# ------------------------------------------------------------
# Janela
# ------------------------------------------------------------
WIN_WIDTH = 700
WIN_HEIGHT = 540

# ------------------------------------------------------------
# Fundo do gol (goal.jpg tem 612x343 originalmente).
# A imagem e redimensionada para caber na largura da janela,
# mantendo a proporcao original.
# ------------------------------------------------------------
_GOAL_IMG_ORIGINAL_SIZE = (612, 343)
BG_SCALE = WIN_WIDTH / _GOAL_IMG_ORIGINAL_SIZE[0]
BG_HEIGHT = round(_GOAL_IMG_ORIGINAL_SIZE[1] * BG_SCALE)  # ~392

# Cor da grama (extraida do proprio goal.jpg) usada para preencher
# o espaco abaixo da imagem de fundo (onde fica a barra/HUD)
C_GREEN_FIELD = (52, 167, 4)

# ------------------------------------------------------------
# Area da trave DENTRO da imagem goal.jpg, medida em pixels
# na imagem ORIGINAL (612x343) e depois escalada para a janela.
# ------------------------------------------------------------
_GOAL_FRAME_ORIGINAL = {
    'left': 168,
    'right': 443,
    'top': 70,
    'bottom': 205,
}
GOAL_LEFT = round(_GOAL_FRAME_ORIGINAL['left'] * BG_SCALE)
GOAL_RIGHT = round(_GOAL_FRAME_ORIGINAL['right'] * BG_SCALE)
GOAL_TOP = round(_GOAL_FRAME_ORIGINAL['top'] * BG_SCALE)
GOAL_BOTTOM = round(_GOAL_FRAME_ORIGINAL['bottom'] * BG_SCALE)
ZONE_WIDTH = (GOAL_RIGHT - GOAL_LEFT) / 3  # 3 zonas: esquerda, centro, direita

# Onde a bola "chega" visualmente dentro da trave (um pouco abaixo do topo)
BALL_TARGET_Y_RATIO = 0.4  # 0.0 = topo da trave, 1.0 = linha do gol

# Posicao inicial da bola (marca do penalti, ja desenhada no goal.jpg)
BALL_START_POS = (349, 345)

# ------------------------------------------------------------
# Cores gerais
# ------------------------------------------------------------
C_WHITE = (255, 255, 255)
C_BLACK = (0, 0, 0)
C_DARK_GREEN = (20, 90, 20)
C_YELLOW = (255, 215, 0)
C_RED = (200, 30, 30)
C_GRAY = (140, 140, 140)

# ------------------------------------------------------------
# Sprites (goleiro.PNG e bola.PNG tem bordas transparentes;
# esses retangulos recortam so o conteudo real do personagem,
# medidos na imagem ORIGINAL de cada arquivo)
# ------------------------------------------------------------
# (x_min, y_min, x_max, y_max)
GOLEIRO_BBOX = (176, 215, 686, 863)
GOLEIRO_DISPLAY_HEIGHT = 130  # altura final desenhada na tela

BOLA_BBOX = (217, 219, 871, 860)
BOLA_DISPLAY_SIZE = 26  # diametro final desenhado na tela

# ------------------------------------------------------------
# Barra de timing (posicionada abaixo da imagem de fundo)
# ------------------------------------------------------------
BAR_LEFT = 100
BAR_RIGHT = 600
BAR_Y = BG_HEIGHT + 90
BAR_HEIGHT = 20
BAR_BASE_SPEED = 6.0        # velocidade do marcador na 1a cobranca
BAR_SPEED_INCREMENT = 1.5   # aumenta a cada cobranca (fica mais dificil)

# ------------------------------------------------------------
# Regras da partida
# ------------------------------------------------------------
MAX_KICKS = 5
GOALS_TO_WIN = 3
SAVES_TO_LOSE = 3
MAX_NAME_LENGTH = 10  # quantidade maxima de caracteres no nome do jogador

# Duracao das animacoes (ms)
KICK_ANIM_DURATION = 500
RESULT_PAUSE_DURATION = 1200

# Tamanhos de fonte
FONT_TITLE = 46
FONT_SUBTITLE = 22
FONT_HUD = 20
FONT_RESULT = 36

# Menu
MENU_OPTION = ('1 PLAYER', '2 PLAYERS', 'EXIT')