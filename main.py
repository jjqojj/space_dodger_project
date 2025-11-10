"""
Título:         Space Dodger Game V1.0
Tutor:          John Jairo Quiroga Orozco
Author:         nombre del estudiante
Descripción:    Evita los enemigos que caen.
Requisitos:     pygame
Ejecución:      python main.py
"""



# ---------- Paquetes ----------
import pygame
import random
import sys  


# ---------- Configuración ----------
WIDTH, HEIGHT = 600, 800
FPS = 60
PLAYER_SPEED = 6
ENEMY_SPAWN_EVENT = pygame.USEREVENT + 1
ENEMY_SPAWN_TIME = 800  # ms


# ---------- Inicialización ----------
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Dodger Game - ¡Evita los meteoros Super Milo")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 24)
big_font = pygame.font.SysFont("arial", 48)

# ---------- Colores en formato RGB ----------
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (200,30,30)
GREEN = (30,200,30)
BLUE = (30,144,255)
YELLOW = (255,215,0)

# ---------- Clases ----------
## Observación: utilizaremos clases para crear las plantillas de jugadores (players) y de los enemigos (enemy)
### Nota 1: utilizaremos la clase base de pygames <<pygame.sprite.Sprite>> dentro de las clases <<players>> y <<enemy>>.

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):                                            # Constructur de clase
        super().__init__()                                               # Inicializa el Sprite
        self.image = pygame.Surface((50, 40), pygame.SRCALPHA)           # Crea la apariencia
        pygame.draw.polygon(self.image, BLUE, [(0,40),(25,0),(50,40)])   # Dibuja la nave en la superficie
        self.rect = self.image.get_rect(center=(x,y))                    # Crea la caja de colisión/posición
        self.speed = PLAYER_SPEED

    def update(self, keys):                                              # Método que mueve la nave según teclas.
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        self.rect.x = max(0, min(WIDTH - self.rect.width, self.rect.x))  # Mantener dentro de la pantalla

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, size, speed, color=RED):                           # Constructur de clase
        super().__init__()                                                   # Inicializa el Sprite
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)           # Crea la apariencia
        pygame.draw.circle(self.image, color, (size//2, size//2), size//2)   # Dibuja el enemigo
        self.rect = self.image.get_rect(midtop=(x, -size))                   # Crea la caja de colisión/posición
        self.speed = speed

    def update(self):                                                       #  Método que baja el enemigo en <<y>> con <<self.speed>>. Si sale por abajo, self.kill() lo elimina para no ocupar memoria.
        self.rect.y += self.speed
        if self.rect.top > HEIGHT + 50:
            self.kill()

# ---------- Funciones personalizadas ----------
def draw_text(surface, text, font, color, x, y, center=False):
    img = font.render(text, True, color)
    rect = img.get_rect(topleft=(x,y))
    if center:
        rect = img.get_rect(center=(x,y))
    surface.blit(img, rect)

def spawn_enemy(all_sprites, enemies, score):
    """Crea enemigos con variación según score (aumenta dificultad)."""
    x = random.randint(20, WIDTH-20)
    # dificultad basada en score
    base_speed = 2 + score // 10
    size_choice = random.choices([20, 30, 40, 60], [0.4, 0.35, 0.2, 0.05])[0]
    speed = base_speed + random.random()*2 + (40-size_choice)/20
    color = random.choice([RED, YELLOW, (180,50,200)])
    enemy = Enemy(x, size_choice, speed, color)
    all_sprites.add(enemy)
    enemies.add(enemy)

def handle_collisions(player, enemies):
    """Devuelve True si hay colisión entre jugador y enemigos."""
    return pygame.sprite.spritecollideany(player, enemies) is not None

def show_menu(screen, title, options, selected_idx):
    screen.fill(BLACK)
    draw_text(screen, title, big_font, WHITE, WIDTH//2, 150, center=True)
    for i, opt in enumerate(options):
        color = YELLOW if i == selected_idx else WHITE
        draw_text(screen, opt, font, color, WIDTH//2, 260 + i*40, center=True)
    pygame.display.flip()

def game_over_screen(screen, score):
    screen.fill(BLACK)
    draw_text(screen, "¡Juego Terminado!", big_font, RED, WIDTH//2, HEIGHT//2 - 60, center=True)
    draw_text(screen, f"Puntaje: {int(score)}", font, WHITE, WIDTH//2, HEIGHT//2, center=True)
    draw_text(screen, "Presiona ENTER para volver al menú", font, WHITE, WIDTH//2, HEIGHT//2 + 50, center=True)
    pygame.display.flip()
    wait_for_enter()

def wait_for_enter():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False
        clock.tick(FPS)

# ---------- Menú principal ----------
def main_menu():
    selected = 0
    options = ["Jugar", "Instrucciones", "Salir"]
    while True:
        show_menu(screen, "Space Dodger Game V1.0", options, selected)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                if event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                if event.key == pygame.K_RETURN:
                    if options[selected] == "Jugar":
                        game_loop()
                    elif options[selected] == "Instrucciones":
                        instructions_screen()
                    elif options[selected] == "Salir":
                        pygame.quit(); sys.exit()
        clock.tick(FPS)

def instructions_screen():
    screen.fill(BLACK)
    draw_text(screen, "Instrucciones", big_font, WHITE, WIDTH//2, 80, center=True)
    draw_text(screen, "Muevete con ← → o A D. Evita los enemigos que caen.", font, WHITE, WIDTH//2, 180, center=True)
    draw_text(screen, "Sobrevive el mayor tiempo posible. Presiona ENTER para volver.", font, WHITE, WIDTH//2, 220, center=True)
    pygame.display.flip()
    wait_for_enter()

# ---------- Bucle del juego ----------
def game_loop():
    # --- GRUPOS ---
    all_sprites = pygame.sprite.Group()  # contiene todo lo que se dibuja
    enemies     = pygame.sprite.Group()  # solo los enemigos (para colisiones)

    # --- JUGADOR ---
    player = Player(WIDTH//2, HEIGHT-80)
    all_sprites.add(player)

    # --- VARIABLES DE JUEGO ---
    score = 0
    level_time = 0
    paused = False
    running = True

    # --- EVENTO DE ENEMIGOS ---
    pygame.time.set_timer(ENEMY_SPAWN_EVENT, ENEMY_SPAWN_TIME)

    # --- BUCLE PRINCIPAL DEL JUEGO ---
    while running:
        dt = clock.tick(FPS)  # tiempo entre frames (milisegundos)

        # --- GESTIÓN DE EVENTOS ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # crear enemigos automáticamente
            if event.type == ENEMY_SPAWN_EVENT and not paused:
                spawn_enemy(all_sprites, enemies, score)

            # pausar/despausar con la tecla P
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused

        # --- ENTRADA DE TECLADO ---
        keys = pygame.key.get_pressed()

        # --- ACTUALIZAR OBJETOS ---
        if not paused:
            player.update(keys)   # el jugador usa las teclas
            enemies.update()      # los enemigos bajan automáticamente

            # --- DETECTAR COLISIONES ---
            if handle_collisions(player, enemies):
                running = False

            # --- ACTUALIZAR PUNTUACIÓN Y DIFICULTAD ---
            score += dt / 1000  # sube 1 punto por segundo aprox.
            level_time += dt

            # cada 10 segundos, aumenta dificultad (reduce tiempo de spawn)
            if level_time > 10000:
                level_time = 0
                new_interval = max(250, ENEMY_SPAWN_TIME - 50)
                pygame.time.set_timer(ENEMY_SPAWN_EVENT, new_interval)

        # --- DIBUJAR EN PANTALLA ---
        screen.fill((10,10,30))             # fondo oscuro
        all_sprites.draw(screen)            # dibuja jugador y enemigos

        # HUD (texto de interfaz)
        draw_text(screen, f"Puntaje: {int(score)}", font, WHITE, 10, 10)
        draw_text(screen, "Pausa: P", font, WHITE, WIDTH-120, 10)

        if paused:
            draw_text(screen, "PAUSADO", big_font, (255,255,0), WIDTH//2, HEIGHT//2, center=True)

        pygame.display.flip()  # actualiza pantalla

    # --- CUANDO TERMINA EL JUEGO ---
    game_over_screen(screen, score)

# ---------- Start ----------
if __name__ == "__main__":
    main_menu()